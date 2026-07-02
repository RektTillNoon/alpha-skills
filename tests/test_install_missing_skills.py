import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from scripts import install_missing_skills


class InstallMissingSkillsTest(unittest.TestCase):
    def test_collects_installed_names_from_nested_cli_json(self):
        payload = {
            "global": [
                {"name": "clean"},
                {"skillName": "owner-check"},
                {"skills": [{"slug": "investigate-fix"}]},
            ]
        }

        self.assertEqual(
            install_missing_skills.collect_installed_skill_names(payload),
            {"clean", "owner-check", "investigate-fix"},
        )

    def test_discovers_only_top_level_skill_directories(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "clean").mkdir()
            (root / "clean" / "SKILL.md").write_text("---\nname: clean\n---\n")
            (root / "plugins").mkdir()
            (root / "plugins" / "SKILL.md").write_text("---\nname: nope\n---\n")
            (root / "README.md").write_text("# Test\n")

            self.assertEqual(install_missing_skills.discover_skill_names(root), ["clean"])

    def test_main_skips_already_installed_skills(self):
        installed = {"clean", "owner-check"}

        with (
            patch.object(install_missing_skills, "discover_skill_names", return_value=["clean", "owner-check"]),
            patch.object(install_missing_skills, "list_installed_skill_names", return_value=installed),
            patch.object(install_missing_skills, "install_skill") as install_skill,
        ):
            self.assertEqual(install_missing_skills.main(["clean", "owner-check", "--yes"]), 0)

        install_skill.assert_not_called()


if __name__ == "__main__":
    unittest.main()
