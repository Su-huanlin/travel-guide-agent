from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv
from openai import OpenAI


@dataclass
class LLMConfig:
    api_key: str
    base_url: str
    model: str
    temperature: float = 0.3
    max_tokens: int = 8192


def load_llm_config() -> LLMConfig:
    load_dotenv()
    api_key = os.getenv("TG_API_KEY") or os.getenv("OPENAI_API_KEY") or ""
    base_url = os.getenv("TG_BASE_URL") or os.getenv("OPENAI_BASE_URL") or "https://api.deepseek.com/v1"
    model = os.getenv("TG_MODEL") or os.getenv("OPENAI_MODEL") or "deepseek-chat"
    temperature = float(os.getenv("TG_TEMPERATURE", "0.3"))
    max_tokens = int(os.getenv("TG_MAX_TOKENS", "8192"))
    if not api_key:
        raise RuntimeError(
            "Missing TG_API_KEY (or OPENAI_API_KEY). Copy .env.example to .env and fill your key."
        )
    return LLMConfig(
        api_key=api_key,
        base_url=base_url.rstrip("/"),
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )


def make_client(config: LLMConfig | None = None) -> tuple[OpenAI, LLMConfig]:
    config = config or load_llm_config()
    client = OpenAI(api_key=config.api_key, base_url=config.base_url)
    return client, config


def chat(
    system: str,
    user: str,
    *,
    config: LLMConfig | None = None,
) -> str:
    """Single-turn chat using OpenAI-compatible Chat Completions API."""
    client, cfg = make_client(config)
    response = client.chat.completions.create(
        model=cfg.model,
        temperature=cfg.temperature,
        max_tokens=cfg.max_tokens,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    content = response.choices[0].message.content
    if not content:
        raise RuntimeError("Model returned empty content")
    return content.strip()
