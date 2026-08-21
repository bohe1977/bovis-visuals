from __future__ import annotations

import json
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8765"
out: dict[str, object] = {"pages": []}
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for path in ("/kbo/", "/kbo-players/"):
        page_result: dict[str, object] = {"path": path, "viewports": []}
        for width, height in ((390, 844), (768, 1024), (1440, 1200)):
            page = browser.new_page(viewport={"width": width, "height": height})
            errors: list[str] = []
            page.on("pageerror", lambda exc: errors.append(str(exc)))
            response = page.goto(BASE + path, wait_until="networkidle")
            page.wait_for_timeout(100)
            assert response and response.ok
            text = page.locator("body").inner_text()
            assert "undefined" not in text
            assert "리포트를 불러오지 못했습니다" not in text
            assert not errors, errors
            entry = {"width": width, "height": height, "title": page.title(), "no_horizontal_overflow": page.evaluate("document.documentElement.scrollWidth <= window.innerWidth"), "errors": errors}
            assert entry["no_horizontal_overflow"], entry
            if path == "/kbo/":
                details = page.evaluate("""() => {
                    const cards=[...document.querySelectorAll('[data-game-card]')];
                    const winnerBounds=cards.flatMap(card=>{
                      const away=card.querySelector('.team.away'), home=card.querySelector('.team.home');
                      const awayBadge=away.querySelector('.winner'), homeBadge=home.querySelector('.winner');
                      const awayName=away.querySelector('.team-name'), homeName=home.querySelector('.team-name');
                      return [awayBadge ? {side:'away',good:awayBadge.getBoundingClientRect().right<=awayName.getBoundingClientRect().left} : null,homeBadge ? {side:'home',good:homeBadge.getBoundingClientRect().left>=homeName.getBoundingClientRect().right} : null].filter(Boolean);
                    });
                    const values=[...document.querySelectorAll('[data-stat-value]')];
                    return {games:cards.length,game_metric:document.querySelector('#metric-games').textContent,total_runs:document.querySelector('#metric-runs').textContent,inactive:[...document.querySelectorAll('#pitcher-inactive .none')].map(x=>x.textContent),status:document.querySelector('.status').textContent,meta_font:getComputedStyle(document.querySelector('.status')).fontFamily,winner_bounds:winnerBounds,one_rect_per_stat:values.every(x=>{const r=document.createRange();r.selectNodeContents(x);return r.getClientRects().length<=1}),mobile_one_column:innerWidth>760||getComputedStyle(document.querySelector('#games')).gridTemplateColumns.split(' ').length===1};
                }""")
                assert details["games"] == 5 and details["game_metric"] == "5" and details["total_runs"] == "64", details
                assert all(x == "등판 없음" for x in details["inactive"]), details
                assert details["status"] == "경기 결과" and "Geist Mono" in details["meta_font"], details
                assert all(x["good"] for x in details["winner_bounds"]), details
                assert details["one_rect_per_stat"] and details["mobile_one_column"], details
                entry.update(details)
            else:
                details = page.evaluate("""() => ({active:document.querySelectorAll('#pa [data-player-card]').length,inactive:[...document.querySelectorAll('#pi .none')].map(x=>x.textContent),badges:[...document.querySelectorAll('.state')].map(x=>x.textContent)})""")
                assert details["active"] == 3 and all(x == "등판 없음" for x in details["inactive"]), details
                assert "승리" in details["badges"] and "패" in details["badges"] and "세이브" not in details["badges"] and "홀드" not in details["badges"], details
                entry.update(details)
            page.screenshot(path=f".artifacts/kbo-2026-08-21/{path.strip('/').replace('/','-')}-{width}.png", full_page=True)
            page_result["viewports"].append(entry)
            page.close()
        out["pages"].append(page_result)
    browser.close()
Path(".artifacts/kbo-2026-08-21/browser-qa.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=2))
