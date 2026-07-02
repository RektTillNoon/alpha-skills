import json
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "seo-geo"
SKILL_ROOT = PLUGIN_ROOT / "skills" / "seo-geo-audit"
CLAUDE_MARKETPLACE = REPO_ROOT / ".claude-plugin" / "marketplace.json"
CODEX_MARKETPLACE = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"
SECURITY_DOC = PLUGIN_ROOT / "SECURITY.md"
PROVIDER_DOC = PLUGIN_ROOT / "docs" / "provider-setup.md"
COMMAND_FILE = PLUGIN_ROOT / "commands" / "seo-geo-audit.md"
EXAMPLE_ROOT = PLUGIN_ROOT / "examples" / "sanitized-basic"
CI_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "seo-geo-publish-safety.yml"
TOP_LEVEL_SKILL_ROOTS = sorted(
    path for path in REPO_ROOT.iterdir() if path.is_dir() and (path / "SKILL.md").is_file()
)
EXPECTED_TOP_LEVEL_SKILLS = sorted(
    [
        "clean",
        "clean-commit",
        "clean-merge-push",
        "evolutionary-5-step",
        "investigate-fix",
        "owner-check",
        "owner-clean",
        "stateful-planning-protocol",
        "technical-design-dossier",
        "tty-design",
        "writing-ticks",
    ]
)
PUBLIC_TEXT_ROOTS = [
    REPO_ROOT / ".agents",
    REPO_ROOT / ".claude-plugin",
    REPO_ROOT / ".github",
    REPO_ROOT / "plugins" / "seo-geo",
    REPO_ROOT / "tests",
    *TOP_LEVEL_SKILL_ROOTS,
]
PUBLIC_TEXT_FILES = [
    REPO_ROOT / "README.md",
]


class SeoGeoPluginPublicContractTest(unittest.TestCase):
    def test_codex_and_claude_manifests_point_to_same_skill_path(self):
        codex_manifest = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
        claude_manifest = PLUGIN_ROOT / ".claude-plugin" / "plugin.json"

        self.assertTrue(codex_manifest.is_file())
        self.assertTrue(claude_manifest.is_file())

        codex = json.loads(codex_manifest.read_text())
        claude = json.loads(claude_manifest.read_text())

        self.assertEqual(codex["name"], "seo-geo")
        self.assertEqual(claude["name"], "seo-geo")
        self.assertEqual(codex["skills"], "./skills/")
        self.assertEqual(claude["skills"], "./skills/")
        self.assertIn("./commands/seo-geo-audit.md", claude["commands"])
        self.assertTrue((SKILL_ROOT / "SKILL.md").is_file())

    def test_claude_marketplace_installs_nested_plugin(self):
        self.assertTrue(CLAUDE_MARKETPLACE.is_file())

        marketplace = json.loads(CLAUDE_MARKETPLACE.read_text())
        plugins = {plugin["name"]: plugin for plugin in marketplace["plugins"]}

        self.assertIn("seo-geo", plugins)
        self.assertEqual(plugins["seo-geo"]["source"], "./plugins/seo-geo")
        self.assertEqual(plugins["seo-geo"]["repository"], "https://github.com/RektTillNoon/alpha-skills")

    def test_codex_marketplace_installs_nested_plugin(self):
        self.assertTrue(CODEX_MARKETPLACE.is_file())

        marketplace = json.loads(CODEX_MARKETPLACE.read_text())
        plugins = {plugin["name"]: plugin for plugin in marketplace["plugins"]}

        self.assertIn("seo-geo", plugins)
        self.assertEqual(plugins["seo-geo"]["source"]["source"], "local")
        self.assertEqual(plugins["seo-geo"]["source"]["path"], "./plugins/seo-geo")
        self.assertEqual(plugins["seo-geo"]["policy"]["installation"], "AVAILABLE")
        self.assertEqual(plugins["seo-geo"]["policy"]["authentication"], "ON_INSTALL")
        self.assertEqual(plugins["seo-geo"]["category"], "Productivity")

    def test_repo_does_not_expose_seo_geo_as_top_level_skill(self):
        skill_file = REPO_ROOT / "seo-geo-audit" / "SKILL.md"
        openai_metadata = REPO_ROOT / "seo-geo-audit" / "agents" / "openai.yaml"
        root_readme = REPO_ROOT / "README.md"

        self.assertFalse(skill_file.exists())
        self.assertFalse(openai_metadata.exists())

        readme_text = root_readme.read_text()

        self.assertNotIn("npx skills@latest add RektTillNoon/alpha-skills --skill seo-geo-audit", readme_text)
        self.assertNotIn("├── seo-geo-audit/", readme_text)

    def test_claude_command_routes_to_canonical_skill(self):
        self.assertTrue(COMMAND_FILE.is_file())

        command = COMMAND_FILE.read_text()

        self.assertIn("description:", command)
        self.assertIn("plugins/seo-geo/skills/seo-geo-audit/SKILL.md", command)
        self.assertIn("classify evidence", command.lower())
        self.assertIn("redact", command.lower())

    def test_install_provider_and_security_docs_are_public_safe(self):
        docs = [REPO_ROOT / "README.md", PLUGIN_ROOT / "README.md", PROVIDER_DOC, SECURITY_DOC]

        for doc in docs:
            self.assertTrue(doc.is_file(), f"Missing {doc}")

        combined = "\n".join(doc.read_text() for doc in docs)

        self.assertIn("/plugin install seo-geo@alpha-skills", combined)
        self.assertIn("cc --plugin-dir", combined)
        self.assertIn(".agents/plugins/marketplace.json", combined)
        self.assertIn("npx skills@latest", combined)
        self.assertIn("does not install the `seo-geo` plugin", combined)
        self.assertIn("credentials live in the host", combined.lower())
        self.assertIn("missing evidence", combined.lower())
        self.assertIn("gitleaks detect --source . --verbose", combined)

    def test_top_level_skill_collection_exposes_expected_skills(self):
        readme_text = (REPO_ROOT / "README.md").read_text()

        self.assertEqual([root.name for root in TOP_LEVEL_SKILL_ROOTS], EXPECTED_TOP_LEVEL_SKILLS)
        self.assertIn("scripts/install_missing_skills.py <skill-name> --yes", readme_text)

        for skill_root in TOP_LEVEL_SKILL_ROOTS:
            skill_file = skill_root / "SKILL.md"

            self.assertTrue(skill_file.is_file(), f"Missing {skill_file}")
            self.assertIn(f"`{skill_root.name}`", readme_text)

        self.assertIn("owner-check", (REPO_ROOT / "clean" / "SKILL.md").read_text())
        self.assertIn("owner-check", (REPO_ROOT / "clean-commit" / "SKILL.md").read_text())
        self.assertFalse((REPO_ROOT / "tex-spec-writer" / "SKILL.md").exists())

        dossier_root = REPO_ROOT / "technical-design-dossier"
        self.assertTrue((dossier_root / "assets" / "technical-design-dossier-template.tex").is_file())
        self.assertTrue((dossier_root / "references" / "golden-example.md").is_file())

    def test_sanitized_example_exists_and_has_expected_shape(self):
        evidence = EXAMPLE_ROOT / "evidence" / "crawl-summary.json"
        report = EXAMPLE_ROOT / "expected-report.md"
        readme = EXAMPLE_ROOT / "README.md"

        for path in (evidence, report, readme):
            self.assertTrue(path.is_file(), f"Missing {path}")

        data = json.loads(evidence.read_text())
        report_text = report.read_text()

        self.assertEqual(data["site"], "https://example.invalid")
        self.assertIn("Evidence Used", report_text)
        self.assertIn("Missing Evidence", report_text)
        self.assertIn("example.invalid", report_text)

    def test_ci_publish_safety_workflow_exists(self):
        self.assertTrue(CI_WORKFLOW.is_file())

        workflow = CI_WORKFLOW.read_text()

        self.assertIn("python3 -B -m unittest clean-commit.tests.test_inspect_unstaged_changes tests.test_install_missing_skills tests.test_seo_geo_plugin_public_contract", workflow)
        self.assertIn("gitleaks detect --source . --verbose", workflow)
        self.assertIn("Repo-local regex secret scan", workflow)
        self.assertIn("rg -n 'sk-", workflow)
        self.assertNotIn("tex-spec-writer", workflow)

    def test_public_content_is_project_generic(self):
        files = _public_scanned_files()
        combined = "\n".join(path.read_text(errors="ignore") for path in files)
        project_specific_patterns = {
            "macOS user home path": re.compile(r"/Users/[A-Za-z0-9._-]+"),
            "private desktop path": re.compile(r"(?:^|/)Desktop/[A-Za-z0-9._ -]+"),
            "repo-local private workspace": re.compile(r"Projects/[A-Za-z0-9._ -]+"),
            "private project content": re.compile(r"\b" + "Bary" + r"on\b|\b" + "bar" + r"yon\b"),
        }

        for label, pattern in project_specific_patterns.items():
            self.assertIsNone(pattern.search(combined), label)

        self.assertIn("any project", combined.lower())
        self.assertIn("public-safe", combined.lower())

    def test_public_content_does_not_embed_secret_like_values(self):
        scanned_files = _public_scanned_files()
        self.assertGreater(len(scanned_files), 0)

        secret_patterns = {
            "literal secret assignment": re.compile(
                r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*['\"][^'\"\n]{8,}['\"]"
            ),
            "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
            "openai key": re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
            "anthropic key": re.compile(r"sk-ant-[A-Za-z0-9_-]{20,}"),
            "github token": re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
            "slack token": re.compile(r"xox[baprs]-[A-Za-z0-9-]{20,}"),
            "google api key": re.compile(r"AIza[0-9A-Za-z_-]{35}"),
            "aws access key": re.compile(r"AKIA[0-9A-Z]{16}"),
            "jwt": re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"),
        }

        for path in scanned_files:
            text = path.read_text(errors="ignore")
            for label, pattern in secret_patterns.items():
                matches = [
                    match
                    for match in pattern.finditer(text)
                    if not _is_public_placeholder(match.group(0))
                ]
                self.assertEqual(matches, [], f"{label} in {path}: {matches[:3]}")


def _is_public_placeholder(value):
    placeholders = [
        "<token>",
        "<your-token>",
        "<api-token>",
        "<your-api-key>",
        "FIGMA_OAUTH_TOKEN",
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY",
        "CODEX_HOME",
        "CLOUDFLARE_API_TOKEN",
    ]
    return any(placeholder in value for placeholder in placeholders)


def _public_scanned_files():
    return [
        path
        for root in PUBLIC_TEXT_ROOTS
        for path in root.rglob("*")
        if path.is_file() and ".git" not in path.parts
    ] + PUBLIC_TEXT_FILES


if __name__ == "__main__":
    unittest.main()
