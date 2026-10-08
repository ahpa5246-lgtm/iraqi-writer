"""Repository structure checks (stdlib only).

Run: python -m unittest discover -s tests -v
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
NAMES = (
    "single-post", "carousel", "technical", "design-writing",
    "visual-direction", "research", "editor",
)


class SkillsStructureTests(unittest.TestCase):
    def test_root_router(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        for term in ("الصيغة", "المجال", "الفعل", "مراجعة أولى", "مراجعة ثانية"):
            self.assertIn(term, text)

    def test_unique_skills(self):
        seen = set()
        for folder in NAMES:
            path = ROOT / "skills" / folder / "SKILL.md"
            content = path.read_text(encoding="utf-8")
            self.assertTrue(content.startswith("---\n"), str(path))
            header = content.split("---", 2)[1]
            name = re.search(r"(?m)^name:\s*(\S+)", header)
            self.assertIsNotNone(name, str(path))
            self.assertNotIn(name.group(1), seen)
            seen.add(name.group(1))
            self.assertRegex(header, r"(?m)^description:")

    def test_internal_links(self):
        for file in ROOT.rglob("*.md"):
            content = file.read_text(encoding="utf-8")
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", content):
                target = target.split("#", 1)[0]
                if target.startswith(("http:", "https:", "mailto:")):
                    continue
                self.assertTrue((file.parent / target).resolve().is_file(),
                                f"Broken link {file}: {target}")

    def test_voice_guide(self):
        content = (ROOT / "references/voice.md").read_text(encoding="utf-8")
        self.assertIn("فصحى", content)
        self.assertIn("لا تُكثر", content)


if __name__ == "__main__":
    unittest.main()
