def search_by_title(items, keyword):
    """Tìm kiếm đĩa DVD theo tiêu đề."""
    return [dvd for dvd in items if keyword in dvd.title]