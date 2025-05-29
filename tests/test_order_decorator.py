import unittest
from src.order import Order
from src.order_decorator import GiftWrapDecorator, DiscountDecorator

class TestOrderDecorator(unittest.TestCase):
    def test_gift_wrap(self):
        order = Order("Maria", ["Pizza"], "Rua XPTO, 123", "Cartão")
        decorated = GiftWrapDecorator(order)
        self.assertIn("Embalagem para presente", repr(decorated))

    def test_discount(self):
        order = Order("Maria", ["Pizza"], "Rua XPTO, 123", "Cartão")
        decorated = DiscountDecorator(order, 10)
        self.assertIn("Desconto: 10%", repr(decorated))

if __name__ == "__main__":
    unittest.main()