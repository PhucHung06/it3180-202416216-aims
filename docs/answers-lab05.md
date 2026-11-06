# Câu hỏi thảo luận Lab 05 – Hotfix Flow & Bảo trì nhiều phiên bản

- **Học phần:** IT3180 – Nhập môn Công nghệ phần mềm
- **Chủ đề:** Hotfix Flow, Lan truyền bản vá & Bảo trì đa phiên bản (Multi-version Maintenance)
- **Người thực hiện:** PhucHung06 (MSSV: 202416216)

---

### Câu 1: Phân tích ưu, nhược điểm của chiến lược *Upstream First* so với *Release First* khi xử lý hotfix?

**Trả lời:**

Trong quản lý cấu hình phần mềm và bảo trì hệ thống thực tế, khi phát hiện lỗi nghiêm trọng trên một phiên bản đã xuất xưởng, đội ngũ phát triển thường đứng trước hai sự lựa chọn về luồng xử lý bản vá:

#### 1. Chiến lược *Release First* (Sửa trên nhánh Release trước rồi đưa ngược về Upstream/Master):
- **Quy trình:** Tạo nhánh hotfix trực tiếp từ nhánh release đang bị lỗi (ví dụ: `release/lab04`), kiểm thử, phát hành bản vá khẩn cấp `PATCH` (`v1.0.1`) cho người dùng/khách hàng, sau đó mới tìm cách đưa bản sửa này về `master` (hoặc các nhánh release kế tiếp) bằng `cherry-pick`.
- **Ưu điểm:**
  - **Tốc độ phản ứng khẩn cấp cực cao:** Khách hàng hoặc hệ thống production đang gặp sự cố được tiếp cận bản vá trong thời gian ngắn nhất có thể mà không bị trì hoãn bởi các đoạn mã mới đang phát triển trên `master`.
  - **Giảm thiểu rủi ro lan truyền mã chưa kiểm chứng:** Bản sửa chỉ tập trung vào codebase cũ đã ổn định của nhánh release, không bị phụ thuộc vào các tính năng mới chưa hoàn thiện trên `master`.
- **Nhược điểm:**
  - **Nguy cơ tái phát lỗi (Regression Risk):** Do áp lực hoàn thành phát hành nóng, lập trình viên rất dễ quên hoặc trì hoãn việc đưa bản vá ngược lại `master`. Hậu quả là ở các phiên bản lớn tiếp theo (ví dụ: `1.1.0`, `2.0.0`), lỗi cũ lại bất ngờ tái xuất hiện dù đã từng được sửa.
  - **Xung đột mã nguồn khi đưa ngược về:** Mã nguồn trên `master` đã tiến hóa xa so với bản release cũ, nên việc `cherry-pick` ngược từ bản release cũ về `master` có thể gặp xung đột mã nguồn phức tạp.

#### 2. Chiến lược *Upstream First* (Sửa trên Master trước rồi Cherry-pick về Release):
- **Quy trình:** Bản sửa lỗi được thực hiện, review và kiểm thử nghiêm ngặt trên nhánh thượng nguồn (`master`) trước. Khi bản sửa đã được kiểm chứng an toàn trên nhánh chính, lập trình viên mới sử dụng `git cherry-pick -x` để bốc tách commit sửa lỗi đưa vào các nhánh `release/*` đang cần bảo trì. (Đây là quy chuẩn phổ biến trong các dự án nguồn mở lớn như Linux Kernel, Kubernetes, Chromium).
- **Ưu điểm:**
  - **Đảm bảo tính vĩnh cửu của bản sửa:** Mã nguồn gốc (`master`) luôn luôn sở hữu bản sửa lỗi mới nhất, loại trừ 100% rủi ro tái phát lỗi ở tất cả các thế hệ phiên bản tương lai.
  - **Tối ưu hóa quy trình kiểm thử và tích hợp liên tục (CI):** Bản sửa được kiểm tra tính tương thích với toàn bộ kiến trúc mới nhất của hệ thống trước khi quyết định đưa vào các phiên bản hỗ trợ dài hạn (LTS).
- **Nhược điểm:**
  - **Thời gian đưa bản vá đến tay người dùng bản cũ có thể chậm hơn:** Cần phải đi qua quy trình duyệt code và chạy CI đầy đủ trên `master` trước khi được tách ra cho release.
  - **Đòi hỏi kỹ thuật bốc tách sạch:** Commit sửa lỗi trên `master` phải được viết độc lập, cô lập (atomic commit) để khi cherry-pick về nhánh release cũ không bị kéo theo các dependencies hoặc cú pháp mới chưa được hỗ trợ ở bản cũ.

#### Bảng so sánh tổng hợp:

| Tiêu chí so sánh | Release First | Upstream First |
|---|---|---|
| **Ưu tiên hàng đầu** | Thời gian khắc phục sự cố cho khách hàng (MTTR). | Tính toàn vẹn và không tái phát lỗi của toàn hệ thống. |
| **Rủi ro lớn nhất** | Quên lan truyền về master $\rightarrow$ tái phát lỗi ở bản sau. | Thời gian phát hành bản vá có thể lâu hơn một chút. |
| **Phù hợp nhất khi** | Sự cố nghiêm trọng ở Production cần vá tức thì (Hotfix khẩn). | Bảo trì định kỳ, vá lỗi bảo mật quy chuẩn của doanh nghiệp lớn. |

---

### Câu 2: Nếu quên lan truyền bản sửa sang nhánh `release/lab05`, lệnh nào ở Phần F sẽ phát hiện ra sự thiếu sót này?

**Trả lời:**

Nếu lập trình viên chỉ sửa trên `release/lab04`, đưa về `master` nhưng **quên không lan truyền sang `release/lab05`**, hai phương pháp kiểm toán ở Phần F sẽ lập tức phát hiện ra sự thiếu sót:

#### 1. Lệnh kiểm toán cấu hình: `git cherry -v`
Sử dụng lệnh:
```bash
git cherry -v origin/release/lab05 origin/release/lab04
```
- **Nguyên lý hoạt động:** Lệnh `git cherry` so sánh nội dung thay đổi (patch-id) giữa hai nhánh để xem những commit nào ở nhánh thứ hai (`release/lab04`) chưa có bản tương đương ở nhánh thứ nhất (`release/lab05`).
- **Dấu hiệu phát hiện thiếu sót:**
  - Nếu nhánh `release/lab05` **ĐÃ** có bản vá: Commit sửa lỗi sẽ xuất hiện với dấu trừ (`-`), nghĩa là đã có bản tương đương.
  - Nếu nhánh `release/lab05` **CHƯA** có bản vá: Lệnh sẽ hiển thị commit sửa lỗi với **dấu cộng (`+`)**:
    ```text
    + bdb30b9... fix: make search_by_title case-insensitive
    ```
    Dấu `+` là bằng chứng rõ ràng chỉ ra commit sửa lỗi này vẫn còn thiếu trên `release/lab05`!

---

#### 2. Vòng lặp kiểm thử hành vi thực tế (Functional Verification Script):
Chạy kịch bản kiểm tra tự động trên cả 3 mốc:
```bash
for ref in v1.0.1 v1.1.0 master; do
  git switch --detach -q $ref; printf "%-8s: " $ref
  python -c "from aims.dvd import DigitalVideoDisc as D; from aims.search import search_by_title; print('FOUND' if len(search_by_title([D('The Lion King')], 'lion')) == 1 else 'FAIL')"
done; git switch -q master
```
- **Dấu hiệu phát hiện:**
  - Nếu quên lan truyền bản sửa sang `release/lab05`, phiên bản `v1.1.0` chưa có logic `.lower()` trong hàm tìm kiếm.
  - Kết quả kiểm thử sẽ in ra thông báo thất bại:
    ```text
    v1.0.1  : FOUND
    v1.1.0  : FAIL   <--- Lỗi được phát hiện ngay tại đây!
    master  : FOUND
    ```
  Script kiểm tra chức năng sẽ ngay lập tức chặn quy trình xuất xưởng và cảnh báo cho đội ngũ QA/Release Engineer biết bản `1.1.0` chưa sẵn sàng.

