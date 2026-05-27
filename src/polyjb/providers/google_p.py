"""Google Gemini provider wrapper. Not exercised during the build session."""

from __future__ import annotations

import os

from polyjb.providers.base import Provider, ProviderResponse


class GoogleProvider(Provider):
    name = "google"

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")

    def complete(self, prompt: str, *, model: str, timeout_s: float = 60.0) -> ProviderResponse:
        if not self.api_key:
            raise NotImplementedError("Set GOOGLE_API_KEY before running.")
        try:
            import google.generativeai as genai
        except ImportError as e:
            raise NotImplementedError("Install the 'google' extra: pip install -e '.[google]'") from e
        genai.configure(api_key=self.api_key)
        gmodel = genai.GenerativeModel(model)
        resp = gmodel.generate_content(prompt)
        return ProviderResponse(text=getattr(resp, "text", "") or "", model=model, raw=resp)
