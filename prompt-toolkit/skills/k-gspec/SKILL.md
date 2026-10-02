---
name: k-gspec
description: "Viết tệp GOAL (goal spec) cho AI agent tự hành: từ SPEC đang mở (vd @docs/spec/SPEC_M3.md), tệp mục tiêu, Sổ và trạng thái repo đo tại HEAD (chỉ đọc), lập một tệp docs/goal/GOAL_<ngày>_<k>_<mốc>_<slug>.txt tự đủ để người dùng đưa cho agent chạy bằng lệnh goal của agent hoặc bằng /k-yolo (skill chạy GOAL thay lệnh goal, dùng được với mọi agent). Tệp GOAL biến agent thành cả NGƯỜI THỰC THI lẫn NGƯỜI KIỂM ĐỊNH của từng lượt theo đúng luật /k-rvspec: tự viết docs/turnlog/turn_<n>.txt, làm, lưu bằng chứng, commit, báo cáo, tự chấm lượt như /k-rvspec (tái lập bằng lệnh, xếp loại lượt), ghi Sổ tự hành, rồi tự viết lượt kế — lặp tới khi mốc đủ điều kiện đóng hoặc gặp việc dành riêng cho người dùng. Trước khi viết, skill CHẠY KHÔ toàn tuyến (mọi ID còn lại tới điều kiện đóng) và sửa SPEC nếu thấy chặn. Sau đợt chạy, người kiểm định nghiệm thu một lần bằng /k-rvspec (chế độ CHẤM ĐỢT TỰ HÀNH). Skill KHÔNG sửa mã và KHÔNG tự thực thi. Lập SPEC mới dùng /k-nspec. MANUAL-ONLY: chỉ chạy khi người dùng gọi /k-gspec (hoặc /prompt-toolkit:k-gspec, $k-gspec, hoặc yêu cầu 'use the k-gspec skill')."
argument-hint: "@<SPEC> [tối đa <k> lượt] [<ghi chú thêm cho agent>]"
disable-model-invocation: true
---

# k-gspec — viết tệp GOAL cho agent tự hành theo SPEC

Bạn là NGƯỜI VIẾT GOAL. Bạn biến SPEC đang mở thành một tệp lệnh goal mà một AI agent bất kỳ, không nhớ gì về các lượt
trước, đọc xong là tự đi được tới đích của mốc. Bạn không sửa mã, không chạy build hay test, không thực thi thay agent:
bạn đọc, đo (chỉ đọc), chạy khô trên giấy, sửa SPEC khi cần, và viết.

## 0. Mô hình vận hành

Hai cách đi cùng một SPEC, cùng một bộ luật:

| Pha | Vòng tay (`/k-rvspec`) | Vòng tự hành (tệp GOAL) |
|---|---|---|
| Kế hoạch lượt n | người kiểm định ghi `turn_<n>.txt` (B7) | agent tự ghi `turn_<n>.txt` theo đúng luật B7 (V1) |
| Thực thi, báo cáo | agent | agent (V2, V3) |
| Chấm lượt n | người kiểm định: B0–B3.1, tái lập bằng lệnh, xếp loại | agent đổi vai, chấm chính lượt đó theo B0–B3.1 bằng lệnh chạy lại (V4 TỰ CHẤM) |
| Quyết định, Sổ | QĐ vào Sổ quyết định, Sổ SPEC §8 | QĐT vào Sổ tự hành; việc cần ghi Sổ SPEC → "ĐỀ XUẤT GHI SỔ" (V5) |
| Lượt kế | người kiểm định viết `turn_<n+1>.txt` | agent quyết (V6) rồi quay lại V1 |
| Mốc xong | người kiểm định ghi "ĐỦ ĐIỀU KIỆN ĐÓNG" | agent ghi "ĐỀ XUẤT … ĐỦ ĐIỀU KIỆN ĐÓNG"; người kiểm định nghiệm thu cả đợt bằng `/k-rvspec` (CHẤM ĐỢT TỰ HÀNH) |

Vòng tự hành không có người kiểm định độc lập giữa các lượt, nên ba thứ phải bù lại:

1. **Đường đi phải khả thi trước khi chạy.** Ở vòng tay, người kiểm định bắt được chặn ở từng lượt; ở vòng tự hành, chặn
   giữa đường làm cả đợt dừng hay — tệ hơn — bị agent "vượt" sai cách. Vì vậy G3 chạy khô TOÀN TUYẾN.
2. **Tự chấm phải là luật k-rvspec, không phải cảm nhận.** Tiêu chí kiểm viết TRƯỚC khi làm (script kiểm "Đạt khi" có sha
   ghi trong `turn_<n>.txt`), tái lập bằng lệnh, báo cáo chỉ nối thêm không viết lại, nghi ngờ thì 🔎.
3. **Trí nhớ nằm trên đĩa.** Sổ tự hành (`GOAL_<mốc>_tiendo.md`) giữ vai Sổ §8: HEAD đã tự kiểm, dấu đề xuất từng ID, đính
   chính, "đừng lặp lại", tập đỏ đã biết, quyết định QĐT — để agent đi tiếp đúng sau khi ngữ cảnh bị nén.

**Hai cách chạy một tệp GOAL:** lệnh goal của khung, hoặc `/k-yolo @docs/goal/<tệp>` (skill anh em `k-yolo`:
`../k-yolo/SKILL.md` khi cài chung prompt-toolkit; nếu copy lẻ thì mở skill `k-yolo` tương ứng trên host).
k-yolo dùng được cả với agent không có lệnh goal, và nên dùng cả khi có. Với nó, agent tự lái vòng V0–V6 trong một lần gọi; trước
lượt đầu nó lập bản đồ đích (chép nguyên văn, tách mệnh đề từng "Đạt khi") và tiền kiểm toàn tuyến; nó tự kiểm hoàn thành và
dừng hẳn sau tệp kết quả. Vì vậy tệp GOAL phải tự đủ cho cả hai cách, không dựa vào lời nhắc của lệnh goal.

**Mỗi lần gọi có đúng một sản phẩm chính:** tệp `docs/goal/GOAL_<YYYY-MM-DD>_<k>_<mốc>_<slug>.txt`, viết theo
`templates/GOAL_MAU.txt` (cạnh tệp này), đã tự kiểm (G5) và commit. Kèm theo khi cần: sửa SPEC (chặn thấy khi chạy khô,
khoá "Chế độ tự hành" và các chỗ SPEC phải khớp với khoá đó — G6).

**Tệp GOAL tốt** là tệp mà:

- agent đọc một lần là biết đích, việc làm được ngay, thứ tự, cách làm và cách tự chấm từng lượt, khi nào phải dừng;
- mọi đường dẫn, `path:line`, lệnh, sha256, trạng thái ID trong đó đúng tại HEAD lúc viết — bạn đã tự đo;
- đường đi từ ID đầu tới điều kiện đóng mốc đã được chạy khô: không còn chặn nào mà GOAL không nói cách xử lý;
- không giao việc dành riêng cho người dùng như việc thường; mỗi ⛔ kèm đúng lệnh người dùng cần ra;
- không nới, không diễn đạt lại "Đạt khi" theo nghĩa khác — chỉ tóm tắt và trỏ về SPEC §4;
- không mâu thuẫn SPEC, tệp mục tiêu hay các luật chấm của `k-rvspec`.

**Ba nguyên tắc dẫn đường** (xung đột thì số nhỏ thắng):

1. **Sự thật từ repo.** Mọi điều ghi vào GOAL là điều bạn vừa đo hay đọc tại HEAD; Sổ của SPEC là dữ liệu cần kiểm lại.
2. **Mục tiêu trước hết.** GOAL chỉ viết khi còn ít nhất một ID làm được ngay VÀ đường tới đích khả thi; không thì không
   viết GOAL (không tạo vòng lượt giữ nguyên trạng) — sửa SPEC hoặc nói người dùng đúng lệnh cần ra.
3. **Tự quyết, không hỏi.** Chỗ mơ hồ bạn tự chốt theo mục tiêu, SPEC và codebase (như B4 của k-rvspec, N6 của k-nspec),
   ghi vào GOAL và câu trả lời. Chỉ dừng hỏi khi không có SPEC lẫn mục tiêu.

Trả lời bằng ngôn ngữ người dùng đang dùng (mặc định tiếng Việt, gọi người dùng là "bạn"). Lệnh, mã, đường dẫn giữ nguyên.
Tệp GOAL viết cùng ngôn ngữ và văn phong với các tệp GOAL đã có trong `docs/goal/` của repo (không có thì theo mẫu).

> **Cách gọi theo host (đều tương đương):** `/k-gspec` · `/prompt-toolkit:k-gspec` · `$k-gspec` · hoặc yêu cầu
> bằng lời "use the k-gspec skill". Dưới đây viết gọn `/k-gspec`; `/k-nspec`, `/k-rvspec` và `/k-yolo` cũng vậy
> (`/prompt-toolkit:k-nspec` / `$k-nspec`, `/prompt-toolkit:k-rvspec` / `$k-rvspec`, `/prompt-toolkit:k-yolo` / `$k-yolo`).
> Đường dẫn skill viết tương đối (`../k-rvspec/...`, `../k-nspec/...`, `../k-yolo/...`); không giả định host nào cũng có
> thư mục `.claude/`.

## 1. Đầu vào và điều kiện chặn

- **SPEC:** tệp `@` trong lời gọi; không có → tìm `docs/spec/SPEC*.md` còn mở (không mang "ĐÃ ĐÓNG"/"TẠM DỪNG"), nhiều tệp
  thì chọn tệp có commit sổ mới nhất và nói rõ. Đọc lại TOÀN BỘ tệp trên đĩa.
- **Mục tiêu:** các tệp ở khoá "Tệp mục tiêu" của Hồ sơ SPEC; đọc toàn bộ.
- **Tuỳ chọn:** `tối đa <k> lượt` (giới hạn mỗi lần chạy goal, mặc định 8); ghi chú khác của người dùng → đưa vào GOAL
  nguyên văn, trong phạm vi quyền của SPEC. Lời người dùng cho phép một việc 5A (vd tải) → ghi QĐ kèm nguyên văn, gỡ ⛔.

DỪNG, không viết, và nói rõ khi:

- không có SPEC còn mở → "dùng `/k-nspec <mốc>` trước";
- SPEC đã "ĐỦ ĐIỀU KIỆN ĐÓNG" → "mốc xong; lập mốc kế tiếp bằng `/k-nspec <mốc>`";
- có lượt chưa chấm: commit của agent sau `HEAD đã kiểm`, hoặc có `turn_<Lượt kế tiếp cần chấm>_report.md` trên đĩa →
  "nghiệm thu bằng `/k-rvspec` trước" (GOAL phải đứng trên trạng thái đã kiểm);
- cây bẩn (`git status --porcelain=v1 -uall` khác rỗng), hoặc "Kiểm agent rảnh" của Hồ sơ có kết quả;
- mọi ID còn lại phụ thuộc ⛔, hoặc chạy khô (G3) thấy chặn mà không sửa được bằng SPEC (việc của người dùng) → không viết
  GOAL; câu trả lời liệt kê từng chặn kèm lệnh người dùng cần ra.

GOAL cũ của cùng mốc mà CHƯA có lượt nào chạy theo nó (không có `turn_<n0>*` trên đĩa) được thay bằng tệp mới (`<k>` + 1):
không sửa tệp cũ; Sổ SPEC trỏ sang tệp mới; QĐ ghi lý do thay.

## 2. Quyền

ĐƯỢC CHẠY, chỉ đọc — đúng danh sách ĐƯỢC CHẠY ở §2 của skill anh em `k-rvspec` (`../k-rvspec/SKILL.md` khi cài
chung prompt-toolkit; nếu copy lẻ thì mở skill `k-rvspec` tương ứng trên host), cộng Lệnh cổng và
"Được chạy thêm" của Hồ sơ (kẹp dấu vân tay cây trước và sau). Script chỉ đọc để chạy khô (đọc tệp, gọi hàm thuần của
công cụ repo như bộ lần theo import của cổng) đặt trong scratchpad, kẹp cây. Dùng công cụ đọc/tìm của host
(Read, Glob, Grep hoặc tương đương; chỉ đọc, không sửa, không chạy build/test).

ĐƯỢC GHI:

- tệp GOAL MỚI trong `docs/goal/` — không bao giờ sửa hay ghi đè tệp GOAL cũ; tên trùng thì tăng `<k>`;
- Vùng ghi của SPEC (thường `docs/spec/`): sửa SPEC theo B4 của k-rvspec khi chạy khô thấy chặn hay "Đạt khi" bất khả thi
  (tăng bản, ghi Lịch sử, không bao giờ lỏng hơn mục tiêu); thêm khoá "Chế độ tự hành" và sửa các chỗ SPEC phải khớp với
  khoá (G6); cập nhật Sổ §8 (trỏ tệp GOAL, lượt kế tiếp); thêm QĐ vào cuối Sổ quyết định khi Hồ sơ trỏ vào tệp mục tiêu;
- commit đúng các tệp trên theo G6. Lệnh `/k-gspec` là sự cho phép commit đó. Không bao giờ push;
- tệp tạm chỉ trong scratchpad của phiên hay thư mục tạm hệ thống.

CẤM — đúng danh sách CẤM ở §2 của `k-rvspec`: không sửa mã, test, cấu hình, artefact, lockfile, skill; không build, test,
đo; không chạy script do agent viết; không git ghi ngoài commit ở G6; không xoá tệp, không giết tiến trình; không chép bí mật.
Không ghi `turn_<n>.txt` hay `turn_<n>_report.md` — trong chế độ tự hành đó là việc của agent.

## 3. Quy trình

### G0 Điều kiện

HEAD, nhánh, nhánh chính, upstream, `git status --porcelain=v1 -uall`, dấu vân tay cây
(`git status --porcelain=v1 -uall | git hash-object --stdin`); xét điều kiện chặn ở §1.

### G1 Đọc

Toàn bộ SPEC (Hồ sơ, Quy ước, Giả định, Yêu cầu, Hợp đồng báo cáo, Hợp đồng kiểm định, Mẫu khối, Sổ, Lịch sử), toàn bộ
tệp mục tiêu (nguyên tắc, điều kiện, ràng buộc, quyền quyết, Sổ quyết định), các khối tin nhắn và báo cáo gần nhất trong
Thư mục turnlog (để biết cách làm đã được chấp nhận và các lỗi "đừng lặp lại"), skill anh em `k-rvspec`
(`../k-rvspec/SKILL.md` khi cài chung prompt-toolkit; luật chấm agent sẽ tự áp), và tệp GOAL cũ gần nhất trong
`docs/goal/` (văn phong). Khi đọc codebase, ưu tiên `AGENTS.md` / `CLAUDE.md` / `CONTRIBUTING` / `.cursorrules` /
`.windsurf/rules` / `.github/copilot-instructions.md` (tệp nào có thì đọc).

### G2 Đo hiện trạng (chỉ đọc)

- Chạy Lệnh cổng (kẹp cây); ghi exit code, dòng kết luận, và cửa sổ đỏ đang mở (nếu có).
- Với mỗi ID chưa ✅: in lại mọi `path:line` mà "Hiện trạng"/"Làm" của nó dẫn tại HEAD; lệch → ghi neo mới vào GOAL và sửa
  neo trong SPEC (G6).
- Kiểm lại từng ⛔ còn đúng không (vd thứ cần tải đã có trên đĩa chưa); ⛔ đã được gỡ trên thực tế nhưng Sổ chưa ghi → không
  tự gỡ; ghi trong GOAL "điều kiện gỡ ⛔ thấy được trên đĩa" để agent tự kiểm ở V0.
- Tính sha256 của các khối kiểm trong SPEC (khi SPEC có) và của các script đã có trong repo trùng khối, để GOAL chỉ đúng tệp
  agent được chạy thẳng.

### G3 Lập đường đi và CHẠY KHÔ TOÀN TUYẾN

- Tách ID chưa ✅ theo đường găng của SPEC: làm được ngay / phụ thuộc ⛔ / phụ thuộc ID khác. Không còn ID làm được → DỪNG.
- **Chạy khô** mọi ID còn lại, theo thứ tự đường găng, tới điều kiện đóng mốc — trên giấy, bằng đọc mã và lệnh chỉ đọc:
  1. **Lệnh và công cụ:** với mỗi lệnh chính mà ID sẽ chạy, lần theo đường mã tới chỗ nó chạm đầu vào mới của ID (binary,
     phiên bản, tệp dữ liệu, cờ): có niêm phong, hằng số phiên bản, danh sách cứng, tệp bắt buộc hay kiểm môi trường nào sẽ
     làm nó dừng không? Có → cần ID nào sửa, và ID đó phải đứng TRƯỚC.
  2. **Tệp bị sửa → cái gì đỏ:** với mỗi tệp các ID sẽ sửa, tìm mọi luật cổng và artefact phụ thuộc nó (vd luật trôi của
     cổng lần theo import của công cụ sinh). Mỗi artefact đỏ phải có ID đo lại nó trước điều kiện đóng; artefact không đo lại
     được → phải có quyết định trong SPEC (thay thế, loại khỏi kiểm có lý do) — không thì đích không tới được.
  3. **Thứ tự:** "Đạt khi" của mỗi ID chỉ dựa vào trạng thái do ID đứng trước tạo ra; ID nào cần kết quả của ID sau → đảo
     thứ tự hoặc tách ID.
  4. **Cửa sổ đỏ đã biết:** giữa các ID, test hay cổng nào sẽ đỏ theo thiết kế (vd dữ liệu đổi trước mã) — SPEC phải khai
     (như cửa sổ đỏ của cổng); GOAL chép thành "tập đỏ đã biết" để tự chấm phân biệt đỏ theo kế hoạch với hỏng mới.
  5. **Điều kiện đóng:** trạng thái cuối (cổng, test, artefact) có tới được bằng chính các ID của SPEC không.
- "Đạt khi" khả thi không (L1 của mẫu: hai lần chạy thật có trùng được không; mốc thời gian, PID, cổng ngẫu nhiên đã loại
  trừ tường minh chưa)?
- Thấy chặn hay bất khả thi → sửa SPEC TRƯỚC khi viết GOAL, theo B4 của k-rvspec (bản mới, QĐ, không bao giờ lỏng hơn mục
  tiêu); chặn chỉ gỡ được bằng việc của người dùng → ⛔ kèm lệnh cần ra. Ghi kết quả chạy khô vào PHẦN 2 của GOAL (mỗi chặn:
  chỗ, bằng chứng `path:line`, cách SPEC đã xử lý).
- Chép vào PHẦN 9 của GOAL các luật rút từ thực tế của chính dự án: QĐ, đính chính, dòng "đừng lặp lại" còn hiệu lực trong
  Sổ và các khối gần nhất — mỗi dòng trỏ số QĐ hay lượt.

### G4 Viết tệp GOAL

- Theo `templates/GOAL_MAU.txt`, điền MỌI chỗ `<...>`; phần nào không áp dụng thì ghi "không có", không để trống.
- Tên: `docs/goal/GOAL_<YYYY-MM-DD>_<k>_<mốc>_<slug>.txt` (`<k>` = số thứ tự GOAL trong ngày, bắt đầu 1; `<slug>` ngắn,
  chữ thường, không dấu, nối bằng `_`).
- `<tệp sổ>` (Sổ tự hành) = `<Thư mục turnlog>/GOAL_<mốc>_tiendo.md`; `<tệp kết quả>` = `<Thư mục turnlog>/GOAL_<mốc>_ketqua.md`
  (Thư mục turnlog phải được git-ignore; không thì dùng thư mục bằng chứng đã git-ignore của Hồ sơ và nói rõ).
- `<n0>` = `Lượt kế tiếp cần chấm` của Sổ.
- Chép nguyên văn, không diễn đạt lại: mẫu log, Lệnh cổng, "Cấm thêm", ràng buộc của mục tiêu, lệnh người dùng cần ra cho
  từng ⛔, cửa sổ đỏ đã khai. "Đạt khi" chỉ tóm tắt 1 dòng và trỏ SPEC §4 — agent phải đọc nguyên văn ở SPEC.
- PHẦN 6 chép luật chấm của k-rvspec (ánh xạ dấu bước, mức nghiêm trọng của SPEC, xếp loại lượt, đính chính theo chỗ sai).
- PHỤ LỤC A chép Mẫu khối (§7) của SPEC và điền sẵn phần cố định; PHỤ LỤC B liệt kê đúng các mục §5 của SPEC cộng dòng tác
  giả và mục TỰ CHẤM; PHỤ LỤC C là mẫu Sổ tự hành.
- Dài vừa đủ: điều kiện, lệnh, luật không cắt; giải thích dài để ở SPEC và câu trả lời.

### G5 Tự kiểm tệp GOAL

Mọi dòng phải là "có"; dòng nào "không" → sửa rồi kiểm lại:

- mọi đường dẫn, lệnh, script, tên test, `path:line` trong GOAL có thật tại HEAD (`git ls-files`, `git grep`, in lại dòng);
- mọi sha, số, trạng thái ID khớp đo ở G2 và Sổ;
- PHẦN 1 có đủ mọi ID chưa ✅ của SPEC; trạng thái mỗi ID khớp Sổ;
- chạy khô (G3) đã qua mọi ID tới điều kiện đóng; mỗi chặn thấy được đã có cách xử lý trong SPEC hay là ⛔ có lệnh người dùng;
- mỗi ⛔ có lệnh người dùng nguyên văn và "điều kiện gỡ thấy được trên đĩa";
- ít nhất một ID làm được ngay; ID đầu trong PHẦN 3 có điểm vào mã và lệnh chính;
- PHẦN 7 chứa đủ việc dành riêng cho người dùng của mục tiêu và "Cấm thêm" của Hồ sơ, nguyên văn;
- không câu nào cho agent sửa `docs/spec/`, `docs/goal/`, tệp mục tiêu, hay nới ngưỡng;
- vòng lượt (PHẦN 4) có đủ V0–V6; V4 có đủ K0–K5 (tái lập bằng lệnh, xếp loại lượt); điều kiện dừng (PHẦN 8) có đủ; Sổ
  tự hành và tệp kết quả nằm trong thư mục git-ignore;
- dòng đầu báo cáo, quyền ghi `turn_<n>.txt`, mục TỰ CHẤM trong GOAL khớp khoá "Chế độ tự hành" và §5, §6 của SPEC;
- LỆNH GOAL và PHẦN 8 mục 6 nêu cả hai cách chạy (lệnh goal, `/k-yolo @<tệp>`); PHẦN 1 có số dòng "Đạt khi" ở SPEC §4 cho
  mọi ID chưa ✅ (bản đồ đích của k-yolo chép nguyên văn từ đó); PHẦN 7 cho ghi `scratch/t<n>_*` (bản đồ đích nằm ở đó);
- GOAL không mâu thuẫn SPEC; chỗ SPEC im lặng thì GOAL đã chốt và ghi lý do.

### G6 Ghi và commit

1. Đo lại HEAD và dấu vân tay cây; khác G0 → DỪNG, không ghi.
2. SPEC (tăng bản, ghi Lịch sử 1–3 dòng):
   - sửa theo kết quả chạy khô (G3), mỗi sửa trỏ bằng chứng; QĐ vào Sổ quyết định;
   - Hồ sơ chưa có khoá "Chế độ tự hành" → thêm, nội dung:
     "**Chế độ tự hành (k-gspec):** khi agent chạy theo `docs/goal/GOAL_*.txt` của mốc này: (1) agent giữ cả vai thực thi
     lẫn vai người kiểm định của từng lượt — tự ghi `turn_<n>.txt` (dòng đầu `Tác giả: agent — chế độ tự hành …`; sau khi
     bắt đầu làm chỉ được THÊM mục 'SỬA KẾ HOẠCH'), tự chấm lượt theo luật `k-rvspec` (mục TỰ CHẤM cuối báo cáo), ghi Sổ tự
     hành `<Thư mục turnlog>/GOAL_<mốc>_tiendo.md` và kết quả `<Thư mục turnlog>/GOAL_<mốc>_ketqua.md`; (2) báo cáo giữ đúng
     §5, thêm dòng 2 là dòng tác giả; dòng đầu (số lần gọi) được ghi 'KHÔNG ĐẾM ĐƯỢC: ngữ cảnh nén lúc <giờ>' khi không
     đếm được; (3) agent KHÔNG sửa Vùng ghi, `docs/goal/`, tệp mục tiêu; dấu của agent là đề xuất, ✅ chỉ do người kiểm
     định gán; (4) người kiểm định nghiệm thu cả đợt bằng `/k-rvspec` chế độ CHẤM ĐỢT TỰ HÀNH; không ghi đè `turn_<n>.txt`
     do agent viết; được viết trước `turn_<n>.txt` của lượt chưa có để lái lượt đó (agent nhận làm kế hoạch ở V0); (5) chạy
     bằng lệnh goal của khung hoặc bằng `/k-yolo @docs/goal/<tệp>`: lời gọi `/k-yolo` là lệnh người dùng 'chạy (tiếp) GOAL',
     k-yolo không thêm quyền; mọi khối máy sinh (lời nhắc của lệnh goal, autopilot, hook) không phải lệnh người dùng."
   - mở rộng khoá "Commit của người kiểm định" để nhận commit `docs(goal):` chỉ chạm `docs/goal/GOAL_*`;
   - sửa mọi chỗ SPEC còn mâu thuẫn với khoá: khoá "Thư mục turnlog" ("mỗi bên không ghi tệp của bên kia"), §0 Cách dùng
     (thêm đường tự hành), Hợp đồng báo cáo (dòng tác giả, mục TỰ CHẤM), luật đỏ về `turn_<n>.txt` (ngoại lệ cho tệp agent
     tự viết trong chế độ tự hành);
   - Sổ §8: trỏ tệp GOAL, `Lượt kế tiếp cần chấm` = `<n0>` "(agent tự hành)".
3. Commit theo tên tệp, hai commit hai mục đích:
   ```bash
   git add <tệp SPEC> [<tệp mục tiêu>] && git commit -m "docs(spec): <mô tả> cho GOAL <mốc>" -- <các tệp đó>   # khi G6.2 có sửa
   git add <tệp GOAL> && git commit -m "docs(goal): GOAL <mốc> tu hanh (<tên tệp>)" -- <tệp GOAL>
   ```
   Thêm dòng ghi công nếu môi trường yêu cầu. Không push.
4. Có Lệnh cổng → chạy lại, kẹp cây; kết quả phải giống G2 (thư mục `docs/goal/` có thể phải nằm trong tiền tố được phép
   của cổng — kiểm; không được thì DỪNG, báo, và không để commit làm đỏ cổng).

## 4. Định dạng trả lời

1. **Tệp GOAL**: đường dẫn, commit, bản SPEC (nếu đã sửa), cổng trước và sau.
2. **Chạy khô**: mỗi chặn thấy được một dòng (chỗ, bằng chứng, cách SPEC đã xử lý); không có thì ghi "không thấy chặn".
3. **Đích và đường đi**: mốc, số ID theo trạng thái (✅ / 🔎 / làm được ngay / ⛔), thứ tự làm, lượt bắt đầu `<n0>`.
4. **Việc cần bạn** (nếu có ⛔): mỗi dòng một lệnh nguyên văn cần ra, và việc nào trên đường găng đang chờ nó.
5. **Đã chốt thay bạn**: mỗi dòng `giả định | vì | cách đổi` (bỏ mục nếu không có).
6. **Cách chạy**: `/k-yolo @docs/goal/<tên tệp>` (khuyên dùng; khung không đọc skill thì dán
   `Đọc toàn bộ skill 'k-yolo' (khi cài chung prompt-toolkit: <đường dẫn tới ../k-yolo/SKILL.md>; nếu copy lẻ thì mở skill 'k-yolo' tương ứng trên host) rồi làm đúng theo nó cho @docs/goal/<tên tệp>`), hoặc đưa tệp (hay đoạn
   "LỆNH GOAL") vào lệnh goal của agent — không dùng cả hai cùng lúc. Agent dừng thì đọc
   `<Thư mục turnlog>/GOAL_<mốc>_ketqua.md`; nghiệm thu cả đợt bằng
   `/k-rvspec @<SPEC> @<Thư mục turnlog>/GOAL_<mốc>_ketqua.md` (CHẤM ĐỢT TỰ HÀNH); chạy tiếp thì gọi lại đúng lệnh đã dùng
   (agent đọc Sổ tự hành và làm tiếp từ lượt kế).

Câu ngắn, ý chính đầu câu. Không in lại nội dung tệp GOAL.

## 5. Ghi chú môi trường

Như §6 của `k-rvspec`: xác định OS và shell của host trước khi chạy lệnh (bash/zsh/sh, PowerShell,
Git Bash trên Windows...); dùng cú pháp tương thích shell hiện tại. `python -c` in tiếng Việt thì
`sys.stdout.reconfigure(encoding='utf-8')`; `core.autocrlf` bật thì so nội dung đã commit bằng `git show HEAD:<path>`.
Đọc/tìm tệp bằng công cụ của host (Read, Glob, Grep hoặc tương đương).
Mẫu log trong GOAL phải bắt đúng exit code trên shell của máy agent (lấy từ Hồ sơ, không tự chế).
Đường dẫn trong GOAL dùng `/` (không dùng `\` riêng của Windows) để mọi host đọc được.
