import json
import os
import re
from datetime import date

from .llm_client import LLMClient

DIFFICULTY_MAP = {
    "beginner": "초급",
    "intermediate": "중급",
    "advanced": "고급",
}

SYSTEM_PROMPT = """당신은 한국인 성인을 위한 영어회화 학습 콘텐츠를 만드는 전문 영어 교사입니다.
반드시 유효한 JSON만 반환하세요. 마크다운이나 추가 텍스트 없이 JSON만 출력하세요.

## JSON 구조
{
  "expressions": [
    {
      "type": "word | phrase | idiom | phrasal_verb",
      "expression": "영어 표현 (소문자로)",
      "pronunciation": "한글 발음 표기",
      "meaning_ko": "한국어 뜻 (간결하게 2~5단어)",
      "explanation_ko": "실제 회화에서 언제/어떻게 쓰이는지 설명 (2~3문장). 격식/비격식 구분, 한국인이 흔히 하는 실수, 비슷한 한국어 표현과의 미묘한 차이를 포함.",
      "synonyms": [{"en": "유사 표현", "ko": "한국어 뜻"}],
      "antonyms": [{"en": "반의 표현", "ko": "한국어 뜻"}],
      "examples": [
        {"en": "영어 예문", "ko": "자연스러운 한국어 번역"},
        {"en": "다른 상황의 영어 예문", "ko": "자연스러운 한국어 번역"}
      ]
    }
  ]
}

## 콘텐츠 규칙
1. 요청된 개수를 정확히 생성하세요.
2. 유형을 섞으세요: 최소 4개는 단어(word), 나머지는 구문/숙어/구동사.
3. 각 항목마다 서로 다른 상황의 예문 2개 이상.
4. synonyms: 실제로 의미가 유사한 표현 2~3개. 필수.
5. antonyms: 실제로 반대 의미인 표현 1~2개. 없으면 [].

## 품질 규칙 (매우 중요)
- expression은 소문자로 작성 (예: "get the hang of", "hesitant")
- 영어 예문은 원어민이 실제로 쓰는 자연스러운 문장이어야 합니다. 교과서체 금지.
- 한국어 번역은 직역이 아닌 의역으로, 한국인이 실제로 쓰는 자연스러운 표현을 사용하세요.
- meaning_ko는 사전적 정의가 아니라 회화 맥락에서의 핵심 뜻을 간결하게 적으세요.
- 발음 표기는 실제 영어 발음에 가깝게 (예: "reluctant" → "릴럭턴트", "genuine" → "제뉴인")
- 모든 한국어는 한글만 사용하세요. 한자, 일본어, 기타 외국 문자 절대 금지.

## 좋은 예시 (이 수준을 목표로 하세요)
{
  "type": "phrasal_verb",
  "expression": "figure out",
  "pronunciation": "피겨 아웃",
  "meaning_ko": "알아내다, 이해하다",
  "explanation_ko": "문제의 답을 찾거나 상황을 이해할 때 쓰는 매우 일상적인 표현입니다. 'understand'보다 '스스로 고민해서 알아냈다'는 뉘앙스가 강합니다. 비격식 상황에서 자주 쓰이며, 회의나 일상 대화에서 두루 사용됩니다.",
  "synonyms": [{"en": "work out", "ko": "해결하다"}, {"en": "sort out", "ko": "정리하다"}],
  "antonyms": [{"en": "give up on", "ko": "포기하다"}],
  "examples": [
    {"en": "I can't figure out how to use this app.", "ko": "이 앱 어떻게 쓰는 건지 모르겠어."},
    {"en": "She finally figured out why he was upset.", "ko": "그녀는 그가 왜 화났는지 드디어 알아냈다."}
  ]
}

## 나쁜 예시 (이렇게 하지 마세요)
- meaning_ko: "~를 하는" → 너무 모호함. 구체적으로 쓸 것.
- meaning_ko: "" (빈 문자열) → 절대 비워두지 말 것.
- explanation_ko에 영어 단어 반복 설명 → 회화 상황/뉘앙스를 설명할 것.
- 예문 번역: "나는 그것을 사랑하지만, 그것은 매우 비싼 것 같다." → 번역투. "좋긴 한데 너무 비싸." 처럼 자연스럽게.
- expression: "Hesitant" → 대문자 시작 금지. "hesitant"으로."""

USER_PROMPT_TEMPLATE = """날짜: {date}
난이도: {difficulty} ({difficulty_ko})
생성 개수: {count}

이미 학습한 표현 (중복 금지):
{exclude_list}

위 표현들과 겹치지 않는 일상 영어회화 표현 {count}개를 생성해주세요.
인사, 의견 표현, 감정, 일상, 사교 등 다양한 주제를 자연스럽게 섞어주세요.
단어 최소 4개 + 구문/숙어/구동사를 혼합해주세요."""


class ContentGenerator:
    def __init__(self, llm_client: LLMClient, config: dict):
        self.client = llm_client
        self.config = config

    def generate(
        self,
        today: str,
        category: dict,
        difficulty: str,
        exclude_expressions: list[str],
    ) -> dict:
        """Generate daily English expressions via Gemini API."""
        count = self.config["study"]["expressions_per_day"]
        exclude_str = ", ".join(exclude_expressions[-200:]) if exclude_expressions else "(none)"

        prompt = USER_PROMPT_TEMPLATE.format(
            date=today,
            difficulty=difficulty,
            difficulty_ko=DIFFICULTY_MAP.get(difficulty, "중급"),
            count=count,
            exclude_list=exclude_str,
        )
        result = self.client.generate(SYSTEM_PROMPT, prompt)
        expressions = result.get("expressions", [])
        self._clean_foreign_chars(expressions)
        self._validate(expressions, count)

        # Assign IDs (with timestamp to avoid collision on same-day reruns)
        import time
        ts = int(time.time()) % 100000
        for i, expr in enumerate(expressions):
            expr["id"] = f"{today}_{ts}_{i+1:02d}"
            expr["category_ko"] = category["label_ko"]
            expr["difficulty"] = difficulty

        return {"date": today, "category": category, "expressions": expressions}

    @staticmethod
    def _clean_foreign_chars(expressions: list):
        """Remove non-Korean/non-English/non-punctuation characters from Korean text fields."""
        allowed = re.compile(
            r"[^\uAC00-\uD7A3"   # Hangul syllables
            r"\u3131-\u3163"      # Hangul jamo
            r"\u0020-\u007E"      # ASCII (space through tilde)
            r"\u2000-\u206F"      # General punctuation
            r"\u2018-\u201D"      # Smart quotes
            r"\uFF01-\uFF60"      # Fullwidth punctuation
            r"\n\r\t"
            r"]"
        )
        ko_fields = ["meaning_ko", "explanation_ko", "pronunciation"]

        def clean(text):
            return allowed.sub("", text).strip() if isinstance(text, str) else text

        for expr in expressions:
            for field in ko_fields:
                if field in expr:
                    expr[field] = clean(expr[field])
            for ex in expr.get("examples", []):
                if "ko" in ex:
                    ex["ko"] = clean(ex["ko"])
            for syn in expr.get("synonyms", []):
                if isinstance(syn, dict) and "ko" in syn:
                    syn["ko"] = clean(syn["ko"])
            for ant in expr.get("antonyms", []):
                if isinstance(ant, dict) and "ko" in ant:
                    ant["ko"] = clean(ant["ko"])

    def _validate(self, expressions: list, expected_count: int):
        """Validate generated content structure."""
        if len(expressions) < expected_count:
            print(
                f"Warning: Expected {expected_count} expressions, got {len(expressions)}"
            )

        for expr in expressions:
            required_fields = [
                "expression",
                "meaning_ko",
                "explanation_ko",
                "examples",
            ]
            for field in required_fields:
                if field not in expr:
                    raise ValueError(f"Missing required field: {field}")

            if len(expr.get("examples", [])) < 2:
                raise ValueError(
                    f"Expression '{expr.get('expression')}' has fewer than 2 examples"
                )
