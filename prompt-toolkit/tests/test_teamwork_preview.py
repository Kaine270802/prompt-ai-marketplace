import json
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE_ROOT = PLUGIN_ROOT.parent
TEAMWORK_ROOT = PLUGIN_ROOT / "skills" / "k-teamwork-preview"
TEAMWORK_SKILL = TEAMWORK_ROOT / "SKILL.md"
TEAMWORK_BLUEPRINTS = TEAMWORK_ROOT / "references" / "blueprints.md"
TEAMWORK_ROLES = TEAMWORK_ROOT / "references" / "roles-governance.md"
TEAMWORK_SHEET = TEAMWORK_ROOT / "resources" / "team-sheet-template.md"
TEAMWORK_AUDIT = TEAMWORK_ROOT / "resources" / "audit-checklist-template.md"
E2E_ROOT = PLUGIN_ROOT / "skills" / "k-e2e"
E2E_SKILL = E2E_ROOT / "SKILL.md"
E2E_UI_METADATA = E2E_ROOT / "agents" / "openai.yaml"

EXPECTED_SKILLS = {
    "k-ask",
    "k-goal",
    "k-review",
    "k-engineer",
    "k-boost",
    "k-nspec",
    "k-rvspec",
    "k-e2e",
    "k-teamwork-preview",
}

# Skills that enforce session-wide manual-only invocation markers.
STRICT_MANUAL_SKILLS = EXPECTED_SKILLS - {"k-boost", "k-teamwork-preview"}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict:
    return json.loads(read(path))


class TeamworkPreviewContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.skill = read(TEAMWORK_SKILL)
        self.blueprints = read(TEAMWORK_BLUEPRINTS)
        self.roles = read(TEAMWORK_ROLES)
        self.sheet = read(TEAMWORK_SHEET)
        self.audit = read(TEAMWORK_AUDIT)
        self.e2e = read(E2E_SKILL)
        self.readme = read(PLUGIN_ROOT / "README.md")

    def test_skill_matches_current_teamwork_model(self) -> None:
        self.assertRegex(self.skill, r"(?m)^name: k-teamwork-preview$")
        self.assertIn("Sentinel", self.skill)
        self.assertIn("Team Sheet", self.skill)
        self.assertIn("Success Auditor", self.skill)
        self.assertIn("Distributed Coding", self.skill)
        self.assertIn("Iterative Coding", self.skill)
        self.assertIn("Long Proof", self.skill)
        self.assertIn("Approval", self.skill)
        self.assertIn("references/blueprints.md", self.skill)
        self.assertIn("references/roles-governance.md", self.skill)
        self.assertIn("resources/team-sheet-template.md", self.skill)
        self.assertIn("resources/audit-checklist-template.md", self.skill)
        self.assertIn("/k-teamwork-preview", self.skill)
        # Old pre-2.6.0 controller model must stay gone.
        self.assertNotIn("TEAMWORK_PROTOCOL_V1", self.skill)
        self.assertNotIn("`CONTROLLER`", self.skill)
        self.assertNotIn("`NATIVE_ADAPTER`", self.skill)
        self.assertNotIn("example-teams", self.skill)
        self.assertNotIn("Coordinator / Hiring Manager", self.skill)
        self.assertNotIn("Independent Verifier", self.skill)

    def test_blueprints_roles_and_templates_exist(self) -> None:
        for path in (
            TEAMWORK_BLUEPRINTS,
            TEAMWORK_ROLES,
            TEAMWORK_SHEET,
            TEAMWORK_AUDIT,
        ):
            self.assertTrue(path.is_file(), path)
        self.assertIn("Distributed Coding", self.blueprints)
        self.assertIn("Iterative Coding", self.blueprints)
        self.assertIn("Long Proof", self.blueprints)
        self.assertIn("Success Auditor", self.blueprints)
        self.assertIn("Sentinel", self.roles)
        self.assertIn("Success Auditor", self.roles)
        self.assertIn("worktree", self.roles)
        self.assertIn("Team Sheet", self.sheet)
        self.assertIn("Milestone", self.sheet)
        self.assertIn("Approval", self.sheet)
        self.assertIn("APPROVED", self.audit)
        self.assertIn("CHANGES_REQUESTED", self.audit)
        self.assertFalse((TEAMWORK_ROOT / "references" / "protocol.md").exists())
        self.assertFalse(
            (TEAMWORK_ROOT / "references" / "example-teams.md").exists()
        )

    def test_e2e_composes_the_team_sheet_workflow(self) -> None:
        self.assertIn("../k-teamwork-preview/SKILL.md", self.e2e)
        self.assertIn(
            "../k-teamwork-preview/references/blueprints.md", self.e2e
        )
        self.assertIn(
            "../k-teamwork-preview/references/roles-governance.md", self.e2e
        )
        self.assertIn("TEAM_PLAN.md", self.e2e)
        self.assertIn("yes / approve / go", self.e2e)
        self.assertNotIn("TEAMWORK_PROTOCOL_V1", self.e2e)
        self.assertNotIn("protocol.md", self.e2e)
        self.assertFalse(
            (E2E_ROOT / "references" / "teamwork-preview.md").exists()
        )

    def test_native_command_and_plugin_skill_are_unambiguous(self) -> None:
        self.assertIn("Sentinel", self.skill)
        self.assertIn("Success Auditor", self.skill)
        self.assertIn("Team Sheet", self.skill)
        self.assertIn("chọn `k-teamwork-preview` có source", self.readme)
        self.assertIn("`prompt-toolkit` trong `/skills`", self.readme)
        self.assertIn("quota/credits", self.readme)

    def test_all_skill_directories_and_ui_metadata_exist(self) -> None:
        discovered = {
            path.parent.name
            for path in (PLUGIN_ROOT / "skills").glob("*/SKILL.md")
        }
        self.assertEqual(EXPECTED_SKILLS, discovered)
        ui_metadata = read(E2E_UI_METADATA)
        self.assertIn("$k-e2e", ui_metadata)
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
        # Local Codex builds may append "+codex.<cachebuster>"; the base
        # version must always match.
        self.assertEqual(base_version, codex_version.split("+", 1)[0])

    def test_readme_and_manifests_advertise_nine_skills(self) -> None:
        self.assertIn("Bộ 9 Agent Skills", self.readme)
        for skill in EXPECTED_SKILLS:
            self.assertIn(f"`{skill}`", self.readme)
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
            self.assertIn("Nine manual skills", read(manifest), manifest)
        self.assertIn(
            "Bộ 9 skill", read(PLUGIN_ROOT / ".zcode-plugin" / "plugin.json")
        )

    def test_cursor_and_copilot_install_paths_are_documented(self) -> None:
        self.assertIn(".cursor/skills/", self.readme)
        self.assertIn("~/.cursor/plugins/local", self.readme)
        self.assertIn(".github/skills/", self.readme)
        self.assertIn("~/.copilot/skills/", self.readme)
        self.assertIn("disable-model-invocation", self.readme)
        self.assertTrue((PLUGIN_ROOT / ".cursor-plugin" / "plugin.json").is_file())
        cursor_market = load_json(
            MARKETPLACE_ROOT / ".cursor-plugin" / "marketplace.json"
        )
        self.assertEqual(cursor_market["name"], "prompt-ai-marketplace")
        self.assertEqual(cursor_market["plugins"][0]["source"], "prompt-toolkit")
        self.assertFalse(
            str(cursor_market["plugins"][0]["source"]).startswith("./")
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
            self.assertRegex(text, r"(?m)^name: " + skill_dir.name + r"$")
            # Every skill documents its explicit invocation path.
            self.assertIn(f"/{skill_dir.name}", text, skill_file)
        # The strictly manual skills additionally lock the session gate.
        # k-boost (on-demand deep reasoning) and k-teamwork-preview
        # (complexity-triggered) intentionally allow model invocation.
        for skill_name in STRICT_MANUAL_SKILLS:
            text = read(PLUGIN_ROOT / "skills" / skill_name / "SKILL.md")
            self.assertIn("disable-model-invocation: true", text, skill_name)
            self.assertIn("MANUAL-ONLY", text, skill_name)

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
