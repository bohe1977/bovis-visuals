import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "scripts" / "render_recipe_cards.py"
GUIDE = ROOT / "data" / "recipe-guides" / "ramen-recipes-8.json"


class RecipeCardContractTests(unittest.TestCase):
    def render(self, guide=GUIDE):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "index.html"
            result = subprocess.run(
                [sys.executable, str(RENDERER), "--input", str(guide), "--output", str(output)],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            return output.read_text(encoding="utf-8")

    def test_current_guide_renders_eight_standard_cards(self):
        html = self.render()
        self.assertEqual(html.count('<article class="recipe-card"'), 8)
        self.assertEqual(html.count('>레퍼런스</a>'), 8)
        self.assertNotIn('레퍼런스 보기', html)
        self.assertNotIn('article::before', html)
        self.assertIn('border-bottom:3px solid var(--accent)', html)

    def test_card_colors_are_unique_and_step_numbers_are_black(self):
        html = self.render()
        colors = __import__('re').findall(r'<article class="recipe-card" style="--accent:(#[0-9a-f]{6})">', html)
        self.assertEqual(len(colors), 8)
        self.assertEqual(len(set(colors)), 8)
        self.assertIn('li::before { content:counter(recipe);', html)
        self.assertIn('color:#111;', html)

    def test_followup_notice_uses_spaced_gray_notice_card(self):
        html = self.render()
        self.assertIn('<strong>확인 사항</strong>원문에서 추가 조리사항 확인 필요', html)
        self.assertIn('margin:31px 0 0;', html)
        self.assertIn('background:var(--wash);', html)

    def test_renderer_rejects_followup_without_notice(self):
        guide = json.loads(GUIDE.read_text(encoding="utf-8"))
        guide["recipes"][5]["notice"] = None
        with tempfile.TemporaryDirectory() as temp:
            invalid = Path(temp) / "invalid.json"
            output = Path(temp) / "index.html"
            invalid.write_text(json.dumps(guide, ensure_ascii=False), encoding="utf-8")
            result = subprocess.run([sys.executable, str(RENDERER), "--input", str(invalid), "--output", str(output)], cwd=ROOT, text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("followup", result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
