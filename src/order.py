class Order:
    def __init__(self, customer, items, address, payment):
        self.customer = customer
        self.items = items
        self.address = address
        self.payment = payment

    def __repr__(self):
        return f"Order(customer={self.customer}, items={self.items}, address={self.address}, payment={self.payment})"