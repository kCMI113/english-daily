import os
import json

import jinja2


class WebBuilder:
    def __init__(self, template_dir: str = None):
        if template_dir is None:
            template_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_dir),
            autoescape=True,
        )

    def build(
        self,
        new_expressions: list[dict],
        review_expressions: list[dict],
        metadata: dict,
    ) -> str:
        template = self.env.get_template("web_template.html")
        return template.render(
            date=metadata["date"],
            category_ko=metadata["category_ko"],
            difficulty_ko=metadata["difficulty_ko"],
            new_expressions=new_expressions,
            review_expressions=review_expressions,
            stats=metadata["stats"],
        )

    def save(self, html: str, docs_dir: str, date: str):
        """Save web page, update index, and update dates.json."""
        os.makedirs(docs_dir, exist_ok=True)
        # Save daily page
        filepath = os.path.join(docs_dir, f"{date}.html")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        # Update dates.json
        self._update_dates_json(docs_dir, date)
        # Update index.html to redirect to latest
        index_path = os.path.join(docs_dir, "index.html")
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(self._build_index(docs_dir, date))

    def _update_dates_json(self, docs_dir: str, date: str):
        """Maintain a sorted list of all dates for navigation."""
        dates_path = os.path.join(docs_dir, "dates.json")
        dates = []
        if os.path.exists(dates_path):
            with open(dates_path, "r", encoding="utf-8") as f:
                dates = json.load(f)
        if date not in dates:
            dates.append(date)
            dates.sort()
        with open(dates_path, "w", encoding="utf-8") as f:
            json.dump(dates, f)

    def _build_index(self, docs_dir: str, _unused: str = "") -> str:
        """Build index page that redirects to the latest date."""
        dates = sorted(
            [f.replace(".html", "") for f in os.listdir(docs_dir)
             if f.endswith(".html") and f != "index.html"],
            reverse=True,
        )
        latest = dates[0] if dates else ""
        links = "\n".join(
            f'      <li><a href="{d}.html">{d}</a></li>' for d in dates
        )
        return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="refresh" content="0; url={latest}.html">
  <title>Daily English Conversation</title>
  <style>
    body {{ font-family: -apple-system, sans-serif; max-width: 480px; margin: 40px auto; padding: 0 16px; }}
    h1 {{ font-size: 20px; color: #1a365d; }}
    ul {{ list-style: none; padding: 0; }}
    li {{ padding: 8px 0; border-bottom: 1px solid #eee; }}
    a {{ color: #2b6cb0; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
  </style>
</head>
<body>
  <h1>Daily English Conversation</h1>
  <p>Redirecting to latest...</p>
  <ul>
{links}
  </ul>
</body>
</html>"""
