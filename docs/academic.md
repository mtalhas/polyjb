# Academic citation

Once v1 prompts have been validated by paid native speakers, a versioned snapshot will be archived on Zenodo with a DOI. Until then, please cite the repository commit SHA.

## BibTeX template (placeholder)

```bibtex
@misc{polyjb_v1_placeholder,
  author       = {Siddiqui, Talha},
  title        = {{PolyJB}: A Multilingual Prompt-Injection Corpus and Deterministic Evaluator (v1 PLACEHOLDER)},
  year         = {2026},
  howpublished = {\url{https://github.com/mtalhas/polyjb}},
  note         = {Pre-validation; do not cite as authoritative}
}
```

## Once validated and archived (template)

```bibtex
@dataset{polyjb_v1,
  author       = {Siddiqui, Talha and {Native Validator Cohort}},
  title        = {{PolyJB} v1: Multilingual Prompt Injection Corpus and Evaluator},
  year         = {2026},
  publisher    = {Zenodo},
  doi          = {<TO BE ASSIGNED>},
  url          = {https://doi.org/<TO BE ASSIGNED>}
}
```

## Related work this corpus tries to complement

- English-first safety benchmarks (HarmBench, AdvBench, JailbreakBench).
- Multilingual translation studies of safety datasets.
- "Low-resource language" jailbreak findings.

A short positioning note will be added once v1 is validated. The thesis is straightforward: refusal-rate measurements that report a single number ignore that the number changes substantially across languages, and the across-language gap is itself the safety signal worth reporting.
