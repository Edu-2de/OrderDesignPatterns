class Order:
    def __init__(self, customer, items, address, payment):
        self.customer = customer
        self.items = items
        self.address = address
        self.payment = payment

    def __repr__(self):
        gift_wrap = getattr(self, 'gift_wrap', False)
        discount = getattr(self, 'discount', None)
        return (f"Order(customer={self.customer}, items={self.items}, address={self.address}, payment={self.payment}, "
                f"gift_wrap={gift_wrap}, discount={discount})")