import os
import time
import json
import yaml

from groq import Groq


def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "..", "config.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


class GroqClient:
    def __init__(self, config=None):
        self.config = config or load_config()
        groq_cfg = self.config["groq"]
        self.client = Groq(api_key=os.environ["GROQ_API_KEY"])
        self.model = groq_cfg["model"]
        self.fallback_model = groq_cfg["fallback_model"]
        self.temperature = groq_cfg["temperature"]
        self.max_tokens = groq_cfg["max_tokens"]

    def generate(self, system_prompt: str, user_prompt: str) -> dict:
        """Generate JSON response from Groq API with retry and fallback."""
        models = [self.model, self.fallback_model]

        for model in models:
            for attempt in range(3):
                try:
                    response = self.client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt},
                        ],
                        temperature=self.temperature,
                        max_tokens=self.max_tokens,
                        response_format={"type": "json_object"},
                    )
                    content = response.choices[0].message.content
                    return json.loads(content)
                except json.JSONDecodeError:
                    if attempt < 2:
                        time.sleep(2 ** attempt)
                        continue
                    # Fall through to next model
                    break
                except Exception as e:
                    if attempt < 2:
                        time.sleep(2 ** attempt)
                        continue
                    print(f"Model {model} failed after 3 attempts: {e}")
                    break

        raise RuntimeError("All models and retries exhausted")
