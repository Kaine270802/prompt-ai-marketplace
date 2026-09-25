# SPEC <TÊN DỰ ÁN> — <MỐC> · bản S1 (<YYYY-MM-DD>)

Dẫn xuất từ <tệp mục tiêu> (bản <ngày>), dòng <n>: "<trích nguyên văn mục tiêu của mốc>".
Lập bằng skill `k-nspec` (`/k-nspec` · `/prompt-toolkit:k-nspec` · `$k-nspec`) tại `<sha HEAD>`. Khi mâu thuẫn:
**lời người dùng > mục tiêu > SPEC > khối tin nhắn lượt > báo cáo agent**.
Người kiểm định (skill `k-rvspec`: `/k-rvspec` · `/prompt-toolkit:k-rvspec` · `$k-rvspec`) giữ SPEC; mỗi lần sửa
tăng số bản (S2, S3...) và ghi ở §10.

## §0 Cách dùng

Vòng lặp mỗi lượt:

1. Người dùng mở `docs/turnlog/turn_<n>.txt` và chép nguyên văn gửi agent (mẫu §7).
2. Agent làm, commit, rồi GHI TOÀN BỘ báo cáo (§5) vào `docs/turnlog/turn_<n>_report.md` (bước cuối khối tin nhắn).
   Agent KHÔNG sửa `turn_<n>.txt`.
3. Người dùng gọi `/k-rvspec @<đường dẫn tệp này> @docs/turnlog/turn_<n>_report.md`.
   (Dự phòng: `/k-rvspec @<tệp này>` rồi dán `KẾT QUẢ TRƯỚC AI AGENT PHẢN HỒI LƯỢT TRƯỚC LÀ:` + toàn bộ phản hồi.)
4. Người kiểm định chấm theo §6, tự quyết mọi lựa chọn, cập nhật §8, commit riêng, rồi GHI khối tin nhắn lượt n+1 ra
   `docs/turnlog/turn_<n+1>.txt` — không in khối trong câu trả lời. Quay lại bước 1.
5. Mốc ĐỦ ĐIỀU KIỆN ĐÓNG → người dùng gọi `/k-nspec <mốc kế tiếp>` để lập SPEC mốc sau.

Tệp của hợp đồng: <tệp mục tiêu> (người dùng sửa) và tệp này (chỉ người kiểm định sửa).
Agent đọc, không sửa. Chỉ người kiểm định đổi trạng thái trong §8; agent chỉ đề xuất (§5 mục 4).

### Hồ sơ repo

<!-- Người kiểm định đọc mục này mỗi lần gọi skill k-rvspec. Khóa không cần thì xoá dòng; khóa thiếu dùng mặc định
     ở §3 của skill k-rvspec (../k-rvspec/SKILL.md khi cài chung prompt-toolkit). Nhãn (chờ duyệt) chỉ dùng cho lệnh có GHI, build, tải hay tốn tiền mà người
     kiểm định sẽ chạy; lệnh chỉ đọc thì không cần nhãn. Build và test dài: để agent chạy và lưu log. -->

- **Vùng ghi:** `docs/spec/`
- **Thư mục turnlog:** `docs/turnlog/` (đã git-ignore, không commit gì trong đó). Người kiểm định ghi
  `turn_<n>.txt` (khối tin nhắn); agent ghi `turn_<n>_report.md` (báo cáo). Mỗi bên KHÔNG ghi tệp của bên kia.
- **Khối lệnh lượt:** `docs/turnlog/turn_<n>.txt`
- **Tệp mục tiêu:** `docs/spec/MUC_TIEU.md`<, `docs/spec/MUC_TIEU_<MỐC>.md`>
- **Sổ quyết định:** <mục 7 của tệp mục tiêu, chỉ thêm vào cuối> | <bảng Quyết định ở §8 của tệp này>
- **Quyền quyết:** <mục 5 của tệp mục tiêu> | <mặc định của k-rvspec B4>
- **Nhánh làm việc:** `<nhánh>`
- **Agent phải commit:** có
- **Commit của người kiểm định:** subject bắt đầu `docs(spec):` và chỉ chạm `docs/spec/`
- **Commit sổ:** `docs(spec): ledger after turn <n>`
- **Upstream:** `origin/<nhánh chính>`
- **Lệnh cổng:** `<lệnh kiểm toàn cục: nhanh, tất định, không ghi vào cây>`
- **Được chạy thêm:** `<lệnh chỉ đọc hoặc chỉ in ra>`
- **Cấm thêm:** <lệnh, thư mục không được đụng>
- **Kiểm agent rảnh:** <lệnh chỉ liệt kê tiến trình của agent hoặc tool đo; có kết quả = agent đang chạy> | không có
- **Agent:** <tên agent>; log: <đường dẫn> | không có
- **Bằng chứng riêng:** log build, test, lint trong `<thư mục đã ignore>`: dòng đầu là nguyên dòng lệnh, dòng cuối là
  exit code; cách bắt exit code đúng trên shell này: `<mẫu lệnh>`
- **Môi trường:** <OS, shell, lưu ý encoding>

## §1 Quy ước

- **1.1 Trạng thái:** ⬜ CHƯA · 🔄 ĐANG · 🔎 CHỜ KIỂM (agent báo đạt) · ✅ XONG · ❌ ĐỎ · ⛔ CHẶN (cần lệnh của người dùng).
  Chỉ người kiểm định gán ✅, sau khi tự tái lập bằng chứng.
- **1.2 Bằng chứng hợp lệ:** lệnh + output nguyên văn, chạy trong chính lượt, có trong danh sách thao tác của lượt.
  Số lấy từ lượt trước ghi `[TỪ LƯỢT k: <đường dẫn log>]`. sha256 đủ 64 ký tự hex.
  `path:line` luôn kèm output lệnh in đúng dòng đó. Hash, nhánh, tag phải resolve được bằng `git rev-parse --verify`.
- **1.3** Neo `path:line` trong SPEC đúng tại commit `<sha>`. Tệp đã đổi thì in lại dòng trước khi dùng.
- **1.4** <quy ước riêng: đơn vị, cách lấy median, điều kiện máy sạch...>

## §2 Giá trị tham chiếu, giả định và neo

- **2.0 Giả định đã chốt khi lập SPEC** (người dùng đổi bằng cách sửa mục tiêu rồi `/k-nspec lập lại`, hoặc nói trong
  lần `/k-rvspec` kế):

  | Mã | Giả định | Vì | Nguồn | Cách đổi |
  |---|---|---|---|---|
  | G1 | <cách hiểu đã chọn> | <lý do> | <dòng mục tiêu, `path:line`> | <...> |

- **2.1** <phiên bản, hash, ngưỡng dùng để chấm; kèm nguồn>
- **2.2 Hiện trạng lúc lập SPEC** (tại `<sha>`): <số đo, kết quả cổng, đếm test... kèm lệnh đã chạy>
- **2.3 Neo mã** (tại `<sha>`): <`path:line` — nội dung>

## §3 Điều kiện đóng mốc và đường găng

| Nhóm | Nội dung (dòng mục tiêu nguồn) | ID |
|---|---|---|
| E1 | <điều kiện hoàn thành trong mục tiêu> | <MỐC>-<X>-01, <MỐC>-<X>-02 |
| E2 | <...> | <...> |

Tổng <N> ID. Tiến độ = số ID ✅ trên tổng, theo từng nhóm (dòng tiến độ ở §8).

**Đường găng:** <ID> → <ID> → <ID>.

**<MỐC> ĐỦ ĐIỀU KIỆN ĐÓNG** khi mọi ID là ✅ tại CÙNG một HEAD cuối, sau đó không có commit nào
(trừ commit chỉ sửa Vùng ghi). Mốc kế tiếp mở khi người dùng gọi `/k-nspec`.

## §4 Yêu cầu

Mỗi yêu cầu gồm: Hiện trạng · Làm · Đạt khi · File được sửa · Kiểm · Phụ thuộc.

### <MỐC>-<X>-01 — <tên>

- **Hiện trạng** (tại `<sha>`): <điều đang đúng hay còn thiếu, kèm `path:line`>
- **Làm:** <việc cụ thể trên mã thật: tệp, hàm, hướng tiếp cận, cạm bẫy đã thấy + lệnh chính>
- **Đạt khi:** <điều kiện đo được bằng lệnh: con số, chuỗi, exit code cụ thể>
- **File được sửa:** <danh sách> | không
- **Kiểm:** <người kiểm định tái lập bằng lệnh nào, hoặc kiểm log nào của agent>
- **Phụ thuộc:** <ID> | không

## §5 Hợp đồng báo cáo của agent

Đúng các mục, đúng thứ tự:

- **BẢNG BƯỚC (đặt ngay đầu báo cáo):** chép lại toàn bộ danh sách bước của khối tin nhắn, mỗi bước kèm ô dấu đã cập nhật
  (`[x]` xong và tự thấy ĐẠT · `[!]` đã làm nhưng KHÔNG ĐẠT · `[-]` chưa làm hoặc bỏ, ghi lý do · `[?]` bị chặn vì việc
  dành riêng cho người dùng) và một dòng: lệnh chính đã chạy | commit hoặc tệp đã đổi. Đánh dấu ngay khi xong từng bước,
  không để tới cuối lượt. Dấu này là ĐỀ XUẤT; chỉ người kiểm định đổi dấu trong §8.
- **0 PREFLIGHT:** bảng kỳ vọng | thực tế cho HEAD, `git status --porcelain`, ahead, <kiểm riêng>.
- **1 SỬA:** mỗi mục sửa trong repo gồm việc | commit | bằng chứng (chỉ khi khối có bước T1).
- **2 YÊU CẦU ĐÃ LÀM:** mỗi ID gồm lệnh nguyên văn | output nguyên văn | ĐẠT/KHÔNG ĐẠT theo "Đạt khi" | commit + tệp.
  Hành vi bị bỏ hay bị đổi (hàm, nhánh, giá trị cấu hình thành hằng số, chuỗi người dùng thấy) → liệt kê, dù chỉ là
  hệ quả phụ.
- **3 QUYẾT ĐỊNH:** QUYẾT ĐỊNH | VÌ | BẰNG CHỨNG | CÁCH ĐẢO NGƯỢC.
- **4 BẢNG TRẠNG THÁI:** ID | trạng thái đề xuất (🔎, ❌ hoặc ⛔) | bằng chứng.
- **5 ĐÓNG LƯỢT:** <Lệnh cổng> + exit code; `git status --porcelain`; HEAD; ahead;
  `git log --oneline <HEAD đầu lượt>..HEAD`; `git show --stat` cho từng commit.
- **6 CHƯA LÀM / BỊ CHẶN:** ID | lý do | số lần hỏng.
- **NƠI NỘP:** ghi TOÀN BỘ báo cáo trên vào `docs/turnlog/turn_<n>_report.md` ở bước cuối lượt (thư mục đã git-ignore,
  KHÔNG commit). Đây là bản người dùng đưa cho người kiểm định.

**Cấm:** ghi ĐẠT không kèm lệnh; tự gán ✅; nêu hash, số đo, bảng thống kê hay trích dẫn không do lệnh trong lượt
sinh ra; đặt mã ID mới (đề xuất việc mới thì viết văn xuôi); sửa Vùng ghi.

## §6 Hợp đồng kiểm định

Người kiểm định làm mỗi lượt qua `/k-rvspec`: chỉ đọc với mọi thứ, trừ Vùng ghi.

### 6.1 Luôn làm

- phạm vi lượt: `<HEAD đã kiểm ở §8>..HEAD`, trừ commit của người kiểm định (Hồ sơ repo);
- HEAD, dấu vân tay cây, ahead, `--stat` từng commit; chạy Lệnh cổng, kẹp dấu vân tay cây trước và sau;
- tính lại mọi hash, resolve mọi ref, in lại mọi `path:line`, tính lại mọi số dùng để kết luận;
- đối chiếu mỗi giá trị bằng chứng với danh sách lệnh của lượt; đối chiếu tệp bị sửa với "File được sửa";
- commit mã xoá nhiều hơn thêm → đọc diff tìm hành vi bị bỏ.

### 6.2 Luật đỏ

- R1: <luật riêng của repo, ví dụ: commit chạm `<thư mục artefact>` phải khớp một lệnh đo trong lượt>.
- Làm yếu test hay cổng (xoá, bỏ qua, nới ngưỡng) để lọt, không có QĐ → 🔴.
- Agent sửa Vùng ghi, `turn_<n>.txt` hoặc thư mục skill → 🔴.

### 6.3 Mức nghiêm trọng

- 🔴 bằng chứng sai hoặc bịa; vi phạm luật đỏ; cổng đỏ cuối lượt; commit làm test đỏ; thao tác không đảo ngược được.
- 🟡 báo đạt mà không đạt "Đạt khi"; sửa ngoài "File được sửa" không có quyết định; `path:line` sai; bỏ hành vi mà
  không nêu; thiếu bằng chứng.
- 🔵 câu chữ, trình bày; sai số không đổi kết luận.

### 6.4 Sau lượt có 🔴

Không giao yêu cầu phụ thuộc phần sai. Sai nằm trong repo → lượt sau bắt đầu bằng T1 SỬA. Sai chỉ ở câu chữ báo cáo →
người kiểm định ghi sự thật vào §8 và nhắc "đừng lặp lại" trong khối; không giao bước viết lại báo cáo cũ.

## §7 Mẫu khối tin nhắn lượt

Người kiểm định ghi khối này ra `docs/turnlog/turn_<n>.txt` (thuần văn bản, không bọc ```` ``` ````).
Khối là lệnh, không phải bài phân tích; nhắm dưới ~150 dòng.

```text
TIN NHẮN LƯỢT <n> — <MỐC> — nhánh <nhánh> — theo <tệp mục tiêu> + <tệp SPEC> (bản S<k>)
Bạn đang đọc docs/turnlog/turn_<n>.txt. KHÔNG sửa tệp này; bạn chỉ ghi docs/turnlog/turn_<n>_report.md.
Đọc tệp mục tiêu và SPEC trước khi làm. Không sửa <Vùng ghi>. Báo cáo theo SPEC §5.

MỤC TIÊU LƯỢT
  <1–3 dòng: sau lượt này điều gì trong "Đạt khi" của ID nào sẽ đúng, và vì sao làm nó bây giờ>

LƯỢT TRƯỚC (<n-1>): <XẾP LOẠI> · bước ✅ x/y · tiến độ <MỐC> t/N
  Đừng lặp lại: <mỗi lỗi một dòng, cụ thể>            (bỏ mục này ở lượt đầu)

KẾ HOẠCH — làm tuần tự; xong bước nào sửa ô dấu của ĐÚNG bước đó rồi mới sang bước sau.
  [ ] T0 PREFLIGHT: git rev-parse HEAD (kỳ vọng <sha>); git status --porcelain (kỳ vọng rỗng); <kiểm riêng>.
      Lệch → DỪNG, báo.
  [ ] T1 SỬA <mã đính chính> (chỉ khi lỗi nằm trong repo): <việc> — Đạt khi: <điều kiện> — tệp: <...>.
  [ ] T2 <ID> — Đạt khi: "<trích nguyên văn §4>"
      Làm: <cách làm cụ thể, có path:line tại HEAD>
      Lệnh chính: <lệnh>    Tệp được sửa: <danh sách>    Lưu bằng chứng: <tệp log/.out>
      Nếu <tình huống đã lường>: <cách dự phòng>.
  [ ] T.. <...>
  [ ] T<cuối> BÁO CÁO: viết TOÀN BỘ báo cáo theo SPEC §5 vào docs/turnlog/turn_<n>_report.md
      (thư mục git-ignore, KHÔNG commit). Đây là việc cuối cùng của lượt.

QUY TẮC
  Ô dấu: [ ] chưa làm · [x] xong và tự thấy ĐẠT · [!] đã làm nhưng KHÔNG ĐẠT · [-] bỏ qua (ghi lý do)
         · [?] bị chặn vì việc dành riêng cho người dùng.
  Bước [!] hoặc [?] → DỪNG các bước phụ thuộc, báo; bước độc lập vẫn làm tiếp.
  Lựa chọn kỹ thuật trong bước: tự quyết (tối đa 3 phương án, chọn cái đảo ngược được), ghi
  QUYẾT ĐỊNH | VÌ | BẰNG CHỨNG | CÁCH ĐẢO NGƯỢC trong báo cáo, rồi làm tiếp.
  Việc dành riêng cho người dùng (push, merge, xoá dữ liệu, tải/cài, tốn tiền, thiết lập hệ thống,
  sửa mục tiêu, nới điều kiện đạt) → KHÔNG làm; đánh [?], nêu lý do, làm tiếp bước độc lập.
  Không đặt mã ID mới; đề xuất việc mới thì viết văn xuôi.
  Commit hết, git add theo tên tệp, mỗi commit một mục đích; cuối lượt git status --porcelain rỗng.
  Cấm: <Cấm thêm của Hồ sơ + ràng buộc của mục tiêu>.

BÁO CÁO: bảng bước kèm ô dấu ở ĐẦU; mỗi bước [x]/[!] kèm lệnh chính đã chạy + commit hoặc tệp đã đổi.
  Mọi số, hash, path:line, trích dẫn phải do lệnh trong lượt sinh ra.
```

## §8 Sổ trạng thái

Người kiểm định cập nhật và commit sau mỗi lần `/k-rvspec`. Sổ là trạng thái hiện hành, không phải nhật ký:
bảng bước chỉ giữ lượt vừa chấm và lượt kế tiếp; đính chính đã đóng quá 2 lượt thì bỏ (git giữ bản cũ).
Dấu: ✅ XONG · 🔎 CHỜ KIỂM · 🔄 ĐANG · ⬜ CHƯA · ❌ ĐỎ · ⛔ CHẶN.
`@<commit>` = đạt tại commit đó, phải kiểm lại ở HEAD cuối (§3).

HEAD đã kiểm: `<sha đầy đủ>` | cây sạch | ahead <n>.
Lượt kế tiếp cần chấm: <n>.
Tiến độ <MỐC>: 0/<N> · E1 0/<a> · E2 0/<b>.

Mức độ hoàn thành từng lượt (mới nhất trên cùng, giữ 5 lượt gần nhất):

| Lượt | Xếp loại | Bước ✅ | ID mới ✅ | 🔴 / 🟡 / 🔵 |
|---|---|---|---|---|

| Nhóm | ID | Dấu | Lượt | Ghi chú |
|---|---|---|---|---|
| E1 | <MỐC>-<X>-01 | ⬜ | — | |

Bước của lượt <n> (dấu agent là đề xuất; dấu người kiểm định là kết luận):

| Bước | ID | Nội dung ngắn | Dấu agent | Dấu người kiểm định | Bằng chứng |
|---|---|---|---|---|---|
| T0 | — | preflight | — | ⬜ | |

Đính chính đang mở:

| Mã | Dấu | Lượt | Nội dung |
|---|---|---|---|

Quyết định (khi Sổ quyết định trỏ về đây):

| Mã | Quyết định | Vì | Bằng chứng | Cách đảo ngược |
|---|---|---|---|---|

### Ghi chú cho lần chấm lượt <n>

- <điều người kiểm định cần nhớ khi chấm>

## §9 Ngoài mốc

Chỉ theo dõi, không giao khi mốc chưa đóng.

## §10 Lịch sử SPEC

- **S1** <YYYY-MM-DD>: bản đầu, lập bằng `/k-nspec` từ <tệp mục tiêu> tại `<sha>`.
