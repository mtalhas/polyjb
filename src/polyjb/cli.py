"""CLI entrypoint."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from polyjb.corpus import all_placeholder, load_language
from polyjb.evaluator import evaluate
from polyjb.providers.base import Provider
from polyjb.report import RunResult, RunRow, build_row, write_json

console = Console()


def _resolve_provider(name: str) -> Provider:
    name = name.lower()
    if name == "openai":
        from polyjb.providers.openai_p import OpenAIProvider
        return OpenAIProvider()
    if name == "anthropic":
        from polyjb.providers.anthropic_p import AnthropicProvider
        return AnthropicProvider()
    if name == "google":
        from polyjb.providers.google_p import GoogleProvider
        return GoogleProvider()
    if name == "bedrock":
        from polyjb.providers.bedrock_p import BedrockProvider
        return BedrockProvider()
    raise click.UsageError(f"unknown provider {name!r}; supported: openai, anthropic, google, bedrock")


@click.group()
def main() -> None:
    """polyjb: multilingual prompt-injection corpus + deterministic evaluator."""


@main.command("list-languages")
def list_languages() -> None:
    """List supported language codes."""
    click.echo("ur ar hi bn id tr")


@main.command("run")
@click.option("--provider", required=True, help="openai | anthropic | google | bedrock")
@click.option("--model", required=True, help="model id specific to the chosen provider")
@click.option("--lang", required=True, type=click.Choice(["ur", "ar", "hi", "bn", "id", "tr"]))
@click.option("--corpus-version", "corpus_version", default="v1")
@click.option("--corpus-root", default="corpus", type=click.Path(file_okay=False, dir_okay=True, path_type=Path))
@click.option("--out", "out_path", default=None, type=click.Path(dir_okay=False, path_type=Path))
@click.option("--include-placeholder/--no-include-placeholder", default=False, help="allow PLACEHOLDER prompts to be evaluated")
def run_cmd(provider: str, model: str, lang: str, corpus_version: str, corpus_root: Path, out_path: Path | None, include_placeholder: bool) -> None:
    """Run the evaluator against a provider/model for a single language."""
    prompts = load_language(corpus_root, lang, corpus_version)
    if all_placeholder(prompts) and not include_placeholder:
        raise click.ClickException(
            "all prompts are PLACEHOLDER_PENDING_VALIDATOR. Pass --include-placeholder to run anyway (results are not authoritative)."
        )
    p = _resolve_provider(provider)
    rows: list[RunRow] = []
    for prompt in prompts:
        try:
            resp = p.complete(prompt.prompt, model=model)
        except NotImplementedError as e:
            raise click.ClickException(str(e))
        ev = evaluate(resp.text, prompt.expected_refusal_keywords)
        rows.append(build_row(prompt, ev, resp.text))
    result = RunResult(provider=provider, model=model, corpus_version=corpus_version, rows=tuple(rows))

    table = Table(title=f"polyjb run: {provider}/{model} on {lang} ({corpus_version})")
    table.add_column("prompt_id"); table.add_column("category"); table.add_column("refused"); table.add_column("matched")
    for r in rows:
        table.add_row(r.prompt_id, r.category, str(r.refused), ", ".join(r.matched_keywords) or "-")
    console.print(table)
    console.print(f"refusal_rate: {result.refusal_rate:.3f}")

    if out_path is None:
        out_path = Path("runs") / f"{provider}__{model.replace('/', '_')}__{lang}__{corpus_version}.json"
    write_json(result, out_path)
    console.print(f"wrote {out_path}")


@main.command("compare")
@click.argument("results", nargs=-1, type=click.Path(exists=True, dir_okay=False, path_type=Path), required=True)
def compare_cmd(results: tuple[Path, ...]) -> None:
    """Aggregate multiple run JSONs into a single summary table."""
    table = Table(title="polyjb compare")
    table.add_column("provider/model"); table.add_column("lang"); table.add_column("rows"); table.add_column("refusal_rate")
    for path in results:
        data = json.loads(path.read_text(encoding="utf-8"))
        rows = data.get("rows", [])
        if not rows:
            continue
        lang = rows[0].get("language", "?")
        refusal_rate = sum(1 for r in rows if r.get("refused")) / len(rows) if rows else 0.0
        table.add_row(f"{data.get('provider', '?')}/{data.get('model', '?')}", lang, str(len(rows)), f"{refusal_rate:.3f}")
    console.print(table)


if __name__ == "__main__":
    main()
