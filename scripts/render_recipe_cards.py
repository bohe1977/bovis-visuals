#!/usr/bin/env python3
"""Render the approved recipe-card-v1 template from a source-backed guide JSON."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "recipe-cards-v1.html"
CONTRACT = ROOT / "standards" / "recipe-card-contract-v1.json"
ACCENT_RE = re.compile(r"#[0-9a-f]{6}$")
HONORIFIC_RE = re.compile(r"(?:요|니다|습니다)[.!]?$")


def fail(message: str) -> None:
    raise ValueError(message)


def validate(guide: dict[str, Any]) -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    if guide.get("version") != contract["version"]:
        fail("guide version must be recipe-card-v1")
    raw_recipes = guide.get("recipes")
    if not isinstance(raw_recipes, list) or len(raw_recipes) != contract["recommendation_card_count"]:
        fail("recipe-card-v1 requires exactly 8 recipes")
    recipes = cast(list[dict[str, Any]], raw_recipes)

    accents: set[str] = set()
    for expected_rank, recipe in enumerate(recipes, start=1):
        if recipe.get("rank") != expected_rank:
            fail(f"recipe {expected_rank} rank must be consecutive")
        for field in contract["required_card_fields"]:
            if not recipe.get(field):
                fail(f"recipe {expected_rank} missing {field}")
        accent = recipe["accent"]
        if not isinstance(accent, str) or not ACCENT_RE.fullmatch(accent):
            fail(f"recipe {expected_rank} accent must be a lowercase hex color")
        if accent in accents:
            fail(f"recipe {expected_rank} accent must be unique")
        accents.add(accent)
        if not recipe["reference"].startswith("https://www.instagram.com/"):
            fail(f"recipe {expected_rank} reference must be an Instagram URL")
        if recipe["status"] not in contract["notice_rules"]["allowed_statuses"]:
            fail(f"recipe {expected_rank} has unsupported status")
        notice = recipe.get("notice")
        if recipe["status"] in {"followup", "caution"} and not notice:
            fail(f"recipe {expected_rank} {recipe['status']} requires a notice")
        if recipe["status"] == "complete" and notice:
            fail(f"recipe {expected_rank} complete may not have a notice")
        raw_steps = recipe.get("steps")
        if not isinstance(raw_steps, list) or not raw_steps:
            fail(f"recipe {expected_rank} requires one or more source-backed steps")
        steps = cast(list[str], raw_steps)
        for step in steps:
            if not isinstance(step, str) or not step.strip():
                fail(f"recipe {expected_rank} contains an empty step")
            if HONORIFIC_RE.search(step.strip()):
                fail(f"recipe {expected_rank} step must use command form, not honorific")


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def card(recipe: dict) -> str:
    steps = "\n".join(f"<li>{esc(step)}</li>" for step in recipe["steps"])
    notice = ""
    if recipe.get("notice"):
        notice = f'\n        <p class="notice"><strong>확인 사항</strong>{esc(recipe["notice"])}</p>'
    return f'''      <article class="recipe-card" style="--accent:{esc(recipe["accent"])}">
        <div class="card-head"><span class="rank">{recipe["rank"]:02d}</span><h2>{esc(recipe["title"])}</h2><a class="reference" href="{esc(recipe["reference"])}" target="_blank" rel="noopener">레퍼런스</a></div>
        <div class="section"><span class="label">준비물</span><p class="ingredients">{esc(recipe["ingredients"])}</p></div>
        <div class="section"><span class="label">조리 흐름</span><ol>{steps}</ol></div>{notice}
      </article>'''


def render(guide: dict) -> str:
    validate(guide)
    template = TEMPLATE.read_text(encoding="utf-8")
    replacements = {
        "__TITLE__": esc(guide["title"]),
        "__DESCRIPTION__": esc(guide["description"]),
        "__EYEBROW__": esc(guide["eyebrow"]),
        "__INTRO__": esc(guide["intro"]),
        "__FOOTER__": esc(guide["footer"]),
        "__CARDS__": "\n".join(card(recipe) for recipe in guide["recipes"]),
    }
    for token, value in replacements.items():
        template = template.replace(token, value)
    if re.search(r"__[A-Z]+__", template):
        fail("unresolved recipe template token")
    return template


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        guide = json.loads(args.input.read_text(encoding="utf-8"))
        output = render(guide)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"recipe-card-v1: {error}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
