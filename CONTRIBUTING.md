# Contributing to PolyJB

Thanks for considering a contribution. The bar is high: this is a safety-research corpus, and quality is the load-bearing property.

## Quickstart

```bash
git clone https://github.com/mtalhas/polyjb
cd polyjb
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
```

## What we want

- Native-speaker validation of v1 prompts (Urdu, Arabic, Hindi, Bengali, Indonesian, Turkish). See `VALIDATOR-CHECKLIST.md`.
- New prompt categories that test culturally specific refusal patterns.
- Provider wrapper improvements in `src/polyjb/providers/`.
- Documentation, especially in the target languages.

## What we do NOT want

- Mechanical machine translations of English prompts. We are explicitly building a corpus that is idiomatic in each target language.
- Prompts that contain or solicit actually harmful content (the prompts test refusal patterns, not the harm itself).
- LLM-as-judge code. The evaluator stays deterministic.

## Adding a prompt

1. Pick a language and create a JSON file under `corpus/<lang>/v1/<id>.json` matching `corpus/SCHEMA.md`.
2. Set `"status": "PLACEHOLDER_PENDING_VALIDATOR"` until a native validator approves it.
3. Run `pytest tests/test_corpus.py -v` to ensure the schema validator accepts your file.
4. Open a PR. Validators may request changes for idiomatic phrasing.

## Adversarial inputs (security)

Corpus files are loaded with strict path validation. Filenames must match `^[a-z0-9_-]+\.json$` and must live inside the language directory. Path traversal attempts are rejected by `polyjb.corpus.load`.

## Code style

- Python 3.11+, type-annotated.
- `ruff check` and `pytest` must pass before opening a PR.
- No new runtime dependencies without a comment explaining why.

## Code of conduct

See `CODE_OF_CONDUCT.md`. We use the Contributor Covenant 2.1.
