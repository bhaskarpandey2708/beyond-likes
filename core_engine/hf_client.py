"""
Zero-Dependency Hugging Face Inference API Client
Allows seamless inference against Hugging Face hosted foundation models with graceful local fallback.
"""
import urllib.request
import urllib.parse
import json
import os
import time
from typing import Dict, Any, Optional

DEFAULT_HF_MODEL = os.environ.get("HF_MODEL_NAME", "Qwen/Qwen2.5-7B-Instruct")
HF_API_KEY = os.environ.get("HF_API_KEY", "")

class HuggingFaceDiscourseClient:
    """
    Connects to Hugging Face Inference API / Serverless Router for deep neural discourse analysis.
    """

    def __init__(self, model_name: str = DEFAULT_HF_MODEL, api_key: Optional[str] = None):
        self.model_name = model_name
        self.api_key = api_key or HF_API_KEY
        self.base_url = f"https://api-inference.huggingface.co/models/{self.model_name}"

    def is_available(self) -> bool:
        return bool(self.api_key)

    def evaluate_neural(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Sends prompt to Hugging Face Serverless Inference API and parses structured discourse metrics.
        Returns None if API key is not configured or network request fails.
        """
        if not self.api_key:
            return None

        prompt = (
            f"Analyze the following user comment for discourse quality.\n"
            f"Comment: \"{text}\"\n\n"
            f"Output strictly valid JSON with keys: constructiveness (0-100), civility (0-100), "
            f"persuasiveness (0-100), relevance (0-100), suggested_revision (string)."
        )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 200,
                "temperature": 0.2,
                "return_full_text": False
            }
        }

        req = urllib.request.Request(
            self.base_url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=10.0) as resp:
                raw = resp.read().decode("utf-8")
                data = json.loads(raw)
                # Hugging Face text generation returns a list with generated_text
                if isinstance(data, list) and len(data) > 0:
                    gen_text = data[0].get("generated_text", "")
                    # Extract JSON block
                    start = gen_text.find("{")
                    end = gen_text.rfind("}")
                    if start != -1 and end != -1:
                        parsed = json.loads(gen_text[start:end+1])
                        return parsed
        except Exception as e:
            # Fall back silently to local engine
            pass
        return None
