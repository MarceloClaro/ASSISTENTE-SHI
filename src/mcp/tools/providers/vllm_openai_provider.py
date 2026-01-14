"""OpenAI-compatible Vision Provider.

Implements an image analysis provider using OpenAI SDK with base_url to support
Zhipu, Alibaba (Qwen), OpenAI, or any OpenAI-compatible service.
"""
from __future__ import annotations
import logging
from typing import Dict, Any, Optional

import os
try:
    import openai  # type: ignore
except Exception:  # pragma: no cover
    # Defer import errors for environments without openai installed
    openai = None

logger = logging.getLogger(__name__)


def _env(value: Optional[str], default: str = "") -> str:
    if not value:
        return default
    if value.startswith("${") and value.endswith("}"):
        key = value[2:-1]
        return os.getenv(key, default)
    return value


class OpenAICompatibleVisionProvider:
    def __init__(self, config: Dict[str, Any]):
        self.api_key = _env(
            config.get("api_key"), os.getenv("ZHIPU_API_KEY", "")
        )
        self.model = config.get("model", "glm-4v-flash")
        self.base_url = config.get(
            "base_url", "https://open.bigmodel.cn/api/paas/v4"
        )
        self.max_tokens = int(config.get("max_tokens", 2048))
        self.temperature = float(config.get("temperature", 0.7))

        if openai is None:
            raise RuntimeError(
                "openai package not available. Please install 'openai>=1.0.0'."
            )

        self.client = openai.OpenAI(
            api_key=self.api_key, base_url=self.base_url
        )
        logger.info(
            f"[Vision] OpenAI-compatible provider initialized: "
            f"model={self.model} base_url={self.base_url}"
        )

    def analyze_image(
        self,
        image_base64: str,
        question: str,
        context: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not image_base64:
            raise ValueError("image_base64 is required")
        if not question:
            question = "Descreva detalhadamente tudo que você vê nesta imagem."

        content = [
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image_base64}"
                }
            },
            {
                "type": "text",
                "text": question
            },
        ]
        if context:
            content.append({
                "type": "text",
                "text": f"\n\nContexto adicional: {context}"
            })

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": content}],
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            stream=False,
        )

        analysis = response.choices[0].message.content
        usage = getattr(response, "usage", None)
        tokens = {
            "input": getattr(usage, "prompt_tokens", None),
            "output": getattr(usage, "completion_tokens", None),
            "total": getattr(usage, "total_tokens", None),
        } if usage else None

        return {
            "status": "success",
            "analysis": analysis,
            "model": self.model,
            "tokens": tokens,
        }
