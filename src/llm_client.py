import os
import json
import re
import time

from google import genai
from google.genai import types


class LLMClient:
    def __init__(self, config: dict):
        self.config = config
        llm_cfg = config["llm"]
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY environment variable is not set")
        self.client = genai.Client(api_key=api_key)
        self.model = llm_cfg["model"]
        self.temperature = llm_cfg["temperature"]
        self.max_tokens = llm_cfg["max_tokens"]

    def generate(self, system_prompt: str, user_prompt: str) -> dict:
        """Generate JSON response from Gemini API with retry."""
        last_error = None
        for attempt in range(3):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt,
                        temperature=self.temperature,
                        max_output_tokens=self.max_tokens,
                        response_mime_type="application/json",
                    ),
                )
                return self._parse_json(response.text)
            except (json.JSONDecodeError, ValueError) as e:
                last_error = e
                print(f"JSON parse error (attempt {attempt + 1}/3): {e}")
                if attempt < 2:
                    time.sleep(2 ** attempt)
                    continue
            except Exception as e:
                last_error = e
                print(f"API error (attempt {attempt + 1}/3): {e}")
                if attempt < 2:
                    time.sleep(2 ** attempt)
                    continue

        raise RuntimeError(f"Gemini API failed after 3 attempts: {last_error}")

    @staticmethod
    def _parse_json(text: str) -> dict:
        """Parse JSON with multiple fallback strategies."""
        # 1. Direct parse
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # 2. Extract first complete JSON object (handles extra data)
        try:
            depth = 0
            start = text.index('{')
            for i, ch in enumerate(text[start:], start):
                if ch == '{':
                    depth += 1
                elif ch == '}':
                    depth -= 1
                    if depth == 0:
                        return json.loads(text[start:i + 1])
        except (ValueError, json.JSONDecodeError):
            pass

        # 3. Strip markdown fences (```json ... ```)
        try:
            cleaned = re.sub(r'```(?:json)?\s*', '', text).strip()
            cleaned = re.sub(r'```\s*$', '', cleaned).strip()
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass

        # 4. Fix truncated JSON (missing closing brackets)
        try:
            fixed = text.rstrip()
            open_braces = fixed.count('{') - fixed.count('}')
            open_brackets = fixed.count('[') - fixed.count(']')
            fixed += ']' * open_brackets + '}' * open_braces
            return json.loads(fixed)
        except json.JSONDecodeError:
            pass

        raise json.JSONDecodeError("All JSON parse strategies failed", text, 0)
