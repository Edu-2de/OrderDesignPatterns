from src.order import Order

class OrderBuilder:
    def __init__(self):
        self.customer = None
        self.items = []
        self.address = None
        self.payment = None

    def set_customer(self, customer):
        self.customer = customer
        return self

    def add_item(self, item):
        self.items.append(item)
        return self

    def set_address(self, address):
        self.address = address
        return self

    def set_payment(self, payment):
        self.payment = payment
        return self

    # Implementar aqui a funcionalidade de presente embalado
    def set_gift_wrap(self, gift_wrap):
        self.gift_wrap = gift_wrap
        return self

    # Implementar aqui a funcionalidade de desconto
    def set_discount(self, discount):
        self.discount = discount
        return self

    # Adicionar propriedades ao método construtor aqui no builder de disconto e gift

    def build(self):
        if not self.customer or not self.items or not self.address or not self.payment:
            raise ValueError("Pedido incompleto!")
        order = Order(
            customer=self.customer,
            items=self.items,
            address=self.address,
            payment=self.payment
        )

        order.gift_wrap = getattr(self, 'gift_wrap', False)
        order.discount = getattr(self, 'discount', None)
        return order