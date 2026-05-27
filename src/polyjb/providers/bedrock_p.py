"""AWS Bedrock provider wrapper. Not exercised during the build session."""

from __future__ import annotations

import json

from polyjb.providers.base import Provider, ProviderResponse


class BedrockProvider(Provider):
    name = "bedrock"

    def __init__(self, region: str | None = None) -> None:
        self.region = region

    def complete(self, prompt: str, *, model: str, timeout_s: float = 60.0) -> ProviderResponse:
        try:
            import boto3
        except ImportError as e:
            raise NotImplementedError("Install the 'bedrock' extra: pip install -e '.[bedrock]'") from e
        client = boto3.client("bedrock-runtime", region_name=self.region)
        # Caller is expected to wire model-specific request shapes; this is a thin shim.
        body = json.dumps({"prompt": prompt}).encode("utf-8")
        resp = client.invoke_model(modelId=model, body=body)
        payload = json.loads(resp["body"].read())
        text = payload.get("completion") or payload.get("outputText") or ""
        return ProviderResponse(text=text, model=model, raw=payload)
