class NotificationStrategy:
    def notify(self, order):
        pass

class EmailNotification(NotificationStrategy):
    def notify(self, order):
        print(f"[Email] Pedido confirmado para {order.customer}")

class SMSNotification(NotificationStrategy):
    def notify(self, order):
        print(f"[SMS] Pedido confirmado para {order.customer}")