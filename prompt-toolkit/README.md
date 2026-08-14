# prompt-toolkit

Bộ 6 Agent Skills dùng chung cho nhiều coding agent, từ nâng
cấp prompt/goal đến read-only review, implementation và verification end-to-end.
`teamwork-preview` là Coordinator / Hiring Manager: thiết kế Team Sheet, chờ user
duyệt, rồi chạy specialist subagents kèm independent verifier/critic. `e2e` tự chọn
direct execution hoặc compose skill này khi work phức tạp.
Mỗi skill là một thư mục `SKILL.md` theo
[Agent Skills open standard](https://agentskills.io/). Cài plugin marketplace nhận
đủ 6 skill.

## Skills

| Skill | Chức năng | Kết quả |
|---|---|---|
| `ask` | Nghiên cứu context và nâng cấp raw prompt | Một prompt copy-ready; không thực thi task |
| `goal` | Làm rõ outcome, scope và success criteria | Một goal copy-ready; để ngỏ cách thực hiện |
| `review` | Audit/diagnose code ở chế độ read-only | Findings có evidence; mọi fix đều `NOT APPLIED` |
| `engineer` | Thực hiện coding task theo Phase 0→4 | Thay đổi nhỏ nhất kèm tests và verification |
| `e2e` | Ghép `review → ask → engineer → verify`, có adaptive teamwork | Hoàn thành coding task bằng direct hoặc coordinator-led subagents |
| `teamwork-preview` | Coordinator thiết kế Team Sheet, duyệt, rồi chạy specialist team | `TEAM_PLAN.md` + artifacts đã verify |

Tất cả skill đều **manual-only**: chỉ dùng khi user gọi rõ tên skill. Cú pháp gọi
khác nhau theo host; xem bảng Quick start bên dưới.

## Workflow `e2e`

```text
raw user prompt
      ↓
review (read-only evidence + root cause)
      ↓
ask (internal grounded execution brief)
      ↓
execution gate
   ├── DIRECT: coordinator implements
   └── TEAMWORK: Team Sheet → user approval → specialists
          ├── Researcher / Explorer (read-only)
          ├── Domain Builders (disjoint Owns)
          └── independent Verifier + Critic/Auditor
      ↓
Coordinator synthesizes verified outputs
```

`e2e` giữ review và upgraded prompt làm internal artifacts, vì vậy user không phải
copy prompt qua ba agent. Skill chỉ dừng để hỏi khi có ambiguity làm thay đổi đáng
kể implementation, L4/L5, schema/auth/permission change hoặc dependency mới.

### Teamwork mode

`teamwork-preview` là control-plane skill độc lập, bám workflow của folder nguồn
`teamwork-preview/`: Coordinator thiết kế Team Sheet, user duyệt, rồi launch
specialists. `e2e` compose skill này khi chọn TEAMWORK. Skill **không** giả lập
native command Antigravity và **không** dùng protocol Sentinel/capsule riêng.

Workflow bắt buộc:

1. Assess & decompose — goal một câu, workstream, team tối thiểu 3–6.
2. Team Sheet — bảng `Role | Specialty | Owns | Inputs | Outputs | Success Criteria`,
   handoff artifacts, milestones, cảnh báo token/cost. Lưu `TEAM_PLAN.md`.
3. Approval gate — dừng đến khi user trả lời yes / approve / go, hoặc sửa plan.
4. Launch — ưu tiên native parallel subagents; nếu host không có, chạy sequential
   focused sessions với shared files, không nhồi hết context vào Coordinator.
5. Verification — independent Verifier trước delivery, rồi Critic/Auditor.
6. Synthesize — Coordinator gộp output đã verify và bàn giao.

Typical roles (chọn động theo task, xem `skills/teamwork-preview/references/example-teams.md`):

| Role | Trách nhiệm |
|---|---|
| Coordinator / Orchestrator | Plan, handoffs, synthesis; không làm thay toàn bộ team |
| Researcher / Explorer | Unknowns, APIs, docs, prior art |
| Domain Builders / Workers (1–4) | Implement theo component, Owns không chồng |
| Verifier / QA | Tests, edge cases, correctness |
| Critic / Auditor | Adversarial review, anti-patterns, false claims |

Guardrails:

- Task đơn giản: nói rõ và làm bình thường; không ép team.
- Không bỏ cổng duyệt hoặc bước independent verification.
- Không để một agent làm hết dưới nhiều tên.
- Owns không chồng để tránh merge conflict.
- Specialist chỉ nhận role brief + artifact liên quan; output ghi file chia sẻ.
- Native `/teamwork-preview` của Antigravity nếu đã sở hữu session thì reuse; không
  mở team thứ hai.

| Host | Teamwork behavior |
|---|---|
| Cursor | Parallel Task/subagents khi Agent expose; không thì sequential + shared files. Gọi `/teamwork-preview` hoặc `/e2e` |
| GitHub Copilot | Agent mode / Copilot CLI; parallel khi host spawn được. Gọi `/teamwork-preview` hoặc `/e2e` |
| Antigravity | Ưu tiên native `/teamwork-preview` khi đã mở; ngoài ra dùng subagent song song nếu host expose |
| Codex | Spawn/delegation khi có; không thì sequential + shared files |
| Claude Code | Agent/subagents hoặc agent teams khi enabled |
| Grok Build | Delegation khi child return quan sát được; không thì sequential |
| Gemini CLI | Delegation khi child return quan sát được; không thì sequential |
| Windsurf | Cascade/subagents khi host expose; không thì sequential |
| OpenCode | Task/agent delegation khi permissions cho phép |
| ZCode | Delegation khi có child lifecycle riêng |

Ví dụ:

```text
/prompt-toolkit:e2e Sửa lỗi login bị kẹt loading khi API trả 401 và thêm regression test.
```

Ở host dùng `$skill-name`:

```text
$e2e Sửa lỗi login bị kẹt loading khi API trả 401 và thêm regression test.
```

Gọi controller skill trực tiếp trên host hỗ trợ namespace hoặc `$skill`:

```text
/prompt-toolkit:teamwork-preview Xây feature này bằng một team có independent audit.
$teamwork-preview Xây feature này bằng một team có independent audit.
```

Với Antigravity, nếu native `/teamwork-preview` đã sở hữu session thì reuse nó và
áp dụng Team Sheet của skill này làm operating plan; không mở team thứ hai. Native
command có thể tốn quota/credits lớn. Để gọi skill plugin, chọn `teamwork-preview` có source `prompt-toolkit` trong `/skills` hoặc yêu cầu rõ bằng lời; chỉ dùng cú pháp namespace khi host thực sự hiển thị nó.

## Cấu trúc repository

```text
prompt-ai-marketplace/
├── marketplace.json                         # ZCode marketplace
├── .agents/plugins/marketplace.json         # Codex marketplace
├── .claude-plugin/marketplace.json          # Claude Code marketplace
├── .cursor-plugin/marketplace.json          # Cursor team marketplace
└── prompt-toolkit/
    ├── .zcode-plugin/plugin.json            # ZCode plugin manifest
    ├── .grok-plugin/plugin.json             # Grok Build plugin manifest
    ├── .codex-plugin/plugin.json            # Codex plugin manifest
    ├── .claude-plugin/plugin.json           # Claude Code plugin manifest
    ├── .cursor-plugin/plugin.json           # Cursor plugin manifest
    ├── plugin.json                           # Agent Plugins + Antigravity manifest
    ├── README.md
    └── skills/
        ├── ask/SKILL.md
        ├── goal/SKILL.md
        ├── review/SKILL.md
        ├── engineer/SKILL.md
        ├── e2e/
        │   ├── SKILL.md
        │   └── agents/openai.yaml           # Optional Codex UI metadata
        └── teamwork-preview/
            ├── SKILL.md
            ├── agents/openai.yaml           # Optional Codex UI metadata
            └── references/example-teams.md
```

## Quick start theo host

| Host | Cách cài khuyến nghị | Cách gọi teamwork |
|---|---|---|
| Cursor | Plugin local hoặc copy skills | `/teamwork-preview <task>` hoặc `/e2e` |
| GitHub Copilot | Copy skills hoặc `gh skill` | `/teamwork-preview <task>` hoặc `/e2e` |
| Claude Code | Marketplace plugin | `/prompt-toolkit:teamwork-preview <task>` hoặc `/prompt-toolkit:e2e` |
| Codex | Native marketplace plugin | `$teamwork-preview <task>` hoặc `$e2e` |
| Google Antigravity | Native `agy plugin` | Native `/teamwork-preview`; custom chọn từ `/skills` theo source plugin |
| Grok Build | Marketplace plugin | `/teamwork-preview <task>` hoặc `/e2e` |
| Gemini CLI | Copy hoặc `gemini skills` | `/teamwork-preview <task>` hoặc `/e2e` |
| Windsurf | Copy vào `.windsurf/skills/` | Yêu cầu “use the teamwork-preview skill” hoặc `/teamwork-preview` |
| OpenCode | Copy vào `.opencode/skills/` | Yêu cầu “use the teamwork-preview skill” |
| Hermes Agent | Copy vào `~/.hermes/skills/` | `/teamwork-preview <task>` hoặc `/e2e` |
| ZCode | Marketplace plugin | `/prompt-toolkit:teamwork-preview <task>` hoặc `$teamwork-preview` |

Các lệnh bên dưới giả định terminal đang đứng tại root `prompt-ai-marketplace/`.
Nếu đang ở nơi khác, thay `./prompt-toolkit/skills` bằng absolute path tương ứng.

### Claude Code

Repository đã bundle đủ cả marketplace manifest và plugin manifest, không cần tạo
thêm file thủ công.

```bash
claude plugin marketplace add "$(pwd)"
claude plugin install prompt-toolkit@prompt-ai-marketplace
```

Hoặc trong Claude Code:

```text
/plugin marketplace add /absolute/path/to/prompt-ai-marketplace
/plugin install prompt-toolkit@prompt-ai-marketplace
```

Test trực tiếp mà không cài marketplace:

```bash
claude --plugin-dir "$(pwd)/prompt-toolkit"
```

Kiểm tra bằng `/skills` hoặc gõ `/prompt-toolkit:`. Claude Code namespace các skill
được cài qua plugin bằng tên plugin. Xem
[Claude Code plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces).

### Codex (CLI, app, IDE)

Codex có native plugin manager. Cài marketplace và plugin ở user-level:

```bash
codex plugin marketplace add "$(pwd)"
codex plugin add prompt-toolkit@prompt-ai-marketplace
```

Kiểm tra:

```bash
codex plugin list
```

Mở task/session mới sau khi cài vì catalog của task đang chạy không hot-reload, rồi
gọi `$teamwork-preview <task>` hoặc `$e2e <task>`. Với Codex cũ chưa có
`codex plugin`, có thể fallback bằng cách
copy `./prompt-toolkit/skills/*` vào `~/.codex/skills/`.
`agents/openai.yaml` trong `e2e` và `teamwork-preview` cung cấp display metadata cho
các Codex surface hỗ trợ field này. Xem
[OpenAI Skills catalog](https://github.com/openai/skills).

Khi surface Codex expose subagent delegation, `e2e`/`teamwork-preview` ưu tiên
parallel specialists theo Team Sheet. Nếu không có, chạy sequential focused sessions
với shared files; không bịa ý kiến từ agent chưa chạy.

### Cursor

Cursor nhận plugin theo [Agent Plugins](https://agent-plugins.org) (`plugin.json` ở
root `prompt-toolkit/`) và Cursor Plugin (`.cursor-plugin/plugin.json`). Skills cũng
được discover từ thư mục `SKILL.md`.

**Không** thêm folder local vào Customize marketplace trừ khi đó là git repo đã có
commit: Cursor chạy `git ls-remote … HEAD` trên `file://` path. Folder chưa `git
init` sẽ lỗi `does not appear to be a git repository`.

Cài plugin local (không cần git, khuyến nghị khi phát triển):

```bash
mkdir -p ~/.cursor/plugins/local
ln -s "$(pwd)/prompt-toolkit" ~/.cursor/plugins/local/prompt-toolkit
```

Windows (PowerShell, junction nếu không dùng symlink):

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.cursor\plugins\local" | Out-Null
New-Item -ItemType Junction -Force -Path "$env:USERPROFILE\.cursor\plugins\local\prompt-toolkit" -Target "$(Get-Location)\prompt-toolkit"
```

Restart Cursor hoặc **Developer: Reload Window**. Mở **Customize → Skills** và gọi
`/ask`, `/goal`, `/review`, `/engineer`, `/e2e`, `/teamwork-preview` trong Agent chat.

Nếu đã Add Marketplace trỏ vào folder này rồi bị `Failed to resolve git ref "HEAD"`:
Uninstall plugin đó, rồi dùng `~/.cursor/plugins/local` ở trên. Muốn giữ marketplace
local thì `git init` + commit ít nhất một lần trong `prompt-ai-marketplace/`, sau đó
add lại.

Team marketplace (Teams/Enterprise): **Dashboard → Plugins → Add Marketplace**, trỏ
Git repo có `.cursor-plugin/marketplace.json`. Developer cài từ **Customize**.

Fallback skill-only:

Workspace:

```bash
mkdir -p /path/to/project/.cursor/skills
cp -R ./prompt-toolkit/skills/* /path/to/project/.cursor/skills/
```

User-level:

```bash
mkdir -p ~/.cursor/skills
cp -R ./prompt-toolkit/skills/* ~/.cursor/skills/
```

Cursor cũng đọc `.agents/skills/`, `.claude/skills/` và `.codex/skills/`. Xem
[Cursor Agent Skills](https://cursor.com/docs/skills) và
[Cursor Plugins](https://cursor.com/docs/plugins).

Cursor có built-in `/review`. Skill `review` của plugin là Elite Code Auditor
read-only; gọi rõ “use the prompt-toolkit review skill” nếu slash command bị nhầm
built-in. Mọi skill dùng `disable-model-invocation: true` — chỉ chạy khi user gọi
`/skill-name`, không auto-trigger.

### GitHub Copilot

Copilot (VS Code agent mode, Copilot CLI, Copilot app, cloud agent) đọc Agent Skills
từ `.github/skills/`, `.agents/skills/`, `.claude/skills/` (project) và
`~/.copilot/skills/`, `~/.agents/skills/` (user). Gọi `/e2e` hoặc `/teamwork-preview`
trong chat.

Workspace:

```bash
mkdir -p /path/to/project/.github/skills
cp -R ./prompt-toolkit/skills/* /path/to/project/.github/skills/
```

User-level:

```bash
mkdir -p ~/.copilot/skills
cp -R ./prompt-toolkit/skills/* ~/.copilot/skills/
```

Nếu repo đã public, `gh skill` (GitHub CLI ≥ 2.90) có thể cài từng skill:

```bash
gh skill preview OWNER/REPO e2e
gh skill install OWNER/REPO e2e --scope user
```

Trong VS Code: gõ `/` trong Copilot Chat, hoặc **Chat: Open Customizations** →
Skills. Xem [Use Agent Skills in VS Code](https://code.visualstudio.com/docs/agent-customization/agent-skills)
và [About agent skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills).

### Google Antigravity

Native plugin install cho Antigravity CLI/IDE hiện hành:

```bash
agy plugin validate "$(pwd)/prompt-toolkit"
agy plugin install "$(pwd)/prompt-toolkit"
agy plugin list
```

Plugin native cung cấp đủ 6 skill. Restart hoặc mở
conversation mới sau khi cài để refresh catalog.
Xem [Antigravity Plugins](https://antigravity.google/docs/plugins) và
[Asynchronous Subagents](https://antigravity.google/docs/subagents).

Fallback skill-only nếu host cũ không có `agy plugin`:

Workspace-level:

```bash
mkdir -p /path/to/project/.agents/skills
cp -R ./prompt-toolkit/skills/* /path/to/project/.agents/skills/
```

Global:

```bash
mkdir -p ~/.gemini/config/skills
cp -R ./prompt-toolkit/skills/* ~/.gemini/config/skills/
```

Mở hoặc reload workspace, rồi nhắc rõ “Use the `teamwork-preview` skill to ...” hoặc
“Use the `e2e` skill to ...”. Antigravity tự
discover skill theo `name` và `description`. Bản hiện hành ưu tiên `.agents/skills/`
cho workspace và vẫn tương thích `.agent/skills/` cũ. Xem
[Antigravity Agent Skills](https://antigravity.google/docs/skills).

Trên Antigravity, `/teamwork-preview` không namespace vẫn được dành cho native
command. Với skill plugin, mở `/skills`, chọn `teamwork-preview` từ source
`prompt-toolkit`, hoặc yêu cầu agent dùng “prompt-toolkit teamwork-preview skill”.
Chỉ dùng `/prompt-toolkit:teamwork-preview` nếu chính UI hiện cú pháp đó. Nếu native
controller đã chạy, reuse và áp dụng Team Sheet; không mở team thứ hai.

### OpenCode

Project-level:

```bash
mkdir -p /path/to/project/.opencode/skills
cp -R ./prompt-toolkit/skills/* /path/to/project/.opencode/skills/
```

Global:

```bash
mkdir -p ~/.config/opencode/skills
cp -R ./prompt-toolkit/skills/* ~/.config/opencode/skills/
```

OpenCode cũng discover `.agents/skills/` và `.claude/skills/`. Nếu skill không xuất
hiện, kiểm tra `permission.skill` trong `opencode.json` không đặt `e2e` hoặc
`teamwork-preview` thành `deny`, sau đó yêu cầu agent dùng đúng skill. Xem
[OpenCode Agent Skills](https://opencode.ai/docs/skills).

### Grok Build

Cài local marketplace/plugin:

```bash
grok plugin install "$(pwd)" --trust
grok inspect
```

Nếu đã cài bản cũ từ cùng local path, uninstall/reinstall để refresh snapshot:

```bash
grok plugin uninstall prompt-toolkit --confirm --keep-data
grok plugin install "$(pwd)" --trust
```

`grok inspect` phải hiển thị `prompt-toolkit` với 6 skills.

### Gemini CLI

Workspace (ưu tiên `.agents/skills/`):

```bash
mkdir -p /path/to/project/.agents/skills
cp -R ./prompt-toolkit/skills/* /path/to/project/.agents/skills/
```

User-level:

```bash
mkdir -p ~/.gemini/skills
cp -R ./prompt-toolkit/skills/* ~/.gemini/skills/
```

Hoặc link local plugin:

```bash
gemini skills link "$(pwd)/prompt-toolkit/skills/e2e" --scope user
gemini skills list
```

Gọi `/e2e <task>` hoặc `/teamwork-preview <task>`. Xem
[Gemini CLI Agent Skills](https://geminicli.com/docs/cli/skills/).

### Windsurf

Workspace:

```bash
mkdir -p /path/to/project/.windsurf/skills
cp -R ./prompt-toolkit/skills/* /path/to/project/.windsurf/skills/
```

User-level:

```bash
mkdir -p ~/.codeium/windsurf/skills
cp -R ./prompt-toolkit/skills/* ~/.codeium/windsurf/skills/
```

Reload window, rồi gọi `/teamwork-preview` hoặc yêu cầu dùng đúng skill.

### Hermes Agent

Local install cho user hiện tại:

```bash
mkdir -p ~/.hermes/skills
cp -R ./prompt-toolkit/skills/* ~/.hermes/skills/
hermes skills list
```

Khi repository đã public trên GitHub, có thể cài riêng skill mà không copy:

```bash
hermes skills inspect OWNER/REPO/prompt-toolkit/skills/e2e
hermes skills install OWNER/REPO/prompt-toolkit/skills/e2e
hermes skills inspect OWNER/REPO/prompt-toolkit/skills/teamwork-preview
hermes skills install OWNER/REPO/prompt-toolkit/skills/teamwork-preview
```

Hermes chạy security scan với skill từ community source. Sau khi cài, dùng
`/teamwork-preview <task>`, `/e2e <task>` hoặc gọi tự nhiên tên skill. Xem
[Hermes Skills System](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/).

### ZCode

Cài toàn bộ plugin:

1. Mở một workspace.
2. Vào **Settings → Plugins → Marketplace**.
3. Nhấn `+`, nhập local path tới root `prompt-ai-marketplace/` hoặc GitHub URL.
4. Chọn **prompt-toolkit**, nhấn **Get**, bảo đảm plugin đang enabled.
5. Gõ `/` và chọn `prompt-toolkit:teamwork-preview` hoặc `prompt-toolkit:e2e`.

Cài riêng skill ở user-level:

```bash
mkdir -p ~/.zcode/skills
cp -R ./prompt-toolkit/skills/e2e ~/.zcode/skills/
cp -R ./prompt-toolkit/skills/teamwork-preview ~/.zcode/skills/
```

Sau đó vào **Settings → Skills → Refresh**. ZCode cũng có thể import skill từ
Claude Code/Codex bằng **Settings → Skills → Import** ở chế độ symlink hoặc copy.
Xem [ZCode Plugins](https://zcode.z.ai/en/docs/plugin) và
[ZCode Skills](https://zcode.z.ai/en/docs/skill).

## Các host SKILL.md khác

| Host / chuẩn | Project-level | User-level |
|---|---|---|
| Agent Skills generic | `.agents/skills/` | `~/.agents/skills/` |
| Cursor | `.cursor/skills/` | `~/.cursor/skills/` |
| GitHub Copilot | `.github/skills/` | `~/.copilot/skills/` |
| Claude-compatible direct skills | `.claude/skills/` | `~/.claude/skills/` |
| Gemini CLI | `.gemini/skills/` hoặc `.agents/skills/` | `~/.gemini/skills/` |
| Windsurf | `.windsurf/skills/` | `~/.codeium/windsurf/skills/` |
| Gemini/Antigravity | `.agents/skills/` | `~/.gemini/config/skills/` |
| OpenCode | `.opencode/skills/` | `~/.config/opencode/skills/` |
| ZCode | import từ external agent | `~/.zcode/skills/` |

Copy nguyên từng thư mục `skills/<name>/` (kèm `references/` nếu có). Không paste
nhiều `SKILL.md` vào một file instructions chung vì sẽ làm mất progressive
disclosure và metadata trigger. Host khác: ưu tiên vị trí trong tài liệu của chính
host.

## Validation và phát hành

Validate toàn bộ SKILL.md bằng validator của skill-creator:

```bash
for skill in ./prompt-toolkit/skills/*; do
  python3 /path/to/skill-creator/scripts/quick_validate.py "$skill"
done
python3 -m unittest ./prompt-toolkit/tests/test_teamwork_preview.py
```

Validate JSON manifests:

```bash
python3 -m json.tool marketplace.json >/dev/null
python3 -m json.tool .agents/plugins/marketplace.json >/dev/null
python3 -m json.tool .claude-plugin/marketplace.json >/dev/null
python3 -m json.tool .cursor-plugin/marketplace.json >/dev/null
python3 -m json.tool prompt-toolkit/.codex-plugin/plugin.json >/dev/null
python3 -m json.tool prompt-toolkit/.claude-plugin/plugin.json >/dev/null
python3 -m json.tool prompt-toolkit/.cursor-plugin/plugin.json >/dev/null
python3 -m json.tool prompt-toolkit/.grok-plugin/plugin.json >/dev/null
python3 -m json.tool prompt-toolkit/.zcode-plugin/plugin.json >/dev/null
python3 -m json.tool prompt-toolkit/plugin.json >/dev/null
```

Nếu có Claude Code CLI:

```bash
claude plugin validate .
claude plugin validate ./prompt-toolkit
```

Khi phát hành thay đổi:

1. Cập nhật skill và README.
2. Tăng cùng một semantic base version trong `.claude-plugin/marketplace.json`,
   `.cursor-plugin/marketplace.json`,
   `prompt-toolkit/.claude-plugin/plugin.json`,
   `prompt-toolkit/.cursor-plugin/plugin.json`,
   `prompt-toolkit/.codex-plugin/plugin.json`,
   `prompt-toolkit/.grok-plugin/plugin.json` và
   `prompt-toolkit/.zcode-plugin/plugin.json`, cùng với
   `prompt-toolkit/plugin.json` cho Agent Plugins / Antigravity / Cursor. Local Codex development có thể thêm
   một build metadata suffix `+codex.<cachebuster>` mà không đổi base version.
3. Chạy validators.
4. Refresh/reinstall plugin hoặc copy lại skill ở host dùng local folder.

## Security notes

- Đọc `SKILL.md` trước khi cài từ repository không tin cậy; skill là operational
  instructions và chạy với quyền của agent host.
- `e2e` không tự thêm dependency, đổi auth/permission, migration/schema hoặc public
  contract nếu chưa có explicit approval.
- `review` luôn read-only. `e2e` chỉ giữ Stage Review read-only rồi chuyển rõ ràng
  sang Stage Engineer; không làm suy yếu read-only contract của skill `review`.
- Teamwork: Coordinator không làm thay toàn bộ team. Domain Builder chỉ sửa path
  mình Owns. Verifier chạy checks; Critic/Auditor không repair. Bắt buộc cổng duyệt
  Team Sheet và independent verification trước khi bàn giao.
- Không chấp nhận specialist self-attestation làm proof; Coordinator kiểm tra lại
  workspace và shared artifacts.
- Không commit absolute path, API key, token, secrets hoặc PII vào skill/manifest.

## Nguồn nội dung

Các skill prompt/engineering được phát triển từ `ASK.md`, `ASK_GOAL.md`, `REVIEW.md`
và `AGENTS.md` trong workspace `PROMPT AI`; `e2e` kết hợp behavioral core của
`review`, `ask` và `engineer`. `teamwork-preview` được port từ folder
`teamwork-preview/` trong workspace `PROMPT AI`: Coordinator / Hiring Manager, Team
Sheet, cổng duyệt bắt buộc, launch native-or-sequential, independent Verifier rồi
Critic/Auditor.
