# Prompt AI Marketplace

Cursor marketplace với plugin `prompt-toolkit` (6 skill: `ask`, `goal`, `review`, `engineer`, `e2e`, `teamwork-preview`).

Repo: [github.com/Kaine270802/prompt-ai-marketplace](https://github.com/Kaine270802/prompt-ai-marketplace)

## Cursor — thêm marketplace

### GitHub (khuyến nghị)

1. Customize → Plugins / Marketplace → **Add Marketplace**.
2. Dán:

```text
https://github.com/Kaine270802/prompt-ai-marketplace
```

3. Install **prompt-toolkit** (user hoặc project).
4. **Developer: Reload Window**.
5. Gọi `/ask`, `/goal`, `/review`, `/engineer`, `/e2e`, `/teamwork-preview`.

Team / Enterprise: **Dashboard → Plugins → Add Marketplace** → Import from Repo, cùng URL.

### Local path (dev)

Folder local **phải là git repo có commit** (Cursor chạy `git ls-remote … HEAD` trên `file://` path).

1. Customize → Plugins / Marketplace → **Add Marketplace**.
2. Dán path:

```text
D:\Macbook\PROMPT AI\prompt-ai-marketplace
```

3. Install **prompt-toolkit**, rồi Reload Window.

Nếu plugin cũ đang báo `Failed to resolve git ref "HEAD"`: **Uninstall**, xóa marketplace đó, add lại URL GitHub hoặc path trên.

Manifest Cursor: `.cursor-plugin/marketplace.json` → plugin `prompt-toolkit/`.

Chi tiết host khác: [prompt-toolkit/README.md](prompt-toolkit/README.md).
