"""Corpus loading and validation.

Strict path validation prevents corpus poisoning via path traversal or
overly long filenames. Prompt content is capped at 4 KB.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ALLOWED_FILENAME = re.compile(r"^[a-z0-9_-]+\.json$")
ALLOWED_CATEGORIES = {"refusal-bypass", "harmful-content", "privacy-extraction", "instruction-override"}
ALLOWED_LANGS = {"ur", "ar", "hi", "bn", "id", "tr"}
ALLOWED_STATUSES = {"PLACEHOLDER_PENDING_VALIDATOR", "VALIDATED", "DEPRECATED"}
MAX_PROMPT_BYTES = 4096


@dataclass(frozen=True)
class Prompt:
    id: str
    language: str
    prompt: str
    category: str
    expected_refusal_keywords: tuple[str, ...]
    notes: str
    status: str
    version: int

    @property
    def is_placeholder(self) -> bool:
        return self.status == "PLACEHOLDER_PENDING_VALIDATOR"


class CorpusError(Exception):
    """Raised when corpus loading fails for any reason."""


def _validate_path(corpus_root: Path, lang: str, version: str, filename: str) -> Path:
    if lang not in ALLOWED_LANGS:
        raise CorpusError(f"unknown language code: {lang!r}")
    if not re.fullmatch(r"v[0-9]+", version):
        raise CorpusError(f"invalid version dir: {version!r}")
    if not ALLOWED_FILENAME.fullmatch(filename):
        raise CorpusError(f"invalid filename (path traversal blocked): {filename!r}")

    corpus_root = corpus_root.resolve()
    target = (corpus_root / lang / version / filename).resolve()
    # Ensure the resolved path is under corpus_root.
    if corpus_root not in target.parents:
        raise CorpusError(f"resolved path escapes corpus root: {target}")
    return target


def load_prompt(corpus_root: Path, lang: str, version: str, filename: str) -> Prompt:
    path = _validate_path(corpus_root, lang, version, filename)
    if not path.is_file():
        raise CorpusError(f"prompt file not found: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise CorpusError(f"{path}: invalid JSON: {e.lineno}:{e.colno}: {e.msg}") from e

    if not isinstance(data, dict):
        raise CorpusError(f"{path}: expected an object")
    for field in ("id", "language", "prompt", "category", "expected_refusal_keywords", "status", "version"):
        if field not in data:
            raise CorpusError(f"{path}: missing required field {field!r}")
    if data["language"] != lang:
        raise CorpusError(f"{path}: language mismatch (file at {lang!r}, payload says {data['language']!r})")
    if data["category"] not in ALLOWED_CATEGORIES:
        raise CorpusError(f"{path}: category must be one of {sorted(ALLOWED_CATEGORIES)}")
    if data["status"] not in ALLOWED_STATUSES:
        raise CorpusError(f"{path}: status must be one of {sorted(ALLOWED_STATUSES)}")
    if not isinstance(data["prompt"], str):
        raise CorpusError(f"{path}: prompt must be a string")
    if len(data["prompt"].encode("utf-8")) > MAX_PROMPT_BYTES:
        raise CorpusError(f"{path}: prompt exceeds {MAX_PROMPT_BYTES} bytes")
    keywords = data["expected_refusal_keywords"]
    if not isinstance(keywords, list) or not all(isinstance(k, str) for k in keywords):
        raise CorpusError(f"{path}: expected_refusal_keywords must be a list of strings")
    if not 1 <= len(keywords) <= 10:
        raise CorpusError(f"{path}: expected_refusal_keywords must have 1-10 entries")

    return Prompt(
        id=data["id"],
        language=data["language"],
        prompt=data["prompt"],
        category=data["category"],
        expected_refusal_keywords=tuple(keywords),
        notes=data.get("notes", ""),
        status=data["status"],
        version=int(data["version"]),
    )


def load_language(corpus_root: Path, lang: str, version: str = "v1") -> list[Prompt]:
    if lang not in ALLOWED_LANGS:
        raise CorpusError(f"unknown language code: {lang!r}")
    if not re.fullmatch(r"v[0-9]+", version):
        raise CorpusError(f"invalid version dir: {version!r}")
    lang_dir = (corpus_root.resolve() / lang / version)
    if not lang_dir.is_dir():
        raise CorpusError(f"language directory not found: {lang_dir}")
    out: list[Prompt] = []
    for child in sorted(lang_dir.iterdir()):
        # _validate_path will reject anything not matching ALLOWED_FILENAME (subdirs, weird names).
        if not child.is_file() or not ALLOWED_FILENAME.fullmatch(child.name):
            continue
        out.append(load_prompt(corpus_root, lang, version, child.name))
    return out


def all_placeholder(prompts: Iterable[Prompt]) -> bool:
    return all(p.is_placeholder for p in prompts)
