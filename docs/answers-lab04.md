# Câu hỏi thảo luận Lab 04 – Release Flow & Phiên bản phát hành

- **Học phần:** IT3180 – Nhập môn Công nghệ phần mềm
- **Chủ đề:** Release Flow, Đóng băng Baseline & Quản lý phiên bản phần mềm (SemVer)
- **Người thực hiện:** PhucHung06 (MSSV: 202416216)

---

### Câu 1: Vì sao nhánh `release/*` không bao giờ merge ngược lại vào `master`? So sánh với mô hình GitFlow?

**Trả lời:**

#### 1. Nguyên lý luồng một chiều trong Release Flow:
- Trong mô hình **Release Flow** (chuẩn quy trình do Microsoft phát triển và được áp dụng trong học phần), nhánh `release/*` được sinh ra từ `master` với mục đích duy nhất: **Đóng băng cấu hình (Freeze Baseline)** để kiểm thử lần cuối, đóng gói sản phẩm và xuất bản bản phát hành ra thị trường/người dùng cuối.
- Dòng chảy của mã nguồn là **luồng một chiều (One-way Flow)** từ `master` $\rightarrow$ `release/*`. 
- **Lý do không merge ngược lại `master`:**
  1. **Bảo toàn tính độc lập của bản phát hành:** Nhánh `release/*` sau khi cắt ra sẽ được "đóng băng" (bật Branch Protection cấm sửa đổi tùy tiện). Nhánh `master` tiếp tục phát triển các tính năng của các phiên bản tương lai mà không bị ràng buộc hay ảnh hưởng bởi nhánh release cũ.
  2. **Tránh ô nhiễm lịch sử commit trên `master`:** Nếu merge ngược lại, cây lịch sử của `master` sẽ phải tiếp nhận các merge commit vòng lặp không cần thiết, làm rối loạn đồ thị commit và gây khó khăn cho việc tra cứu bằng `git log`.
  3. **Xử lý sự cố qua Hotfix/Cherry-pick:** Nếu phát hiện lỗi trên bản release sau khi đã bàn giao, quy trình SCM chuẩn áp dụng cơ chế *Hotfix flow*: bản sửa lỗi được thực hiện trên `master` trước (hoặc trên nhánh hotfix riêng), sau đó dùng lệnh `git cherry-pick` để bốc tách duy nhất commit sửa lỗi đó đưa vào `release/*`, tuyệt đối không merge toàn bộ nhánh vào nhau.

#### 2. So sánh đối chiếu với mô hình GitFlow:

| Tiêu chí | Mô hình Release Flow (Lab 04) | Mô hình GitFlow truyền thống |
|---|---|---|
| **Cấu trúc nhánh chính** | Duy nhất **1 nhánh chính dài hạn**: `master` (hoặc `main`). | Sử dụng **2 nhánh chính dài hạn**: `master` (chứa mã production) và `develop` (chứa mã tích hợp). |
| **Quy tắc merge nhánh Release** | **Không bao giờ merge ngược lại `master`**. Nhánh release sống độc lập hoặc kết thúc vòng đời sau khi bàn giao. | Nhánh `release` sau khi kiểm thử và sửa lỗi xong **bắt buộc phải merge kép** vào cả `master` VÀ `develop`. |
| **Xử lý bản vá (Bugfix / Hotfix)** | Áp dụng chiến lược *Upstream First* / `cherry-pick`: sửa lỗi tập trung rồi chọn lọc đưa commit vào nhánh release cần thiết. | Phải mở nhánh `hotfix` từ `master`, sau khi vá xong lại merge kép vào cả `master` và `develop`. |
| **Độ phức tạp của đồ thị Git** | **Đơn giản, trực quan, tuyến tính**: Phù hợp hoàn hảo với văn hóa DevOps, kiểm thử tự động (CI/CD) và triển khai liên tục. | **Phức tạp, nhiều nhánh đan xen**: Dễ phát sinh xung đột chéo giữa nhánh `release` và nhánh `develop` khi có nhiều lập trình viên cùng làm việc. |

---

### Câu 2: Vì sao phiên bản ở Lab 04 được đặt là `1.0.0` mà không phải `0.4.0`?

**Trả lời:**

#### 1. Tuân thủ quy chuẩn Định danh phiên bản theo ngữ nghĩa (Semantic Versioning - SemVer 2.0.0):
Theo đặc tả của SemVer, cấu trúc số hiệu phiên bản có dạng `MAJOR.MINOR.PATCH`:
- **`MAJOR` (Số chính):** Tăng khi có những thay đổi lớn làm thay đổi kiến trúc hoặc phá vỡ tính tương thích ngược (Breaking Changes).
- **`MINOR` (Số phụ):** Tăng khi bổ sung thêm các tính năng mới nhưng vẫn đảm bảo tương thích ngược.
- **`PATCH` (Bản vá):** Tăng khi thực hiện các bản sửa lỗi nhỏ không thêm tính năng và không phá vỡ tính tương thích.

#### 2. Ý nghĩa kỹ thuật và nghiệp vụ khi nâng lên `1.0.0`:
1. **Chuyển giao từ giai đoạn Thử nghiệm sang Ổn định (Production Ready):**
   - Theo đặc tả SemVer (Điều 4): Dải phiên bản `0.y.z` là giai đoạn phát triển sơ khai (*Initial Development*). Ở giai đoạn này (các bài Lab 01 $\rightarrow$ Lab 03 với `v0.1.0`, `v0.2.0`, `v0.3.0`), sản phẩm chỉ mang tính thử nghiệm nội bộ, kiến trúc còn xáo trộn, API chưa ổn định và có thể thay đổi bất cứ lúc nào.
   - Phiên bản **`1.0.0`** là cột mốc chính thức xác nhận: phần mềm đã thoát khỏi trạng thái bản nháp thử nghiệm, đạt được mức độ ổn định đầu tiên (*First Stable Release Baseline*), sẵn sàng xuất bản và đưa vào môi trường vận hành thực tế cho người dùng cuối.

2. **Hoàn thiện trọn vẹn bộ tính năng cốt lõi (Core Feature Set):**
   - Đến mốc Lab 04, ứng dụng AIMS-mini đã sở hữu đầy đủ bộ khung tính năng cơ bản của một hệ thống thương mại điện tử hoàn chỉnh:
     - Quản lý giỏ hàng và danh mục DVD (`aims.cart`, `aims.dvd`).
     - Hiển thị và in thông tin giỏ hàng (`print_cart`).
     - Tìm kiếm sản phẩm theo tiêu đề (`search_by_title`).
     - Tính toán tiền thanh toán và áp dụng mã giảm giá (`total_cost_with_discount`).
     - Kiểm soát giới hạn nghiêm ngặt số lượng sản phẩm không vượt quá ngưỡng tối đa.
     - Tài liệu hóa hoàn chỉnh: Sơ đồ Use-case, `CHANGELOG.md` và hệ thống Unit Test tự động bao phủ các ca kiểm thử.

3. **Cam kết tính tương thích ngược đối với người dùng (Public API Contract):**
   - Việc phát hành `1.0.0` là một lời tuyên bố và cam kết về mặt kỹ thuật: Từ thời điểm này trở đi, các API công khai của AIMS-mini đã được chuẩn hóa. Bất kỳ sự mở rộng tính năng tiếp theo (như sắp xếp giỏ hàng `sort_by_title` / `sort_by_cost`) sẽ được quản lý nghiêm ngặt qua số hiệu Minor (`1.1.0`), giúp các hệ thống khác tích hợp mà không lo bị đổ vỡ bất ngờ.

