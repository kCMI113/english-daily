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
        # Update index.html as a home page with links to latest study and slang
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
        """Build the GitHub Pages home page."""
        dates = sorted(
            [f.replace(".html", "") for f in os.listdir(docs_dir)
             if f.endswith(".html") and f != "index.html" and f[:4].isdigit()],
            reverse=True,
        )
        latest = dates[0] if dates else ""
        links = "\n".join(
            f'      <li><a href="{d}.html">{d}</a></li>' for d in dates
        )
        latest_card = (
            f'<a class="card primary" href="{latest}.html">'
            f'<span class="label">Latest</span><strong>{latest}</strong>'
            f'<small>오늘의 영어회화 학습과 복습</small></a>'
            if latest else
            '<div class="card primary"><span class="label">Latest</span><strong>준비 중</strong></div>'
        )
        slang_card = (
            '<a class="card accent" href="slang.html">'
            '<span class="label">Slang</span><strong>Slang Glossary</strong>'
            '<small>알파벳별 슬랭 표현, 예문, TTS</small></a>'
            if os.path.exists(os.path.join(docs_dir, "slang.html")) else
            '<div class="card accent"><span class="label">Slang</span><strong>준비 중</strong></div>'
        )
        return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="cache-control" content="no-cache, no-store, must-revalidate">
  <meta http-equiv="pragma" content="no-cache">
  <title>Daily English Conversation</title>
  <style>
    * {{ box-sizing: border-box; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 0; background: #f5f7fb; color: #172033; }}
    header {{ background: #152238; color: #fff; padding: 28px 18px 22px; }}
    main, .wrap {{ max-width: 860px; margin: 0 auto; }}
    main {{ padding: 18px; }}
    h1 {{ margin: 0; font-size: 28px; letter-spacing: 0; }}
    .sub {{ margin: 8px 0 0; color: #c9d6e8; font-size: 14px; }}
    .cards {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; margin-bottom: 22px; }}
    .card {{ display: block; min-height: 136px; border: 1px solid #dce4ef; border-radius: 8px; padding: 18px; text-decoration: none; color: #172033; background: #fff; box-shadow: 0 1px 3px rgba(14, 31, 53, .04); }}
    .card:hover {{ border-color: #2f6fbd; }}
    .card.primary {{ border-top: 4px solid #2f6fbd; }}
    .card.accent {{ border-top: 4px solid #2f8f6b; }}
    .label {{ display: block; color: #6b7890; font-size: 12px; font-weight: 700; text-transform: uppercase; margin-bottom: 10px; }}
    strong {{ display: block; font-size: 22px; margin-bottom: 8px; }}
    small {{ color: #516178; font-size: 14px; }}
    h2 {{ font-size: 18px; margin: 0 0 8px; }}
    ul {{ list-style: none; padding: 0; margin: 0; background: #fff; border: 1px solid #dce4ef; border-radius: 8px; overflow: hidden; }}
    li {{ border-bottom: 1px solid #edf1f6; }}
    li:last-child {{ border-bottom: 0; }}
    li a {{ display: block; padding: 10px 14px; color: #2f6fbd; text-decoration: none; }}
    li a:hover {{ background: #eef4ff; }}
    @media (max-width: 640px) {{
      h1 {{ font-size: 23px; }}
      .cards {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="wrap">
      <h1>Daily English Conversation</h1>
      <p class="sub">매일 영어회화와 슬랭 표현 학습</p>
    </div>
  </header>
  <main>
    <section class="cards">
      {latest_card}
      {slang_card}
    </section>
    <h2>Daily Archive</h2>
    <ul>
{links}
    </ul>
  </main>
</body>
</html>"""
