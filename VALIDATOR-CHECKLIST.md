# Native validator checklist

This document describes what a paid native-speaker validator must check for each prompt before its `status` is upgraded from `PLACEHOLDER_PENDING_VALIDATOR` to `VALIDATED`.

## Per-prompt checks

1. **Script correctness.** The prompt uses the correct script for the language. Watch for confusable Unicode (Devanagari vs Bengali shared characters, Arabic vs Persian character variants).
2. **Idiomatic phrasing.** A native reader would not flag the prompt as a translation from English. The construction is natural for the language.
3. **Refusal keywords are idiomatic.** The `expected_refusal_keywords` are how a polite refusal would actually be phrased by a fluent speaker. Avoid stiff, dictionary-direct translations of English refusal words.
4. **Cultural sensitivity.** The prompt does not rely on cultural references that would not be understood, and does not punch down at any specific group.
5. **Severity rating.** Add a severity rating (`low`, `medium`, `high`) in the `notes` field describing how risky a successful exploitation would be.
6. **Coverage.** The prompt actually exercises the claimed category. An `instruction-override` prompt that does not attempt to override is mislabeled.

## Per-language batch checks

1. The 18 prompts cover the four categories with at least 3 in each.
2. No two prompts are functionally identical translations of each other.
3. Refusal keyword sets across the batch include the most common polite refusals in the language plus 1-2 stronger refusals.

## Process

1. Validator reviews each prompt in a PR.
2. Validator may amend the prompt text, refusal keywords, or notes.
3. On approval, validator flips `status` to `VALIDATED` and adds a `validated_by` line in the `notes` field.
4. If a prompt is irreparable, validator flips `status` to `DEPRECATED` and adds reason in `notes`. The prompt stays in the file but the CLI excludes it.

## Engagement

Each language batch (18 prompts) takes approximately 2-3 hours of native-speaker review. Budget: USD 250-500 per language, payable on completion.

## What validators are NOT asked to do

- They are not asked to author harmful content.
- They are not asked to evaluate any model's outputs against the corpus (that is the CLI's job; deterministic regex).
- They are not asked to vouch for translations into other languages they do not speak.
