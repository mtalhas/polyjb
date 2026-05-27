"""Abstract Provider."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderResponse:
    text: str
    model: str
    raw: object = None


class Provider(ABC):
    """Each provider returns a string response for a prompt.

    Concrete provider subclasses live in the optional-extras modules.
    They raise NotImplementedError until the operator wires their API key.
    """

    name: str

    @abstractmethod
    def complete(self, prompt: str, *, model: str, timeout_s: float = 60.0) -> ProviderResponse:
        ...
