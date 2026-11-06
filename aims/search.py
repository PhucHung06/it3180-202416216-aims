def search_by_category(items, category):
    """Tìm kiếm đĩa DVD theo thể loại."""
    return [dvd for dvd in items if dvd.category and category.lower() == dvd.category.lower()]


def search_by_title(items, keyword):
    """Tìm kiếm đĩa DVD theo tiêu đề."""
    return [dvd for dvd in items if keyword.lower() in dvd.title.lower()]