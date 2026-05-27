"""OpenAI provider wrapper. Not exercised during the build session."""

from __future__ import annotations

import os

from polyjb.providers.base import Provider, ProviderResponse


class OpenAIProvider(Provider):
    name = "openai"

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")

    def complete(self, prompt: str, *, model: str, timeout_s: float = 60.0) -> ProviderResponse:
        if not self.api_key:
            raise NotImplementedError("Set OPENAI_API_KEY before running. polyjb did not call any provider during this session.")
        try:
            from openai import OpenAI
        except ImportError as e:
            raise NotImplementedError("Install the 'openai' extra: pip install -e '.[openai]'") from e
        client = OpenAI(api_key=self.api_key, timeout=timeout_s)
        resp = client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}])
        text = resp.choices[0].message.content or ""
        return ProviderResponse(text=text, model=model, raw=resp)
