# Tổng hợp Câu hỏi thảo luận & Trả lời - SCM IT3180

- **Họ và tên:** PhucHung06
- **MSSV:** 202416216
- **Học phần:** IT3180 – Nhập môn Công nghệ phần mềm
- **Repository:** `it3180-202416216-aims`

---

## 📌 Lab 01 – Thiết lập môi trường & Refactor Flow

### Câu 1: Vì sao nên dùng `git mv` thay vì di chuyển tệp bằng chuột/file explorer thông thường?
- **Trả lời:**
  1. **Bảo toàn lịch sử thay đổi (Commit History):** Di chuyển tệp bằng chuột hay hệ điều hành chỉ đơn giản là xóa tệp ở chỗ cũ và thêm mới ở chỗ mới, khiến Git có thể hiểu nhầm là thao tác xóa + tạo mới. `git mv` báo trực tiếp cho Staging Area rằng đây là hành động đổi tên/di chuyển (`renamed`), giúp bảo toàn trọn vẹn lịch sử commit và công sức đóng góp của từng dòng code qua các lệnh như `git log --follow` hay `git blame`.
  2. **Hỗ trợ Code Review trực quan:** Trên Pull Request của GitHub, các tệp chuyển bằng `git mv` được gắn nhãn `renamed`, người review chỉ cần xem diff nội dung thay đổi thực tế mà không phải duyệt lại toàn bộ tệp như một tệp mới tinh.
  3. **Thao tác nhanh gọn:** Tự động đưa thay đổi vào Staging Area mà không cần chạy thêm lệnh `git add`/`git rm`.

---

### Câu 2: Nhánh `release/lab01` có phải là một Baseline không? Tại sao?
- **Trả lời:**
  - **Có, nhánh `release/lab01` chính là một Baseline** (cụ thể là *Release Baseline* cho mốc Lab 01).
  - **Lý do:**
    - Theo định nghĩa SCM, Baseline là một cấu hình/trạng thái phiên bản sản phẩm đã được kiểm thử, thẩm định đạt chuẩn và được "đóng băng" (frozen) tại một thời điểm bàn giao.
    - `release/lab01` cố định trạng thái mã nguồn sau khi refactor đã chạy kiểm thử thành công (`Total cost: 63.89 $`).
    - Nhánh này được dùng làm căn cứ nộp bài/đánh giá, không được commit trực tiếp thêm tính năng mới mà chỉ có thể sửa đổi qua quy trình kiểm soát chặt chẽ (Hotfix flow) nếu phát hiện lỗi nghiêm trọng.

---

### Câu 3: Vì sao không nên commit thẳng lên `master` dù bạn chỉ làm việc một mình?
- **Trả lời:**
  1. **Giữ nhánh `master` luôn ổn định và sẵn sàng chạy (Deployable State):** Tránh việc đưa các đoạn code thử nghiệm, dở dang làm hỏng trạng thái hoạt động của nhánh chính.
  2. **Tận dụng cơ chế Tự kiểm duyệt (Self-Review qua Pull Request):** Khi mở PR, bạn có cơ hội kiểm tra lại toàn bộ diff thay đổi trên giao diện web, dễ dàng phát hiện các lỗi vô ý như sót tệp rác, debug log, sai convention commit trước khi tích hợp vào nhánh chính.
  3. **Đảm bảo tính truy vết (Traceability & SCM Change Control):** Mỗi PR đại diện cho một Change Request rõ ràng về mục đích, thay đổi và bằng chứng kiểm thử trong lịch sử dự án.
  4. **Rèn luyện thói quen làm việc nhóm và tương thích với CI/CD:** Chuẩn bị sẵn sàng cho quy trình bảo vệ nhánh (Branch Protection) và tự động hóa kiểm thử trong các bài lab tiếp theo cũng như môi trường doanh nghiệp.

---

## 📌 Lab 02 – Feature/Topic Flow & Pull Request

### Câu 1: Vì sao lập trình viên phải đồng bộ (fetch/merge) nhánh `master` vào nhánh của mình trước khi gửi PR?
- **Trả lời:**
  1. **Phát hiện và giải quyết xung đột (Merge Conflict) sớm:** Nhánh của bạn có thể xuất phát từ commit cũ, trong lúc đó người khác đã merge code vào `master`. Đồng bộ trước giúp xử lý xung đột ngay tại máy cục bộ thay vì để PR bị khóa do conflict.
  2. **Kiểm tra tích hợp (Integration Testing):** Đảm bảo mã nguồn tính năng mới tương thích và chạy ổn định với trạng thái mới nhất của toàn hệ thống (ví dụ: Dev 2 kéo `print_cart` của Dev 1 về chạy thử `python main.py` trước khi merge).
  3. **Tối ưu quy trình Review:** Giúp reviewer tập trung vào logic code mới, tuân thủ nguyên tắc SCM: "thứ được duyệt = thứ đã được tích hợp và kiểm thử".

---

### Câu 2: Khi nào thì NÊN dùng Rebase và khi nào KHÔNG ĐƯỢC dùng Rebase?
- **Trả lời:**
  - **NÊN dùng:** Trên các nhánh cá nhân (local/feature branch) chưa chia sẻ với ai hoặc khi muốn gộp vào master bằng `Rebase and merge` để giữ lịch sử commit thẳng hàng (Linear History), sạch sẽ và dễ đọc bằng `git log`.
  - **KHÔNG ĐƯỢC DÙNG (Golden Rule of Rebase):** Tuyệt đối không rebase trên các nhánh công khai, dùng chung như `master`, `main`, `release/*` vì rebase tạo ra mã SHA mới, viết lại lịch sử commit, sẽ phá vỡ toàn bộ cấu trúc kho Git của các thành viên khác trong nhóm.

---

### Câu 3: Nhánh `feature/*` khác nhánh `topic/*` như thế nào?
- **Trả lời:**
  - `feature/*`: Dùng để phát triển một **chức năng cụ thể** phục vụ trực tiếp người dùng cuối (ví dụ: `feature/cart-print`, `feature/search-by-title`).
  - `topic/*`: Dành cho một **chủ đề kỹ thuật phụ trợ hoặc tài liệu** hỗ trợ đội ngũ phát triển (ví dụ: `topic/pr-template`, `topic/use-case-diagram`).
  - Việc phân biệt giúp quy trình Change Control rõ ràng và reviewer nắm bắt ngay được bản chất thay đổi.

---

## 📌 Lab 03 – Bugfix Flow, Xung đột & Hoàn tác

### Câu 1: Khái niệm "Merge Base" là gì? Vai trò của nó khi Git giải quyết xung đột?
- **Trả lời:**
  - **Khái niệm:** Merge Base là commit tổ tiên chung gần nhất (Best Common Ancestor) của 2 nhánh chuẩn bị merge. Lệnh tra cứu: `git merge-base <branch1> <branch2>`.
  - **Vai trò trong thuật toán 3-Way Merge:**
    - Git dùng Merge Base làm hệ quy chiếu gốc (Reference Baseline) để so sánh độ lệch thay đổi của từng nhánh: $\Delta_A = A - \text{Base}$ và $\Delta_B = B - \text{Base}$.
    - **Tự động merge:** Nếu chỉ có 1 nhánh sửa dòng $X$ còn nhánh kia giữ nguyên như Base, Git tự động lấy nội dung sửa đổi. Nếu 2 nhánh sửa ở các file hoặc dòng code tách biệt nhau, Git tự động gộp cả hai.
    - **Phát hiện xung đột (Conflict):** Khi cả 2 nhánh cùng sửa đổi trên cùng một dòng code (hoặc khối code liền kề) so với Base nhưng nội dung sửa đổi lại khác nhau, Git sẽ phát hiện xung đột và dừng lại, gắn cờ `<<<<<<<`, `=======`, `>>>>>>>` để yêu cầu lập trình viên can thiệp thủ công.

---

### Câu 2: Vì sao trên các nhánh như `master` hay `release/*` phải dùng `git revert` thay vì `git reset` để hoàn tác?
- **Trả lời:**
  - **Tránh phá vỡ đồng bộ trong nhóm (Collaboration Safety):** `git reset` viết lại lịch sử (kéo lùi con trỏ về quá khứ và làm biến mất các commit sau đó), đòi hỏi phải dùng `git push --force` để đẩy lên remote. Điều này làm hỏng cấu trúc đồ thị commit của các thành viên khác khi họ pull về. Ngược lại, `git revert` tạo một commit mới đảo ngược thay đổi, tiến về phía trước và bảo toàn toàn bộ lịch sử cũ.
  - **Đảm bảo tính truy vết (Traceability & SCM Audit Trail):** `git revert` lưu lại bằng chứng minh bạch về việc lỗi nào đã xảy ra và được khắc phục/hoàn tác ra sao trong cây commit.
  - **Tuân thủ quy tắc bảo vệ nhánh (Branch Protection):** Các nhánh công khai như `master` và `release/*` thường cấm hoàn toàn Force Push. Do đó, `git reset` không thể đẩy lên remote được, bắt buộc phải dùng `git revert` thông qua PR có review và kiểm thử CI.

---

## 📌 Lab 04 – Release Flow & Phiên bản phát hành

### Câu 1: Vì sao nhánh `release/*` không bao giờ merge ngược lại vào `master`? So sánh với mô hình GitFlow?
- **Trả lời:**
  - **Nguyên lý một chiều trong Release Flow:** Nhánh `release/*` chỉ phục vụ mục đích đóng băng (Freeze Baseline) và bảo trì bản đã xuất xưởng. Mọi tính năng mới chỉ đi một chiều từ `master` $\rightarrow$ `release/*`. Không merge ngược lại để tránh làm ô nhiễm lịch sử commit trên `master` với các merge commit thừa. Nếu có lỗi trên release, ta dùng cơ chế hotfix và `cherry-pick` bản vá chứ không merge toàn bộ nhánh.
  - **So sánh với GitFlow:** GitFlow sử dụng 2 nhánh dài hạn (`master` và `develop`), nhánh release sau khi hoàn tất bắt buộc phải merge kép ngược vào cả hai nhánh, tạo ra đồ thị Git phức tạp và dễ xung đột. Ngược lại, Release Flow chỉ duy trì duy nhất 1 nhánh chính `master`, đồ thị tuyến tính, tinh gọn và tối ưu cho CI/CD.

---

### Câu 2: Vì sao phiên bản ở Lab 04 được đặt là `1.0.0` thay vì `0.4.0`?
- **Trả lời:**
  - **Chuẩn Semantic Versioning (SemVer 2.0.0):** Dải `0.y.z` là giai đoạn thử nghiệm sơ khai (Initial Development), cấu trúc API chưa ổn định. Việc gắn `1.0.0` đánh dấu mốc phiên bản ổn định đầu tiên (First Stable Production-Ready Baseline), chuyển giao phần mềm từ thử nghiệm sang bàn giao chính thức cho người dùng.
  - **Hoàn thiện tính năng cốt lõi:** Đến Lab 04, AIMS-mini đã hoàn chỉnh các tính năng cốt lõi (Cart, DVD, tìm kiếm, in ấn, giảm giá, kiểm soát số lượng, tài liệu và Unit Test tự động). Đặt phiên bản `1.0.0` là một cam kết về tính ổn định và tương thích ngược của API công khai từ thời điểm này trở đi.

---

## 📌 Lab 05 – Hotfix Flow & Bảo trì nhiều phiên bản

### Câu 1: Phân tích ưu và nhược điểm của chiến lược *Upstream First* so với *Release First* khi xử lý hotfix?
- **Trả lời:**
  - **Release First (Sửa trên Release trước rồi đưa về Master):**
    - *Ưu điểm:* Tốc độ phản ứng khẩn cấp cực cao, đưa bản vá tới tay khách hàng/production nhanh nhất mà không bị trì hoãn bởi các đoạn mã mới đang làm dở trên master.
    - *Nhược điểm:* Lập trình viên rất dễ quên không lan truyền ngược về master, dẫn đến việc các bản phát hành lớn tiếp theo lại bị tái phát lỗi cũ (Regression). Đồng thời khi đưa ngược về dễ gặp conflict do master đã đi xa.
  - **Upstream First (Sửa trên Master trước rồi Cherry-pick về Release):**
    - *Ưu điểm:* Mã nguồn gốc (`master`) luôn có bản sửa mới nhất, loại trừ 100% rủi ro tái phát lỗi ở tương lai; quy trình kiểm thử CI toàn diện và chuẩn mực (chuẩn của Linux, Kubernetes).
    - *Nhược điểm:* Thời gian đưa bản vá đến tay người dùng bản cũ có thể lâu hơn vì phải qua quy trình review và kiểm thử nghiêm ngặt trên master trước.

---

### Câu 2: Nếu quên lan truyền bản sửa sang nhánh `release/lab05`, lệnh nào ở Phần F sẽ phát hiện ra sự thiếu sót này?
- **Trả lời:**
  - **Lệnh kiểm toán cấu hình:** `git cherry -v origin/release/lab05 origin/release/lab04`. Nếu thiếu bản vá trên `release/lab05`, lệnh sẽ in ra commit sửa lỗi với **dấu cộng (`+`)**, báo hiệu commit đó chưa có bản tương đương ở `release/lab05`.
  - **Kịch bản kiểm thử hành vi thực tế:** Vòng lặp test `for ref in v1.0.1 v1.1.0 master` sẽ in ra kết quả **`FAIL`** tại mốc `v1.1.0` (do chưa có logic tìm kiếm không phân biệt hoa thường), giúp phát hiện lỗi ngay lập tức trước khi xuất bản.

