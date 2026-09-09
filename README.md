# prompt-ai-marketplace

Marketplace chứa plugin **`prompt-toolkit`** (v2.7.0): bộ 7 Agent Skills dùng chung cho
nhiều coding agent — từ nâng cấp prompt/goal, review read-only, implementation,
deep reasoning, đến delivery end-to-end và autonomous agent teamwork. Tối ưu output layout
dễ đọc cho tiếng Việt.

## Plugin bên trong

| Plugin | Version | Skills | Mô tả |
|---|---|---|---|
| `prompt-toolkit` | 2.7.0 | `ask`, `goal`, `review`, `engineer`, `boost`, `e2e`, `teamwork-preview` | Prompt/goal refinement, read-only audit, engineering có test, deep reasoning, end-to-end delivery, teamwork có duyệt + audit độc lập |

| Skill | Làm gì | Kết quả |
|---|---|---|
| `ask` | Nghiên cứu context, nâng cấp raw prompt | 1 prompt copy-ready; không thực thi task |
| `goal` | Làm rõ outcome, scope, success criteria | 1 goal copy-ready + auto-lưu `docs/goal/GOAL_*.txt` |
| `review` | Audit/diagnose ở chế độ read-only tuyệt đối | Findings có evidence `path:line`; mọi fix đều `NOT APPLIED` |
| `engineer` | Làm coding task theo Phase 0→4 | Thay đổi nhỏ nhất kèm tests + verification |
| `boost` | Deep reasoning cho bug khó: hypotheses → investigate → patch → falsify | Root cause có repro test; patch tối thiểu qua adversarial check |
| `e2e` | Ghép `review → ask → engineer → verify` | Task hoàn thành, direct hoặc teamwork |
| `teamwork-preview` | Sentinel + blueprint, Team Sheet + DAG, duyệt, specialists cách ly, Success Auditor | Team Sheet theo template + sign-off `APPROVED` từng milestone |

`ask`, `goal`, `review`, `engineer`, `e2e`, `teamwork-preview` là **manual-only**
(`disable-model-invocation: true`): chỉ chạy khi bạn gọi rõ tên skill.
`boost` chạy khi bạn gọi `/boost` hoặc nêu rõ cần deep thinking / verification chặt.

## Cài nhanh

Chi tiết đầy đủ theo từng host nằm ở [`prompt-toolkit/README.md`](prompt-toolkit/README.md).
Tóm tắt:

```bash
# Claude Code
claude plugin marketplace add "$(pwd)"
claude plugin install prompt-toolkit@prompt-ai-marketplace

# Codex
codex plugin marketplace add "$(pwd)"
codex plugin add prompt-toolkit@prompt-ai-marketplace

# Copy thủ công (Copilot / OpenCode / Gemini / Windsurf / Hermes / ZCode)
cp -R ./prompt-toolkit/skills/* <skills-dir-cua-host>/
```

| Host | Skills dir thủ công |
|---|---|
| GitHub Copilot | `.github/skills/` hoặc `~/.copilot/skills/` |
| OpenCode | `.opencode/skills/` hoặc `~/.config/opencode/skills/` |
| Gemini CLI | `.agents/skills/` hoặc `~/.gemini/skills/` |
| Windsurf | `.windsurf/skills/` |
| ZCode | `~/.zcode/skills/` (+ Settings → Skills → Refresh) |
| Cursor | `~/.cursor/plugins/local/` (symlink, rồi Reload Window) |
| Antigravity | `agy plugin install "$(pwd)/prompt-toolkit"` |

## Cách dùng

```text
/ask Sửa bug login kẹt loading khi API trả 401
/goal Tăng tỉ lệ hoàn thành onboarding trong 60 ngày
/review Vì sao hàm handleLogin() kẹt loading ở nhánh lỗi?
/engineer Sửa lỗi login 401 + thêm regression test
/e2e Sửa lỗi login bị kẹt loading khi API trả 401 và thêm regression test
/teamwork-preview Xây feature này bằng một team có independent audit
```

- Host dùng namespace: `/prompt-toolkit:e2e`, `/prompt-toolkit:teamwork-preview`.
- Host dùng `$skill`: `$e2e`, `$teamwork-preview`.
- Trên Antigravity, native `/teamwork-preview` được ưu tiên nếu đã sở hữu session;
  skill plugin thì chọn trong `/skills` theo source `prompt-toolkit`.

## Điểm khác biệt

- **Đào sâu vấn đề thực:** `ask`/`goal` suy luận intent ẩn, tách OUTCOME khỏi OUTPUT;
  `review`/`engineer` rank nỗi đau theo user-impact, chạy 5-Whys silent, chốt bằng
  `Assumption` + pre-mortem 1 dòng. Depth-probe ≤1 vòng, placeholder ≤3.
- **An toàn theo thiết kế:** `review` read-only tuyệt đối (mọi fix là proposal
  `NOT APPLIED`); `engineer` mặc định CHECK MODE khi xem trước, chỉ sửa khi có
  `/engineer` + approve; không tự thêm dependency, đổi auth/permission hay phá
  contract khi chưa được duyệt.
- **Layout tiếng Việt dễ quét:** câu ngắn, ý chính đầu câu, kết quả `review`/`engineer`
  render theo heading `## 1..8` + bảng file checklist, mọi claim cite `path:line`.
- **Teamwork có kỷ luật:** Team Sheet `Role | Specialty | Owns | Inputs | Outputs |
  Success Criteria`, cổng duyệt bắt buộc (yes/approve/go), Verifier độc lập rồi mới
  tới Critic/Auditor. Task đơn giản thì làm thẳng, không ép team.

## Cấu trúc repository

```text
prompt-ai-marketplace/
├── marketplace.json
├── README.md
└── prompt-toolkit/
    ├── plugin.json
    ├── README.md                  # hướng dẫn chi tiết từng host
    └── skills/
        ├── ask/SKILL.md
        ├── goal/SKILL.md
        ├── review/SKILL.md
        ├── engineer/SKILL.md
        ├── e2e/SKILL.md
        └── teamwork-preview/
            ├── SKILL.md
            └── references/example-teams.md
```

## Phát triển

```bash
python3 -m json.tool marketplace.json >/dev/null
for skill in ./prompt-toolkit/skills/*; do
  python3 /path/to/skill-creator/scripts/quick_validate.py "$skill"
done
```

Khi sửa skill: cập nhật `prompt-toolkit/README.md`, tăng cùng một semantic version
trong các manifest, chạy validators, rồi reinstall plugin hoặc copy lại skill ở host
dùng folder local. Chi tiết xem mục Validation và phát hành trong
[`prompt-toolkit/README.md`](prompt-toolkit/README.md).
