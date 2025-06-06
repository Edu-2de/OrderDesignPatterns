import unittest
from src.strategy import EmailNotification, SMSNotification
from src.observer import OrderSubject, KitchenObserver, CustomerObserver
from src.order import Order

class TestStrategyObserver(unittest.TestCase):
    def setUp(self):
        self.order = Order("Cliente", ["Pizza"], "Rua Teste", "Cartão")

    def test_email_notification_strategy(self):
        strategy = EmailNotification()
        # Para testar saída no terminal, use assertLogs ou patch print se quiser
        strategy.notify(self.order)  # Deve imprimir mensagem de email

    def test_sms_notification_strategy(self):
        strategy = SMSNotification()
        strategy.notify(self.order)  # Deve imprimir mensagem de SMS

    def test_observer_notifies_all(self):
        subject = OrderSubject()
        kitchen = KitchenObserver()
        customer = CustomerObserver(EmailNotification())
        subject.attach(kitchen)
        subject.attach(customer)
        # Aqui, ambos kitchen e customer devem ser notificados (imprime no terminal)
        subject.notify(self.order)

if __name__ == "__main__":
    unittest.main()