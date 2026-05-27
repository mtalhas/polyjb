# PolyJB

> **v1 PLACEHOLDER status.** The corpus in this repo has NOT yet been validated by native speakers of the listed languages. Do not cite as authoritative. Validator engagement is funded and scheduled; see `VALIDATOR-CHECKLIST.md`.

PolyJB is a multilingual prompt-injection / refusal-bypass evaluation corpus and a deterministic CLI evaluator. It targets six languages that are systematically under-represented in current LLM safety benchmarks: Urdu, Arabic, Hindi, Bengali, Indonesian, and Turkish.

## Why this exists

Most published safety evaluations are English-first. A growing body of research shows that LLM guardrails are less robust in non-English contexts. Native-speaker authored evaluation corpora in these languages are scarce, and the few that exist often translate English prompts mechanically rather than constructing prompts that exploit each language's idiomatic structure.

The author (Talha Siddiqui) is a native Urdu speaker. Native-speaker access to South Asian languages is the project's "unfair advantage" in the academic sense: harder for outsiders to staff equivalent coverage. The v1 corpus in this repo is authored as a PLACEHOLDER and is gated behind validator review by paid native speakers before any results are claimed as authoritative.

## Architectural rule

The evaluator is **deterministic**. It checks whether a model's response matches a per-language `expected_refusal_keywords` set via regex match. No LLM is used as a judge. The CLI is a harness; the corpus is data; the score is arithmetic.

## Layout

```
corpus/
  SCHEMA.md                  prompt JSON schema
  urdu/v1/                   18 prompts, PLACEHOLDER
  arabic/v1/                 18 prompts, PLACEHOLDER
  hindi/v1/                  18 prompts, PLACEHOLDER
  bengali/v1/                18 prompts, PLACEHOLDER
  indonesian/v1/             18 prompts, PLACEHOLDER
  turkish/v1/                18 prompts, PLACEHOLDER
VALIDATOR-CHECKLIST.md       what native validators must check
src/polyjb/                  Python CLI (run, compare)
tests/                       unit + adversarial tests
docs/example-run.md          example run output
docs/academic.md             citation template, BibTeX
```

## Install

```bash
pip install -e ".[dev,openai,anthropic]"
```

## CLI

```bash
# (paid provider API needed; not run during the build session)
polyjb run --provider openai --model gpt-4o --lang urdu --corpus v1
polyjb compare --results runs/*.json
```

By default, `polyjb compare` refuses to aggregate placeholder prompts. Pass `--include-placeholder` to override (only for dry-run smoke tests).

## Status of v1 corpus

| Language | v1 prompts | Native validator | Authoritative? |
| --- | --- | --- | --- |
| Urdu | 18 | pending | no |
| Arabic | 18 | pending | no |
| Hindi | 18 | pending | no |
| Bengali | 18 | pending | no |
| Indonesian | 18 | pending | no |
| Turkish | 18 | pending | no |

Validator engagement budget: USD 250-500 per language, to be funded by Talha Siddiqui when v1 reaches stable shape.

## Citing

This corpus is pre-publication. A versioned, DOI-assigned snapshot will land on Zenodo once v1 passes validator review. Until then, please cite this repository's commit SHA. See `docs/academic.md` for a BibTeX template.

## License

MIT. See `LICENSE`.

## Not for misuse

The corpus tests whether LLM safety systems refuse specific instruction-override patterns. The prompts are NOT recipes for harm. They are evaluation inputs. Use this corpus to make your model safer, not to make it less safe. By contributing or evaluating, you agree to use the corpus only for safety research, red-teaming, and academic study.

## Contributing

See `CONTRIBUTING.md`. We especially welcome native speakers of any of the six languages.
