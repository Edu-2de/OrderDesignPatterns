import unittest
from src.order_builder import OrderBuilder

class TestOrderBuilder(unittest.TestCase):
    def test_builder_creates_complete_order(self):
        builder = OrderBuilder()
        order = (builder
                 .set_customer("Maria")
                 .add_item("Pizza")
                 .add_item("Refrigerante")
                 .set_address("Rua XPTO, 123")
                 .set_payment("Cartão")
                 .build())
        self.assertEqual(order.customer, "Maria")
        self.assertEqual(order.items, ["Pizza", "Refrigerante"])
        self.assertEqual(order.address, "Rua XPTO, 123")
        self.assertEqual(order.payment, "Cartão")

    def test_builder_incomplete_order_raises(self):
        builder = OrderBuilder()
        builder.set_customer("João")
        with self.assertRaises(ValueError):
            builder.build()

if __name__ == "__main__":
    unittest.main()