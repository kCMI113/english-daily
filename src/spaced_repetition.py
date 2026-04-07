import json
import os
from datetime import date, timedelta


class SpacedRepetitionManager:
    def __init__(self, history_path: str, config: dict):
        self.history_path = history_path
        self.config = config
        self.intervals = {
            int(k): v
            for k, v in config["spaced_repetition"]["intervals"].items()
        }
        self.retire_after = config["spaced_repetition"]["retire_after_box"]
        self.data = self._load()

    def _load(self) -> dict:
        defaults = {
            "metadata": {
                "last_run": None,
                "total_expressions_learned": 0,
                "current_category_index": 0,
            },
            "expressions": {},
        }
        if os.path.exists(self.history_path):
            with open(self.history_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Fill missing keys
            for key, val in defaults["metadata"].items():
                data.setdefault("metadata", {})[key] = data.get("metadata", {}).get(key, val)
            data.setdefault("expressions", {})
            return data
        return defaults

    def save(self):
        with open(self.history_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def get_due_reviews(self, today: str) -> list[dict]:
        """Return expressions due for review today, sorted by box (lower first)."""
        max_items = self.config["study"]["max_review_items"]
        due = []

        for expr_id, expr in self.data["expressions"].items():
            box = expr.get("box", 1)
            next_review = expr.get("next_review", "")
            if box <= self.retire_after and next_review <= today:
                due.append({"id": expr_id, **expr})

        due.sort(key=lambda x: (x.get("box", 1), x.get("last_reviewed", "")))
        return due[:max_items]

    def add_new_expressions(self, expressions: list[dict], today: str):
        """Add today's new expressions to box 1."""
        for expr in expressions:
            expr_id = expr["id"]
            next_review = self._calc_next_review(today, 1)
            self.data["expressions"][expr_id] = {
                "expression": expr["expression"],
                "meaning_ko": expr["meaning_ko"],
                "category_ko": expr.get("category_ko", ""),
                "box": 1,
                "first_seen": today,
                "last_reviewed": today,
                "next_review": next_review,
                "review_count": 0,
                "examples": expr["examples"][:2],
                "synonyms": expr.get("synonyms", []),
                "antonyms": expr.get("antonyms", []),
            }
        self.data["metadata"]["total_expressions_learned"] += len(expressions)

    def promote_reviewed(self, expr_ids: list[str], today: str):
        """Promote reviewed expressions to next box."""
        for expr_id in expr_ids:
            if expr_id not in self.data["expressions"]:
                continue
            expr = self.data["expressions"][expr_id]
            new_box = expr.get("box", 1) + 1
            expr["box"] = new_box
            expr["last_reviewed"] = today
            expr["review_count"] = expr.get("review_count", 0) + 1
            if new_box <= self.retire_after:
                expr["next_review"] = self._calc_next_review(today, new_box)
            else:
                expr["next_review"] = "retired"

    def get_recent_expressions(self, days: int = 90) -> list[str]:
        """Get list of expression strings from recent days for deduplication."""
        cutoff = (date.today() - timedelta(days=days)).isoformat()
        return [
            expr["expression"]
            for expr in self.data["expressions"].values()
            if expr.get("first_seen", "") >= cutoff
        ]

    def get_stats(self) -> dict:
        """Get learning statistics."""
        expressions = self.data["expressions"]
        total = len(expressions)
        by_box = {}
        retired = 0
        for expr in expressions.values():
            box = expr.get("box", 1)
            if box > self.retire_after:
                retired += 1
            else:
                by_box[box] = by_box.get(box, 0) + 1

        return {
            "total_learned": self.data["metadata"]["total_expressions_learned"],
            "active": total - retired,
            "retired": retired,
            "by_box": by_box,
        }

    def archive_content(self, content: dict, log_path: str):
        """Archive generated content to content_log.json."""
        if os.path.exists(log_path):
            with open(log_path, "r", encoding="utf-8") as f:
                log = json.load(f)
        else:
            log = {}

        log[content["date"]] = {
            "category": content["category"]["name"],
            "category_ko": content["category"]["label_ko"],
            "expressions": [
                {
                    "id": e["id"],
                    "expression": e["expression"],
                    "meaning_ko": e["meaning_ko"],
                }
                for e in content["expressions"]
            ],
        }

        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(log, f, ensure_ascii=False, indent=2)

    def update_last_run(self, today: str):
        self.data["metadata"]["last_run"] = today

    def _calc_next_review(self, from_date: str, box: int) -> str:
        d = date.fromisoformat(from_date)
        interval = self.intervals.get(box, 1)
        return (d + timedelta(days=interval)).isoformat()
