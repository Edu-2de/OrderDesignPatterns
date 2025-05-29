import unittest
from src.order_facade import OrderProcessorFacade

class TestOrderFacade(unittest.TestCase):
    def test_criar_e_processar_pedido_simples(self):
        facade = OrderProcessorFacade()
        order = facade.criar_e_processar_pedido(
            customer="João",
            items=["Hambúrguer"],
            address="Rua ABC, 45",
            payment="Pix"
        )
        self.assertIn("Order(customer=João", repr(order))

    def test_criar_e_processar_pedido_com_decorators(self):
        facade = OrderProcessorFacade()
        order = facade.criar_e_processar_pedido(
            customer="Ana",
            items=["Sushi"],
            address="Rua Sushi, 99",
            payment="Dinheiro",
            gift_wrap=True,
            discount=15
        )
        self.assertIn("Embalagem para presente", repr(order))
        self.assertIn("Desconto: 15%", repr(order))

if __name__ == "__main__":
    unittest.main()