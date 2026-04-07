import os
import sys
from datetime import date

import yaml

from .llm_client import LLMClient
from .content_generator import ContentGenerator, DIFFICULTY_MAP
from .spaced_repetition import SpacedRepetitionManager
from .email_builder import EmailBuilder
from .email_sender import EmailSender
from .web_builder import WebBuilder

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_config() -> dict:
    config_path = os.path.join(BASE_DIR, "config.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_subject(today: str, category_ko: str, new_count: int, review_count: int, prefix: str) -> str:
    month = int(today.split("-")[1])
    day = int(today.split("-")[2])
    parts = [f"{prefix} {month}월 {day}일 - {category_ko} 표현 {new_count}개"]
    if review_count > 0:
        parts[0] += f" + 복습 {review_count}개"
    return parts[0]


def main():
    config = load_config()
    if len(sys.argv) > 1:
        today = sys.argv[1]
        date.fromisoformat(today)  # validate format
    else:
        today = date.today().isoformat()

    # Paths
    history_path = os.path.join(BASE_DIR, "data", "history.json")
    content_log_path = os.path.join(BASE_DIR, "data", "content_log.json")

    # 1. Load spaced repetition state
    sr = SpacedRepetitionManager(history_path, config)

    # 2. Get reviews due today
    reviews = sr.get_due_reviews(today)

    # 3. Category
    category = config["category"]

    # 4. Get recent expressions for deduplication
    recent = sr.get_recent_expressions(days=30)

    # 5. Generate new content
    print(f"Generating {config['study']['expressions_per_day']} expressions for '{category['label_ko']}'...")
    llm_client = LLMClient(config)
    generator = ContentGenerator(llm_client, config)
    content = generator.generate(
        today=today,
        category=category,
        difficulty=config["study"]["difficulty"],
        exclude_expressions=recent,
    )
    print(f"Generated {len(content['expressions'])} expressions.")

    # 6. Add new expressions to history
    sr.add_new_expressions(content["expressions"], today)

    # 7. Promote reviewed expressions
    review_ids = [r["id"] for r in reviews]
    sr.promote_reviewed(review_ids, today)

    # 8. Build email
    difficulty = config["study"]["difficulty"]
    metadata = {
        "date": today,
        "category_ko": category["label_ko"],
        "difficulty_ko": DIFFICULTY_MAP.get(difficulty, "중급"),
        "stats": sr.get_stats(),
    }

    builder = EmailBuilder()
    html = builder.build(
        new_expressions=content["expressions"],
        review_expressions=reviews,
        metadata=metadata,
    )

    # 9. Send email
    to_email = os.environ.get("EMAIL_TO")
    if to_email:
        subject = build_subject(
            today,
            category["label_ko"],
            len(content["expressions"]),
            len(reviews),
            config["email"]["subject_prefix"],
        )
        sender = EmailSender()
        if not sender.send(to_email, subject, html):
            print("Warning: Email delivery failed")
    else:
        # Save HTML locally for testing
        out_path = os.path.join(BASE_DIR, "output.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"No EMAIL_TO set. Saved HTML to {out_path}")

    # 10. Build web version (with TTS)
    docs_dir = os.path.join(BASE_DIR, "docs")
    web_builder = WebBuilder()
    web_html = web_builder.build(
        new_expressions=content["expressions"],
        review_expressions=reviews,
        metadata=metadata,
    )
    web_builder.save(web_html, docs_dir, today)
    print(f"Web version saved to docs/{today}.html")

    # 11. Save state
    sr.update_last_run(today)
    sr.save()
    sr.archive_content(content, content_log_path)

    print(f"Done! {today} - {category['label_ko']}, "
          f"new: {len(content['expressions'])}, review: {len(reviews)}")


if __name__ == "__main__":
    main()
