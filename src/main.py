import os
import sys
from datetime import date

import yaml

from .llm_client import LLMClient
from .content_generator import ContentGenerator, DIFFICULTY_MAP
from .spaced_repetition import SpacedRepetitionManager
from .web_builder import WebBuilder

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_config() -> dict:
    config_path = os.path.join(BASE_DIR, "config.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


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

    # 8. Build web version
    difficulty = config["study"]["difficulty"]
    metadata = {
        "date": today,
        "category_ko": category["label_ko"],
        "difficulty_ko": DIFFICULTY_MAP.get(difficulty, "중급"),
    }

    docs_dir = os.path.join(BASE_DIR, "docs")
    web_builder = WebBuilder()
    web_html = web_builder.build(
        new_expressions=content["expressions"],
        review_expressions=reviews,
        metadata=metadata,
    )
    web_builder.save(web_html, docs_dir, today)
    print(f"Web version saved to docs/{today}.html")

    # 9. Save state
    sr.update_last_run(today)
    sr.save()
    sr.archive_content(content, content_log_path)

    print(f"Done! {today} - {category['label_ko']}, "
          f"new: {len(content['expressions'])}, review: {len(reviews)}")


if __name__ == "__main__":
    main()
