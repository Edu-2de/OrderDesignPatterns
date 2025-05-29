from src.order_builder import OrderBuilder

class OrderProcessorFacade:
    def __init__(self):
        self.builder = OrderBuilder()

    def criar_e_processar_pedido(self, customer, items, address, payment, gift_wrap=False, discount=None):
        builder = (self.builder
                   .set_customer(customer)
                   .set_address(address)
                   .set_payment(payment))
        for item in items:
            builder.add_item(item)
        order = builder.build()

        # Decorators
        if gift_wrap:
            from src.order_decorator import GiftWrapDecorator
            order = GiftWrapDecorator(order)
        if discount:
            from src.order_decorator import DiscountDecorator
            order = DiscountDecorator(order, discount)

        self._process_payment(order)
        self._enviar_notificacao(order)
        return order

    def _process_payment(self, order):
        # Simula processamento de pagamento
        pass

    def _enviar_notificacao(self, order):
        # Simula envio de notificação
        pass