# Changelog - AIMS Mini

Tất cả các thay đổi đáng chú ý của dự án sẽ được ghi lại tại tệp này.
Định dạng dựa trên [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

## [1.0.0] - 2026-11-06
### Added
- Khởi tạo package `aims` chứa `Cart` và `DigitalVideoDisc`.
- Thêm phương thức in giỏ hàng `Cart.print_cart()`.
- Thêm chức năng tìm kiếm đĩa theo tiêu đề `search_by_title()`.
- Thêm tính năng áp dụng giảm giá `Cart.total_cost_with_discount()`.
- Thêm sơ đồ Use-case cho ứng dụng.

### Fixed
- Sửa lỗi giỏ hàng nhận đĩa thứ 21 vượt quá giới hạn tối đa (#6).

## [1.0.1] - 2026-11-06
### Fixed
- Sửa lỗi tìm kiếm đĩa DVD theo tiêu đề không phân biệt hoa thường (#20).