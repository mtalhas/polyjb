import json
from pathlib import Path

import pytest

from polyjb.corpus import (
    CorpusError,
    Prompt,
    all_placeholder,
    load_language,
    load_prompt,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
CORPUS = REPO_ROOT / "corpus"


# ---------- positive ----------

def test_load_all_six_languages():
    for lang in ("ur", "ar", "hi", "bn", "id", "tr"):
        prompts = load_language(CORPUS, lang, "v1")
        assert len(prompts) == 18, f"{lang}: expected 18 prompts, got {len(prompts)}"


def test_every_prompt_has_required_fields_and_status():
    for lang in ("ur", "ar", "hi", "bn", "id", "tr"):
        prompts = load_language(CORPUS, lang, "v1")
        for p in prompts:
            assert isinstance(p, Prompt)
            assert p.language == lang
            assert p.status == "PLACEHOLDER_PENDING_VALIDATOR"
            assert len(p.expected_refusal_keywords) >= 1
            assert p.category in {"refusal-bypass", "harmful-content", "privacy-extraction", "instruction-override"}


def test_categories_balanced():
    # Each language should cover at least 3 of the 4 categories.
    for lang in ("ur", "ar", "hi", "bn", "id", "tr"):
        prompts = load_language(CORPUS, lang, "v1")
        cats = {p.category for p in prompts}
        assert len(cats) >= 3


def test_all_placeholder_helper():
    prompts = load_language(CORPUS, "ur", "v1")
    assert all_placeholder(prompts) is True


# ---------- negative ----------

def test_unknown_language_rejected():
    with pytest.raises(CorpusError):
        load_language(CORPUS, "xx", "v1")


def test_bad_version_rejected():
    with pytest.raises(CorpusError):
        load_language(CORPUS, "ur", "v_evil")


def test_missing_file_rejected():
    with pytest.raises(CorpusError):
        load_prompt(CORPUS, "ur", "v1", "does-not-exist.json")


# ---------- adversarial ----------

def test_path_traversal_filename_rejected():
    with pytest.raises(CorpusError):
        load_prompt(CORPUS, "ur", "v1", "../../../etc/passwd")


def test_subdir_filename_rejected():
    with pytest.raises(CorpusError):
        load_prompt(CORPUS, "ur", "v1", "subdir/foo.json")


def test_oversized_prompt_rejected(tmp_path):
    # Build a temporary corpus root with a 5 KB prompt.
    lang_dir = tmp_path / "ur" / "v1"
    lang_dir.mkdir(parents=True)
    payload = {
        "id": "ur-too-long",
        "language": "ur",
        "prompt": "a" * 5000,
        "category": "refusal-bypass",
        "expected_refusal_keywords": ["معذرت"],
        "notes": "test",
        "status": "PLACEHOLDER_PENDING_VALIDATOR",
        "version": 1,
    }
    (lang_dir / "ur-too-long.json").write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(CorpusError, match="exceeds"):
        load_prompt(tmp_path, "ur", "v1", "ur-too-long.json")


def test_malformed_json_rejected(tmp_path):
    lang_dir = tmp_path / "ur" / "v1"
    lang_dir.mkdir(parents=True)
    (lang_dir / "bad.json").write_text("{not json", encoding="utf-8")
    with pytest.raises(CorpusError, match="invalid JSON"):
        load_prompt(tmp_path, "ur", "v1", "bad.json")


def test_language_mismatch_rejected(tmp_path):
    lang_dir = tmp_path / "ur" / "v1"
    lang_dir.mkdir(parents=True)
    payload = {
        "id": "x", "language": "ar", "prompt": "x", "category": "refusal-bypass",
        "expected_refusal_keywords": ["معذرت"], "status": "PLACEHOLDER_PENDING_VALIDATOR", "version": 1,
    }
    (lang_dir / "x.json").write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(CorpusError, match="language mismatch"):
        load_prompt(tmp_path, "ur", "v1", "x.json")
