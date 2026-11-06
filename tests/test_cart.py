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
    def test_sort_by_title_and_cost(self):
        cart = Cart()
        dvd_a = DigitalVideoDisc("A", "Cat", "Dir", 90, 20.0)
        dvd_b = DigitalVideoDisc("B", "Cat", "Dir", 90, 10.0)
        cart.add_dvd(dvd_b)
        cart.add_dvd(dvd_a)

        cart.sort_by_title()
        self.assertEqual(cart.items[0].title, "A")

        cart.sort_by_cost()
        self.assertEqual(cart.items[0].title, "A")  # cost 20.0 cao hơn 10.0

if __name__ == "__main__":
    unittest.main()

