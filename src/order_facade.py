from src.order_builder import OrderBuilder
from src.observer import OrderSubject, KitchenObserver, CustomerObserver
from src.strategy import EmailNotification, SMSNotification

class OrderProcessorFacade:
    def __init__(self):
        self.subject = OrderSubject()
        self.subject.attach(KitchenObserver())
        # Por padrão, notifica cliente por email
        self.customer_observer = CustomerObserver(EmailNotification())
        self.subject.attach(self.customer_observer)

    def set_notification_strategy(self, strategy):
        self.customer_observer.notify_strategy = strategy

    def criar_e_processar_pedido(self, customer, items, address, payment, gift_wrap=False, discount=None, notification_type="email"):
        builder = OrderBuilder()
        builder.set_customer(customer).add_item(items).set_address(address).set_payment(payment)
        if gift_wrap:
            builder.set_gift_wrap(True)
        if discount:
            builder.set_discount(discount)
        order = builder.build()
        # Troca a estratégia se necessário
        if notification_type == "sms":
            self.set_notification_strategy(SMSNotification())
        else:
            self.set_notification_strategy(EmailNotification())
        self.subject.notify(order)
        return order


    def _process_payment(self, order):
        # Simula processamento de pagamento
        pass
