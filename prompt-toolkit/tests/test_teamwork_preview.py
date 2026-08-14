import json
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE_ROOT = PLUGIN_ROOT.parent
TEAMWORK_ROOT = PLUGIN_ROOT / "skills" / "teamwork-preview"
TEAMWORK_SKILL = TEAMWORK_ROOT / "SKILL.md"
TEAMWORK_EXAMPLES = TEAMWORK_ROOT / "references" / "example-teams.md"
E2E_SKILL = PLUGIN_ROOT / "skills" / "e2e" / "SKILL.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict:
    return json.loads(read(path))


class TeamworkPreviewContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.skill = read(TEAMWORK_SKILL)
        self.examples = read(TEAMWORK_EXAMPLES)
        self.e2e = read(E2E_SKILL)
        self.readme = read(PLUGIN_ROOT / "README.md")

    def test_skill_matches_source_team_sheet_workflow(self) -> None:
        self.assertRegex(self.skill, r"(?m)^name: teamwork-preview$")
        self.assertIn("MANUAL-ONLY", self.skill)
        self.assertIn("Coordinator / Hiring Manager", self.skill)
        self.assertIn("Design the Team Sheet", self.skill)
        self.assertIn("| Role | Specialty | Owns | Inputs | Outputs | Success Criteria |", self.skill)
        self.assertIn("TEAM_PLAN.md", self.skill)
        self.assertIn("Present for Approval (Mandatory Gate)", self.skill)
        self.assertIn("Independent Verifier must run before final delivery", self.skill)
        self.assertIn("references/example-teams.md", self.skill)
        self.assertNotIn("TEAMWORK_PROTOCOL_V1", self.skill)
        self.assertNotIn("`CONTROLLER`", self.skill)
        self.assertNotIn("`NATIVE_ADAPTER`", self.skill)

    def test_example_teams_reference_exists_and_protocol_is_gone(self) -> None:
        self.assertTrue(TEAMWORK_EXAMPLES.is_file())
        self.assertIn("| Role | Specialty | Owns | Inputs | Outputs | Success Criteria |", self.examples)
        self.assertIn("Full-Stack Web Application", self.examples)
        self.assertFalse((TEAMWORK_ROOT / "references" / "protocol.md").exists())

    def test_e2e_composes_the_team_sheet_workflow(self) -> None:
        self.assertIn("../teamwork-preview/SKILL.md", self.e2e)
        self.assertIn("../teamwork-preview/references/example-teams.md", self.e2e)
        self.assertIn("TEAM_PLAN.md", self.e2e)
        self.assertIn("yes / approve / go", self.e2e)
        self.assertNotIn("TEAMWORK_PROTOCOL_V1", self.e2e)
        self.assertNotIn("protocol.md", self.e2e)
        self.assertFalse(
            (PLUGIN_ROOT / "skills" / "e2e" / "references" / "teamwork-preview.md").exists()
        )

    def test_native_command_and_plugin_skill_are_unambiguous(self) -> None:
        self.assertIn("native `/teamwork-preview`", self.skill)
        self.assertIn("never start a second team", self.skill)
        self.assertIn("chọn `teamwork-preview` có source", self.readme)
        self.assertIn("`prompt-toolkit` trong `/skills`", self.readme)
        self.assertIn("quota/credits", self.readme)

    def test_all_skill_directories_and_ui_metadata_exist(self) -> None:
        expected = {
            "ask",
            "goal",
            "review",
            "engineer",
            "e2e",
            "teamwork-preview",
        }
        discovered = {
            path.parent.name
            for path in (PLUGIN_ROOT / "skills").glob("*/SKILL.md")
        }
        self.assertEqual(expected, discovered)
        ui_metadata = read(TEAMWORK_ROOT / "agents" / "openai.yaml")
        self.assertIn("$teamwork-preview", ui_metadata)
        self.assertIn("Team Sheet", ui_metadata)

    def test_manifest_base_versions_match(self) -> None:
        base_version = load_json(PLUGIN_ROOT / "plugin.json")["version"]
        versioned_manifests = [
            PLUGIN_ROOT / ".claude-plugin" / "plugin.json",
            PLUGIN_ROOT / ".cursor-plugin" / "plugin.json",
            PLUGIN_ROOT / ".grok-plugin" / "plugin.json",
            PLUGIN_ROOT / ".zcode-plugin" / "plugin.json",
            MARKETPLACE_ROOT / ".claude-plugin" / "marketplace.json",
            MARKETPLACE_ROOT / ".cursor-plugin" / "marketplace.json",
        ]
        for manifest in versioned_manifests:
            data = load_json(manifest)
            version = (
                data["plugins"][0]["version"]
                if manifest.name == "marketplace.json"
                else data["version"]
            )
            self.assertEqual(base_version, version, manifest)

        codex_version = load_json(
            PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
        )["version"]
        self.assertEqual(base_version, codex_version.split("+", 1)[0])
        self.assertIn("+codex.", codex_version)

    def test_readme_and_manifests_advertise_six_skills(self) -> None:
        self.assertIn("Bộ 6 Agent Skills", self.readme)
        self.assertIn("`teamwork-preview`", self.readme)
        english_manifests = [
            PLUGIN_ROOT / "plugin.json",
            PLUGIN_ROOT / ".codex-plugin" / "plugin.json",
            PLUGIN_ROOT / ".claude-plugin" / "plugin.json",
            PLUGIN_ROOT / ".grok-plugin" / "plugin.json",
            PLUGIN_ROOT / ".cursor-plugin" / "plugin.json",
            MARKETPLACE_ROOT / ".claude-plugin" / "marketplace.json",
            MARKETPLACE_ROOT / ".cursor-plugin" / "marketplace.json",
        ]
        for manifest in english_manifests:
            self.assertIn("Six manual skills", read(manifest), manifest)
        self.assertIn(
            "Bộ 6 skill", read(PLUGIN_ROOT / ".zcode-plugin" / "plugin.json")
        )

    def test_cursor_and_copilot_install_paths_are_documented(self) -> None:
        self.assertIn(".cursor/skills/", self.readme)
        self.assertIn("~/.cursor/plugins/local", self.readme)
        self.assertIn(".github/skills/", self.readme)
        self.assertIn("~/.copilot/skills/", self.readme)
        self.assertIn("disable-model-invocation", self.readme)
        self.assertTrue((PLUGIN_ROOT / ".cursor-plugin" / "plugin.json").is_file())
        self.assertTrue(
            (MARKETPLACE_ROOT / ".cursor-plugin" / "marketplace.json").is_file()
        )
        plugin = load_json(PLUGIN_ROOT / "plugin.json")
        self.assertEqual(
            plugin["$schema"],
            "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        )

    def test_skills_require_explicit_slash_invocation(self) -> None:
        for skill_dir in (PLUGIN_ROOT / "skills").iterdir():
            skill_file = skill_dir / "SKILL.md"
            if not skill_file.is_file():
                continue
            text = read(skill_file)
            self.assertIn("disable-model-invocation: true", text, skill_file)
            self.assertIn("MANUAL-ONLY", text, skill_file)

    def test_moa_is_not_bundled(self) -> None:
        forbidden = (
            "moa_ref",
            "moa_status",
            "moa_consult",
            "moa_ask_references",
            "CLI-MoA-AI",
            "Mixture-of-Agents",
            "second-opinion",
            "PHASE 1.5",
            "Stage 1.5",
        )
        scanned = [
            *MARKETPLACE_ROOT.glob("*.json"),
            *MARKETPLACE_ROOT.glob(".claude-plugin/*.json"),
            *MARKETPLACE_ROOT.glob(".agents/plugins/*.json"),
            *PLUGIN_ROOT.glob("*.json"),
            *PLUGIN_ROOT.glob(".*-plugin/*.json"),
            PLUGIN_ROOT / "README.md",
            *PLUGIN_ROOT.glob("skills/**/*.md"),
        ]
        for path in scanned:
            if not path.is_file():
                continue
            text = read(path)
            for token in forbidden:
                self.assertNotIn(token, text, f"{path} still mentions {token}")
        self.assertFalse((PLUGIN_ROOT / ".mcp.json").exists())
        self.assertFalse((PLUGIN_ROOT / "mcp_config.json").exists())
        self.assertNotIn("mcpServers", read(PLUGIN_ROOT / ".codex-plugin" / "plugin.json"))


if __name__ == "__main__":
    unittest.main()
