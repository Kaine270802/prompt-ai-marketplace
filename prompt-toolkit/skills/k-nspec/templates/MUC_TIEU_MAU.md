# MỤC TIÊU <TÊN DỰ ÁN> — BẤT BIẾN (bản <YYYY-MM-DD>)

Đây KHÔNG phải danh sách việc. SPEC của từng mốc do skill `k-nspec` lập từ tệp này; việc của từng lượt do skill
`k-rvspec` viết theo SPEC (`/k-nspec` còn gọi là `/prompt-toolkit:k-nspec` / `$k-nspec`;
`/k-rvspec` còn gọi là `/prompt-toolkit:k-rvspec` / `$k-rvspec`).
Chỉ người dùng sửa tệp này; người kiểm định chỉ thêm dòng vào cuối mục 7.

## 1. ĐÍCH

<Dự án là gì, cho ai, giải quyết việc gì. Thước đo so sánh, nếu có.>

## 2. NGUYÊN TẮC (khi xung đột, số nhỏ hơn thắng)

- **N1 Bằng chứng:** mọi con số có lệnh hoặc artefact tái lập được; mọi trích dẫn là nguồn đã mở và đọc.
- **N2** <nguyên tắc riêng của dự án>

## 3. HOÀN THÀNH KHI (đo bằng công cụ, không tự khai)

- **D1** <điều kiện + lệnh hoặc công cụ đo + ngưỡng>
- **D2 Cổng:** <lệnh kiểm> exit 0; <lệnh test> 0 lỗi; <lệnh lint> sạch.

## 4. LỘ TRÌNH (chỉ làm mốc ĐANG MỞ; mốc kế tiếp mở khi người dùng gọi `/k-nspec`)

- **M1 [ĐANG MỞ]** <kết quả của mốc>
- **M2** <...>

## 5. QUYỀN QUYẾT

- **5A Dành riêng cho người dùng.** Agent không làm; người kiểm định không hỏi, không giao, mà chọn đường khác tới cùng
  đích — không có đường khác thì ghi ⛔ kèm đúng lệnh người dùng cần ra. Gồm: mở mốc mới; đổi mục tiêu, nới hay bỏ
  điều kiện đạt, ngưỡng; push, merge, release, deploy; tải hay cài công cụ; việc tốn tiền; xoá dữ liệu hay lịch sử;
  thiết lập hệ thống hoặc bảo mật.
- **5B Agent tự quyết** lựa chọn kỹ thuật trong lượt: tối đa 3 phương án có bằng chứng; loại phương án vi phạm;
  ưu tiên đảo ngược được > ít rủi ro > đụng ít tệp > nhanh. Ghi QUYẾT ĐỊNH | VÌ | BẰNG CHỨNG | CÁCH ĐẢO NGƯỢC.
- **5C Người kiểm định (`/k-rvspec`)** chấm theo SPEC; được bác quyết định 5B; tự quyết MỌI việc không thuộc 5A và
  giao ngay — không có mục "Cần bạn quyết"; quyết định bền ghi vào mục 7.

## 6. RÀNG BUỘC CỐ ĐỊNH

- Không push khi chưa có lệnh riêng.
- <ràng buộc riêng: thư mục chỉ đọc, lệnh cấm, giới hạn tài nguyên>

## 7. QUYẾT ĐỊNH ĐÃ CHỐT (người kiểm định chỉ thêm vào cuối, mỗi QĐ vài dòng)

- **QĐ-1** <quyết định> — vì <lý do>. Đảo ngược: <cách>.
