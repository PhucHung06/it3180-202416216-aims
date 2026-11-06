import unittest
from aims.cart import Cart, MAX_NUMBERS_ORDERED
from aims.dvd import DigitalVideoDisc

class TestCartLimit(unittest.TestCase):
    def test_add_dvd_until_full(self):
        cart = Cart()
        # Thêm 20 đĩa đầu tiên -> Phải thành công (True)
        for i in range(MAX_NUMBERS_ORDERED):
            dvd = DigitalVideoDisc(f"Title {i}", "Category", "Director", 90, 10.0)
            self.assertTrue(cart.add_dvd(dvd))
        
        # Thử thêm đĩa thứ 21 -> Phải bị từ chối (False)
        dvd_21 = DigitalVideoDisc("Title 21", "Category", "Director", 90, 10.0)
        self.assertFalse(cart.add_dvd(dvd_21))

    def test_discount_calculation(self):
        cart = Cart()
        dvd = DigitalVideoDisc("Sample DVD", "Category", "Director", 90, 100.0)
        cart.add_dvd(dvd)
        # Giảm giá 20% trên 100$ -> Phải còn 80$
        self.assertAlmostEqual(cart.total_cost_with_discount(20), 80.0)
        # Percent không hợp lệ -> Phải raise ValueError
        with self.assertRaises(ValueError):
            cart.total_cost_with_discount(150)
        with self.assertRaises(ValueError):
            cart.total_cost_with_discount(-10)


if __name__ == "__main__":
    unittest.main()

