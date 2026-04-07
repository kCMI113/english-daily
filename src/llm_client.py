import os
import json
import time

from google import genai
from google.genai import types


class LLMClient:
    def __init__(self, config: dict):
        self.config = config
        llm_cfg = config["llm"]
        self.client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        self.model = llm_cfg["model"]
        self.temperature = llm_cfg["temperature"]
        self.max_tokens = llm_cfg["max_tokens"]

    def generate(self, system_prompt: str, user_prompt: str) -> dict:
        """Generate JSON response from Gemini API with retry."""
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
                return json.loads(response.text)
            except json.JSONDecodeError:
                if attempt < 2:
                    time.sleep(2 ** attempt)
                    continue
                raise
            except Exception as e:
                if attempt < 2:
                    time.sleep(2 ** attempt)
                    continue
                raise RuntimeError(f"Gemini API failed after 3 attempts: {e}")

        raise RuntimeError("All retries exhausted")
