# Câu hỏi thảo luận Lab 02 – Feature/Topic Flow & Pull Request

- **Học phần:** IT3180 – Nhập môn Công nghệ phần mềm
- **Chủ đề:** Quy trình Feature/Topic Flow, Code Review và Chiến lược Merge
- **Người thực hiện:** PhucHung06 (MSSV: 202416216)

---

### Câu 1: Vì sao lập trình viên phải đồng bộ (fetch/merge) nhánh `master` vào nhánh của mình trước khi gửi PR?

**Trả lời:**
1. **Phát hiện và giải quyết xung đột (Merge Conflict) sớm tại máy cục bộ:**
   - Trong quá trình một lập trình viên làm việc trên nhánh tính năng, nhánh `master` trên remote có thể đã tiếp nhận nhiều commit/PR mới từ các thành viên khác. Việc kéo `master` mới về giúp lập trình viên chủ động xử lý xung đột ngay trên máy mình trước khi tạo PR, tránh tình trạng PR bị khóa với thông báo *"This branch has conflicts that must be resolved"*.

2. **Kiểm tra tích hợp (Integration Testing) thực tế:**
   - Đảm bảo tính năng mới viết tương thích tốt với phiên bản mới nhất của toàn bộ hệ thống. (Ví dụ cụ thể trong Lab 02: Dev 2 kéo `master` đã có hàm `print_cart` của Dev 1 về để chạy thử nghiệm `python main.py`, xác nhận hệ thống tích hợp chạy ổn định trước khi xin merge).

3. **Giảm áp lực cho Reviewer và bảo vệ nhánh chính:**
   - Người review có thể tập trung đánh giá chất lượng logic của code mới thay vì phải xử lý lỗi xung đột. Tuân thủ nguyên tắc SCM: *"Mã nguồn đưa lên review phải là mã nguồn đã được tích hợp và kiểm thử đạt chuẩn"*.

---

### Câu 2: Khi nào thì NÊN dùng Rebase và khi nào KHÔNG ĐƯỢC dùng Rebase?

**Trả lời:**

#### 1. Khi NÊN dùng Rebase:
- **Trên nhánh riêng cá nhân (Feature/Topic/Local branch):** Khi bạn đang làm việc một mình trên một nhánh và muốn cập nhật code mới nhất từ `master` (`git rebase master`), hoặc muốn gộp vào nhánh chính bằng `Rebase and merge`.
- **Duy trì lịch sử thẳng hàng (Linear History):** Giúp đồ thị Git thẳng tắp, trực quan, không sinh ra các commit merge trung gian rác dạng `Merge branch 'master' into...`, giúp việc đọc `git log` như một cuốn nhật ký phát triển liền mạch.

#### 2. Khi KHÔNG ĐƯỢC dùng Rebase (The Golden Rule of Rebase):
- **Tuyệt đối KHÔNG rebase trên các nhánh công khai, dùng chung:** Như nhánh `master`, `main`, `release/*` hoặc nhánh mà hai hay nhiều người đang cùng pull/push code chung.
- **Lý do kỹ thuật:** Rebase bản chất là nhấc các commit cũ và tạo ra các **commit hoàn toàn mới với mã băm SHA mới**. Nếu rebase trên nhánh công khai rồi đẩy lên (`git push --force`), lịch sử của remote sẽ bị viết lại, làm sai lệch toàn bộ mốc theo dõi của các thành viên khác, dẫn đến lỗi xung đột dây chuyền nghiêm trọng trong toàn đội.

---

### Câu 3: Nhánh `feature/*` khác nhánh `topic/*` như thế nào?

**Trả lời:**

| Tiêu chí | Nhánh `feature/*` | Nhánh `topic/*` |
|---|---|---|
| **Bản chất** | Phát triển **tính năng nghiệp vụ** mới. | Thực hiện một **chủ đề kỹ thuật / tài liệu / cấu hình**. |
| **Đối tượng hưởng lợi** | Trực tiếp phục vụ **người dùng cuối (End-user)**. | Phục vụ **đội ngũ phát triển (Developers / QA / DevOps)**. |
| **Ví dụ trong Lab 02** | - `feature/cart-print` (in giỏ hàng)<br>- `feature/search-by-title` (tìm kiếm DVD) | - `topic/pr-template` (tạo mẫu PR)<br>- `topic/use-case-diagram` (vẽ sơ đồ use-case) |
| **Ý nghĩa trong quy trình SCM** | Phân loại rõ ràng mục đích của thay đổi, giúp người duyệt (Reviewer) và hệ thống CI phân định được phạm vi kiểm thử (tính năng cần test nghiệp vụ kỹ, tài liệu chỉ cần review nội dung). |
