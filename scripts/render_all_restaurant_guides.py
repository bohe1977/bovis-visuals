#!/usr/bin/env python3
"""Render or verify every public restaurant guide declared in the v2 manifest."""
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "data" / "restaurant-guides" / "manifest.json"
RENDERER = ROOT / "scripts" / "render_restaurant_map.py"


def fail(message: str) -> None:
    raise SystemExit(message)


def relative_path(root: Path, value: str, label: str) -> Path:
    path = (root / value).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        fail(f"{label} escapes repository root: {value}")
    return path


def render(source: Path) -> str:
    with tempfile.TemporaryDirectory() as directory:
        output = Path(directory) / "guide.html"
        result = subprocess.run(
            [sys.executable, str(RENDERER), str(source), str(output)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        if result.returncode:
            fail(f"renderer failed for {source.relative_to(ROOT)}: {result.stderr.strip()}")
        return output.read_text(encoding="utf-8")


def alias_markup(site_base: str, output: Path, digest: str) -> str:
    destination = f"{site_base.rstrip('/')}/{output.parent.as_posix()}/?v={digest}"
    title = "최신 맛집 지도"
    return (
        '<!doctype html><html lang="ko"><head><meta charset="utf-8">'
        f'<meta http-equiv="refresh" content="0; url={destination}">'
        f'<link rel="canonical" href="https://bohe1977.github.io{destination}">'
        f'<title>{title}</title><script>location.replace({destination!r})</script></head>'
        f'<body><a href="{destination}">{title} 열기</a></body></html>'
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="fail when generated files or aliases are stale")
    mode.add_argument("--write", action="store_true", help="write every generated file and alias")
    args = parser.parse_args()

    manifest_path = args.manifest.resolve()
    root = ROOT
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest.get("siteBase"), str) or not manifest["siteBase"].startswith("/"):
        fail("manifest requires an absolute siteBase")
    guides = manifest.get("guides")
    if not isinstance(guides, list) or not guides:
        fail("manifest requires a non-empty guides array")

    seen = set()
    stale = []
    index_html = (root / "index.html").read_text(encoding="utf-8")
    for guide in guides:
        required = {"slug", "data", "output"}
        if not isinstance(guide, dict) or not required <= set(guide):
            fail("each manifest guide requires slug, data, and output")
        if guide["slug"] in seen:
            fail(f"duplicate manifest slug: {guide['slug']}")
        seen.add(guide["slug"])
        source = relative_path(root, guide["data"], "data path")
        output = relative_path(root, guide["output"], "output path")
        if not source.is_file():
            fail(f"missing data file: {guide['data']}")
        rendered = render(source)
        if not output.exists() or output.read_text(encoding="utf-8") != rendered:
            stale.append(guide["output"])
            if args.write:
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_text(rendered, encoding="utf-8")
        if "archiveHref" in guide and f'href="{guide["archiveHref"]}"' not in index_html:
            fail(f"index.html does not link manifest archiveHref: {guide['archiveHref']}")
        if "shareAlias" in guide:
            alias = relative_path(root, guide["shareAlias"], "shareAlias")
            digest = hashlib.sha256(rendered.encode("utf-8")).hexdigest()[:12]
            expected_alias = alias_markup(manifest["siteBase"], output.relative_to(root), digest)
            if not alias.exists() or alias.read_text(encoding="utf-8") != expected_alias:
                stale.append(guide["shareAlias"])
                if args.write:
                    alias.parent.mkdir(parents=True, exist_ok=True)
                    alias.write_text(expected_alias, encoding="utf-8")

    if stale and args.check:
        fail("stale generated restaurant guide files: " + ", ".join(stale))
    print(("wrote" if args.write else "verified") + f" {len(guides)} restaurant guides")


if __name__ == "__main__":
    main()
