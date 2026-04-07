import os

import jinja2


class EmailBuilder:
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
        template = self.env.get_template("email_template.html")
        return template.render(
            date=metadata["date"],
            category_ko=metadata["category_ko"],
            difficulty_ko=metadata["difficulty_ko"],
            new_expressions=new_expressions,
            review_expressions=review_expressions,
            stats=metadata["stats"],
        )
