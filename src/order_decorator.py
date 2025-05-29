from src.order import Order

class OrderDecorator(Order):
    def __init__(self, order):
        self._order = order

    def __repr__(self):
        return repr(self._order)

class GiftWrapDecorator(OrderDecorator):
    def __repr__(self):
        return f"{repr(self._order)} [Embalagem para presente]"

class DiscountDecorator(OrderDecorator):
    def __init__(self, order, discount):
        super().__init__(order)
        self.discount = discount

    def __repr__(self):
        return f"{repr(self._order)} [Desconto: {self.discount}%]"