# Prompt AI Marketplace

Local Cursor marketplace với plugin `prompt-toolkit` (6 skill: `ask`, `goal`, `review`, `engineer`, `e2e`, `teamwork-preview`).

## Cursor — thêm marketplace

Folder này **phải là git repo có commit** (Cursor chạy `git ls-remote … HEAD` trên `file://` path).

1. Customize → Plugins / Marketplace → **Add Marketplace**.
2. Dán path:

```text
D:\Macbook\PROMPT AI\prompt-ai-marketplace
```

3. Install **prompt-toolkit** (user hoặc project).
4. **Developer: Reload Window**.
5. Gọi `/ask`, `/goal`, `/review`, `/engineer`, `/e2e`, `/teamwork-preview`.

Nếu plugin cũ đang báo `Failed to resolve git ref "HEAD"`: **Uninstall**, xóa marketplace đó, add lại path trên.

Manifest Cursor: `.cursor-plugin/marketplace.json` → plugin `prompt-toolkit/`.

Chi tiết host khác: [prompt-toolkit/README.md](prompt-toolkit/README.md).
