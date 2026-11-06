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

## [1.1.0] - 2026-11-06
### Added
- Thêm phương thức sắp xếp giỏ hàng `Cart.sort_by_title()` và `Cart.sort_by_cost()`.
- Thêm chức năng tìm kiếm đĩa theo thể loại `search_by_category()`.