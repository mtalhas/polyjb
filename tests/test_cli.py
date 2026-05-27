"""CLI smoke tests using click's testing harness.

The provider is intentionally not invoked: the tests stop at the placeholder
guard or use --include-placeholder against a missing API key (NotImplementedError).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from polyjb.cli import main

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_list_languages_shows_six_codes():
    runner = CliRunner()
    result = runner.invoke(main, ["list-languages"])
    assert result.exit_code == 0
    assert {"ur", "ar", "hi", "bn", "id", "tr"} <= set(result.output.split())


def test_run_refuses_to_aggregate_placeholders_by_default():
    runner = CliRunner()
    result = runner.invoke(main, [
        "run", "--provider", "openai", "--model", "gpt-4o",
        "--lang", "ur",
        "--corpus-root", str(REPO_ROOT / "corpus")
    ])
    assert result.exit_code != 0
    assert "PLACEHOLDER" in result.output


def test_run_with_placeholder_flag_calls_provider_and_fails_loud_without_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    runner = CliRunner()
    result = runner.invoke(main, [
        "run", "--provider", "openai", "--model", "gpt-4o",
        "--lang", "ur",
        "--include-placeholder",
        "--corpus-root", str(REPO_ROOT / "corpus")
    ])
    assert result.exit_code != 0
    assert "OPENAI_API_KEY" in result.output


def test_compare_aggregates_two_run_jsons(tmp_path: Path):
    payload = {
        "provider": "openai", "model": "gpt-4o", "corpus_version": "v1",
        "rows": [
            {"prompt_id": "ur-1", "language": "ur", "category": "refusal-bypass", "status": "VALIDATED", "refused": True, "matched_keywords": ["معذرت"], "response_excerpt": "..."},
            {"prompt_id": "ur-2", "language": "ur", "category": "harmful-content", "status": "VALIDATED", "refused": False, "matched_keywords": [], "response_excerpt": "..."}
        ]
    }
    a = tmp_path / "a.json"; a.write_text(json.dumps(payload), encoding="utf-8")
    b = tmp_path / "b.json"; b.write_text(json.dumps(payload), encoding="utf-8")

    runner = CliRunner()
    result = runner.invoke(main, ["compare", str(a), str(b)])
    assert result.exit_code == 0
    assert "polyjb compare" in result.output


def test_unknown_provider_rejected():
    runner = CliRunner()
    result = runner.invoke(main, [
        "run", "--provider", "totally-fake", "--model", "x",
        "--lang", "ur", "--include-placeholder",
        "--corpus-root", str(REPO_ROOT / "corpus")
    ])
    assert result.exit_code != 0
    assert "unknown provider" in result.output
