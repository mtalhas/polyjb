"""Result aggregation and pretty-print."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from polyjb.corpus import Prompt
from polyjb.evaluator import EvalResult


@dataclass(frozen=True)
class RunRow:
    prompt_id: str
    language: str
    category: str
    status: str
    refused: bool
    matched_keywords: tuple[str, ...]
    response_excerpt: str


@dataclass(frozen=True)
class RunResult:
    provider: str
    model: str
    corpus_version: str
    rows: tuple[RunRow, ...]

    @property
    def refusal_rate(self) -> float:
        if not self.rows:
            return 0.0
        return sum(1 for r in self.rows if r.refused) / len(self.rows)

    def to_dict(self) -> dict:
        return {
            "provider": self.provider,
            "model": self.model,
            "corpus_version": self.corpus_version,
            "refusal_rate": self.refusal_rate,
            "rows": [asdict(r) for r in self.rows],
        }


def write_json(result: RunResult, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")


def build_row(prompt: Prompt, ev: EvalResult, response: str) -> RunRow:
    return RunRow(
        prompt_id=prompt.id,
        language=prompt.language,
        category=prompt.category,
        status=prompt.status,
        refused=ev.refused,
        matched_keywords=ev.matched_keywords,
        response_excerpt=response[:200],
    )
