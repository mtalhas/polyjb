"""Anthropic provider wrapper. Not exercised during the build session."""

from __future__ import annotations

import os

from polyjb.providers.base import Provider, ProviderResponse


class AnthropicProvider(Provider):
    name = "anthropic"

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")

    def complete(self, prompt: str, *, model: str, timeout_s: float = 60.0) -> ProviderResponse:
        if not self.api_key:
            raise NotImplementedError("Set ANTHROPIC_API_KEY before running.")
        try:
            from anthropic import Anthropic
        except ImportError as e:
            raise NotImplementedError("Install the 'anthropic' extra: pip install -e '.[anthropic]'") from e
        client = Anthropic(api_key=self.api_key)
        resp = client.messages.create(model=model, max_tokens=1024, messages=[{"role": "user", "content": prompt}])
        text = "".join(block.text for block in resp.content if getattr(block, "type", None) == "text")
        return ProviderResponse(text=text, model=model, raw=resp)
