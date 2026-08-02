#!/usr/bin/env python3
"""Create a draft restaurant-guide JSON; only manifest entries can be rendered publicly."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDE_DIR = ROOT / "data" / "restaurant-guides"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.strip().lower()).strip("-")
    if not slug:
        raise SystemExit("slug must contain lowercase latin letters or digits")
    return slug


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slug", required=True, help="latin, kebab-case guide identifier")
    parser.add_argument("--title", required=True)
    parser.add_argument("--origin", required=True, help="human-readable reference point")
    args = parser.parse_args()

    slug = slugify(args.slug)
    path = GUIDE_DIR / f"{slug}.json"
    if path.exists():
        raise SystemExit(f"refusing to overwrite existing guide: {path.relative_to(ROOT)}")

    draft = {
        "_status": "draft — add verified candidates, then register this file in manifest.json before rendering",
        "config": {
            "title": args.title,
            "description": f"{args.origin} 기준 맛집 지도 초안입니다.",
            "eyebrow": "LOCAL FOOD GUIDE",
            "intro": f"기준점은 <strong>{args.origin}</strong>입니다.",
            "source": "SOURCE: pending Naver Place verification",
            "notice": "후보·주소·메뉴·영업 정보는 검증 후 공개합니다.",
            "markerHelper": f"{args.origin} 기준 직선거리",
            "distanceFilters": [
                {"value": "all", "label": "전체"},
                {"value": "100", "label": "0~100m"},
                {"value": "300", "label": "100~300m"},
                {"value": "500", "label": "300~500m"},
            ],
        },
        "modeConfig": {
            "general": {
                "label": "일반 추천",
                "radiusLabel": "≤ 500m",
                "bestFor": "식사",
                "markerTitle": f"{args.origin}에서 가까운 순서",
                "quickPicks": [],
            }
        },
        "general": [],
    }
    path.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"created draft: {path.relative_to(ROOT)}")
    print("next: verify Naver Place evidence, fill candidates, add manifest entry, then run render_all_restaurant_guides.py --write")


if __name__ == "__main__":
    main()
