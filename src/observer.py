class Observer:
    def update(self, order):
        pass

class KitchenObserver(Observer):
    def update(self, order):
        print(f"[Cozinha] Novo pedido: {order}")

class CustomerObserver(Observer):
    def __init__(self, notify_strategy):
        self.notify_strategy = notify_strategy
    def update(self, order):
        self.notify_strategy.notify(order)

class OrderSubject:
    def __init__(self):
        self.observers = []
    def attach(self, observer):
        self.observers.append(observer)
    def notify(self, order):
        for obs in self.observers:
            obs.update(order)