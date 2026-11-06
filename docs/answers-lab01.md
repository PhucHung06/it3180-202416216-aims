# Câu hỏi thảo luận Lab 01 – Thiết lập môi trường & Refactor Flow

- **Học phần:** IT3180 – Nhập môn Công nghệ phần mềm
- **Chủ đề:** Quản lý cấu hình phần mềm với Git & GitHub
- **Người thực hiện:** PhucHung06 (MSSV: 202416216)

---

### Câu 1: Vì sao nên dùng `git mv` thay vì di chuyển tệp bằng chuột/file explorer thông thường?

**Trả lời:**
1. **Bảo toàn lịch sử thay đổi (Commit History):**
   - Khi di chuyển tệp bằng File Explorer hay chuột, hệ điều hành chỉ đơn giản là xóa tệp ở vị trí cũ và tạo một tệp mới ở vị trí mới. Git có thể nhận diện đó là 2 thao tác rời rạc: một thao tác *Delete* và một thao tác *Add file mới*.
   - Lệnh `git mv` báo trực tiếp cho Git (chỉ mục/Staging Area) rằng đây là hành động di chuyển/đổi tên (`renamed`). Nhờ đó, toàn bộ lịch sử commit, người đóng góp và các phiên bản sửa đổi trước đây của tệp được bảo toàn liên tục khi tra cứu bằng lệnh `git log --follow <tệp>` hoặc `git blame`.

2. **Hỗ trợ Code Review trực quan trên GitHub:**
   - Khi tạo Pull Request, các tệp được di chuyển bằng `git mv` sẽ được GitHub hiển thị dưới dạng nhãn **`renamed`** (chỉ hiển thị những dòng code thực sự thay đổi bên trong), giúp reviewer dễ dàng nhận biết cấu trúc mà không phải đọc lại toàn bộ mã nguồn như một tệp mới thêm vào.

3. **Thao tác nhanh và an toàn:**
   - `git mv` tự động đưa trạng thái di chuyển vào vùng Staging Area ngay lập tức mà không cần phải chạy thêm lệnh `git rm` ở file cũ và `git add` ở file mới.

---

### Câu 2: Nhánh `release/lab01` có phải là một Baseline không? Tại sao?

**Trả lời:**
- **Có, nhánh `release/lab01` chính là một Baseline** (cụ thể là *Release Baseline* cho mốc hoàn thành Lab 01).

**Giải thích theo lý thuyết SCM:**
1. **Định nghĩa Baseline:** Trong Quản lý cấu hình phần mềm (SCM), Baseline là một cấu hình hoặc trạng thái phiên bản sản phẩm phần mềm đã được xem xét kỹ lưỡng, kiểm thử đạt yêu cầu, được các bên thống nhất và chính thức "đóng băng" tại một mốc thời gian cụ thể.
2. **Đáp ứng đầy đủ tiêu chí của Baseline:**
   - **Đã kiểm thử và đạt yêu cầu:** Mã nguồn sau khi refactor vào package `aims/` đã chạy thử nghiệm và cho kết quả chuẩn xác (`Total cost: 63.89 $`).
   - **Tính đóng băng (Freeze):** Nhánh `release/lab01` được tạo ra từ đỉnh của `master` để cố định trạng thái bài nộp, làm căn cứ bàn giao và đánh giá.
   - **Kiểm soát thay đổi nghiêm ngặt (Change Control):** Sau khi đã tạo nhánh release, lập trình viên không được phép commit trực tiếp thêm bất kỳ tính năng mới nào lên nhánh này. Nếu phát hiện lỗi nghiêm trọng, thay đổi chỉ được đưa vào thông qua quy trình sửa lỗi đặc biệt (**Hotfix flow**) có phê duyệt.

---

### Câu 3: Vì sao không nên commit thẳng lên `master` dù bạn chỉ làm việc một mình?

**Trả lời:**
1. **Giữ nhánh `master` luôn ổn định và sẵn sàng chạy (Deployable State):**
   - Nhánh `master` đóng vai trò là "nguồn chân lý" (Single Source of Truth) của toàn bộ dự án. Làm việc trên các nhánh riêng (`refactor/*`, `feature/*`, `bugfix/*`) giúp cô lập các thay đổi đang làm dở hoặc có nguy cơ phát sinh lỗi, tránh làm gián đoạn trạng thái hoạt động bình thường của codebase chính.

2. **Tận dụng cơ chế Tự phản biện & Kiểm soát (Self-Review qua Pull Request):**
   - Kể cả khi làm một mình, việc mở Pull Request buộc lập trình viên phải thực hiện bước kiểm tra lại toàn bộ khác biệt mã nguồn (Diff) trên giao diện GitHub trước khi merge. Thao tác này giúp phát hiện sớm các lỗi ngớ ngẩn như: sót tệp tạm, commit nhầm log debug, sai sót cú pháp hoặc chưa tuân thủ quy ước đặt tên commit.

3. **Đảm bảo tính truy vết (Traceability & Status Accounting):**
   - Mỗi Pull Request là một bằng chứng rõ ràng cho một Change Request trong SCM: có tiêu đề, lý do thay đổi, mô tả chi tiết và kết quả kiểm thử. Khi nhìn lại lịch sử dự án, ta biết chính xác một thay đổi lớn được đưa vào nhằm mục đích gì thay vì một chuỗi các commit vụn vặt trên `master`.

4. **Sẵn sàng cho làm việc nhóm và thiết lập CI/CD:**
   - Trong thực tế và từ Lab 02 trở đi, nhánh `master` sẽ được kích hoạt cơ chế bảo vệ (**Branch Protection Rules**) và hệ thống tự động kiểm thử (**CI**). Nếu không rèn luyện thói quen làm việc qua nhánh và Pull Request ngay từ đầu, bạn sẽ gặp khó khăn khi làm việc trong môi trường nhóm chuyên nghiệp.
