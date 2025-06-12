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

    # def set_items(self, items):
    #    self.items = address
    #    return self

    def set_address(self, address):
        self.address = address
        return self

    def set_payment(self, payment):
        self.payment = payment
        return self

    def build(self):
        if not self.customer or not self.items or not self.address or not self.payment:
            raise ValueError("Pedido incompleto!")
        return Order(
            customer=self.customer,
            items=self.items,
            address=self.address,
            payment=self.payment
        )