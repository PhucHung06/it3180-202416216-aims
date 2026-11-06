# Câu hỏi thảo luận Lab 03 – Bugfix Flow, Xung đột & Hoàn tác

- **Học phần:** IT3180 – Nhập môn Công nghệ phần mềm
- **Chủ đề:** Bugfix Flow, Xung đột (Merge Conflict) & Kỹ thuật hoàn tác an toàn
- **Người thực hiện:** PhucHung06 (MSSV: 202416216)

---

### Câu 1: Merge Base là gì? Vai trò của nó khi Git giải quyết xung đột?

**Trả lời:**

#### 1. Khái niệm "Merge Base" (Best Common Ancestor):
- Trong mô hình đồ thị có hướng không chu trình (DAG) của Git, **Merge Base** là **commit tổ tiên chung gần nhất** giữa hai nhánh (hoặc hai commit) chuẩn bị được hợp nhất (merge).
- Ta có thể tra cứu mã băm commit của Merge Base giữa hai nhánh bằng lệnh:
  ```bash
  git merge-base <branch_A> <branch_B>
  ```

#### 2. Vai trò của Merge Base trong thuật toán 3-Way Merge:
Git không dùng phép so sánh 2 chiều (2-way diff) đơn thuần giữa đỉnh hai nhánh, mà áp dụng thuật toán **3-way merge** với 3 điểm tham chiếu:
- **Base (O):** Commit tổ tiên chung gần nhất (Merge Base).
- **Ours / HEAD (A):** Commit đỉnh của nhánh hiện tại đang đứng.
- **Theirs / Incoming (B):** Commit đỉnh của nhánh chuẩn bị gộp vào.

Merge Base đóng vai trò là **hệ quy chiếu gốc (Reference Baseline)** để Git tính toán độ lệch (delta changes):
$$\Delta_A = A - \text{Base} \quad (\text{Những thay đổi do nhánh } A \text{ tạo ra})$$
$$\Delta_B = B - \text{Base} \quad (\text{Những thay đổi do nhánh } B \text{ tạo ra})$$

#### 3. Cách Git tự động xử lý và phát hiện xung đột:
- **Tự động hợp nhất (Clean Merge):**
  - Nếu một dòng code ở nhánh $A$ có thay đổi so với Base, trong khi ở nhánh $B$ dòng đó vẫn giống hệt Base: Git tự động nhận biết nhánh $B$ không can thiệp và áp dụng thay đổi của nhánh $A$.
  - Tương tự, nếu nhánh $B$ sửa còn nhánh $A$ không sửa: Git áp dụng thay đổi của $B$.
  - Nếu hai nhánh sửa đổi ở các file khác nhau hoặc các dòng code tách biệt nhau: Git tự động gộp cả hai thay đổi một cách an toàn mà không cần con người can thiệp.
- **Phát hiện xung đột (Conflict Detection):**
  - Khi cả hai nhánh $A$ và $B$ đều sửa đổi trên **cùng một dòng code** (hoặc cùng một khối code liền kề) so với Merge Base, nhưng nội dung sửa đổi ở $A$ và $B$ lại **khác nhau**: Git không thể tự quyết định thay đổi nào là chính xác.
  - Khi đó, Git dừng tiến trình merge, giữ nguyên trạng thái và đánh dấu vùng xung đột bằng các ký hiệu (`<<<<<<< HEAD`, `=======`, `>>>>>>>`), yêu cầu lập trình viên can thiệp thủ công để chọn lọc hoặc kết hợp nội dung mong muốn.

---

### Câu 2: Vì sao trên các nhánh như `master` hay `release/*` phải dùng `git revert` thay vì `git reset` để hoàn tác?

**Trả lời:**

#### 1. So sánh bản chất kỹ thuật giữa `git reset` và `git revert`:

| Tiêu chí | `git reset` | `git revert` |
|---|---|---|
| **Cơ chế hoạt động** | **Kéo lùi con trỏ (Rewriting History):** Dời con trỏ nhánh về một commit trong quá khứ, loại bỏ các commit sau đó khỏi lịch sử nhánh. | **Tiến về phía trước (Forward-Moving Undo):** Tạo ra một **commit mới hoàn toàn** có nội dung đảo ngược (inverse diff) commit lỗi. |
| **Ảnh hưởng lịch sử** | Viết lại và làm mất dấu lịch sử commit cũ. | Bảo toàn nguyên vẹn toàn bộ lịch sử commit, hoàn toàn minh bạch. |
| **Cách đồng bộ lên Remote** | Bắt buộc phải dùng `git push --force` (vì lịch sử cục bộ bị thụt lùi so với remote). | Đẩy lên bình thường bằng `git push` tiêu chuẩn (thông qua Pull Request an toàn). |
| **Phạm vi áp dụng phù hợp** | Chỉ dùng cho các commit cục bộ cá nhân **chưa từng push** lên remote. | Áp dụng bắt buộc cho các **nhánh công khai, dùng chung** (`master`, `main`, `release/*`). |

#### 2. Các lý do bắt buộc phải dùng `git revert` trên `master` hoặc `release/*`:

1. **Bảo vệ tính toàn vẹn và tránh phá vỡ kho mã nguồn của nhóm (Collaboration Safety):**
   - Các nhánh `master` và `release/*` là nhánh dùng chung của toàn bộ đội ngũ phát triển.
   - Nếu một lập trình viên dùng `git reset` rồi ép đẩy (`push --force`), lịch sử trên remote bị cắt ngắn. Khi các thành viên khác kéo code (`git pull`), máy của họ sẽ rơi vào tình trạng phân kỳ lịch sử (diverged branches). Việc này dễ dẫn đến việc các commit lỗi vô tình bị merge ngược trở lại, hoặc tệ hơn là gây mất mát mã nguồn của người khác.

2. **Đảm bảo tính truy vết và kiểm toán phần mềm (Traceability & SCM Audit Trail):**
   - Theo nguyên tắc Quản lý cấu hình phần mềm (SCM), mọi sự thay đổi trong vòng đời sản phẩm cần được lưu trữ minh bạch.
   - `git revert` tạo ra commit hoàn tác rõ ràng (ghi rõ lý do revert, mã commit bị revert). Nhờ đó, người quản trị hoặc kiểm toán viên có thể dễ dàng theo dõi: commit nào gây ra lỗi, tại sao phải revert và ai là người thực hiện.

3. **Tương thích với cơ chế bảo vệ nhánh (Branch Protection Rules & CI/CD):**
   - Trong môi trường làm việc chuyên nghiệp, nhánh `master` và `release/*` luôn được kích hoạt quy tắc bảo vệ: **cấm tuyệt đối Force Push** (`push --force` bị reject).
   - Vì vậy, `git reset` là bất khả thi trên các nhánh này. Quy trình chuẩn bắt buộc là tạo nhánh bugfix, chạy `git revert` (hoặc `git revert -m 1` đối với merge commit), đẩy lên và mở Pull Request để chạy kiểm thử tự động (CI) và được đồng nghiệp review trước khi merge.

