
## Fase 1: Padrão Criacional

### **Builder**

#### Por que Builder?

O padrão Builder facilita a construção de objetos complexos (como um pedido de pizza), permitindo configurar cada parte separadamente de forma legível e segura.

#### Como foi implementado?

O `OrderBuilder` permite criar um pedido passo a passo, garantindo que nenhum pedido seja criado incompleto.

```python
order = (OrderBuilder()
         .set_customer("Maria")
         .add_item("Pizza Margherita")
         .set_address("Rua XPTO, 123")
         .set_payment("Cartão")
         .build())
```

---

## Fase 2: Padrões Estruturais

- **Decorator**  
  Permite adicionar funcionalidades extras ao pedido (ex: embalagem para presente, desconto), sem alterar sua estrutura base.

- **Facade**  
  Fornece uma interface simplificada para criar e processar pedidos, escondendo a complexidade dos detalhes internos (pagamento, notificação, etc).

#### Por que foram escolhidos?

- **Decorator:** Para adicionar novas funcionalidades ao pedido de forma flexível e sem modificar a classe principal.
- **Facade:** Para simplificar o fluxo de criação e processamento de pedidos, facilitando o uso do sistema por outras partes do código.

#### Como foi implementado?

##### Decorator

```python
order = Order("Maria", ["Pizza Margherita"], "Rua XPTO, 123", "Cartão")
order = GiftWrapDecorator(order)
order = DiscountDecorator(order, 10)
print(order)
# Order(customer=Maria, ...) [Embalagem para presente] [Desconto: 10%]
```

##### Facade

```python
facade = OrderProcessorFacade()
order = facade.criar_e_processar_pedido(
    customer="João",
    items=["Pizza Calabresa"],
    address="Rua ABC, 45",
    payment="Pix",
    gift_wrap=True,
    discount=5
)
print(order)
```

---

## Fase 3: Padrões Comportamentais

- **Observer**  
  Permite notificar automaticamente diferentes partes do sistema (ex: cozinha, cliente) quando um pedido é criado ou finalizado, sem acoplamento direto entre as classes.

- **Strategy**  
  Permite trocar dinamicamente o algoritmo de notificação do cliente (ex: Email, SMS), tornando o sistema flexível para diferentes formas de comunicação.

#### Por que foram escolhidos?

- **Observer:** Para desacoplar o fluxo de notificação, permitindo que múltiplos interessados sejam avisados sobre eventos do pedido sem dependências diretas.
- **Strategy:** Para permitir a troca dinâmica da forma de notificação do cliente, facilitando a extensão para novos canais (ex: WhatsApp, Push).

#### Como foi implementado?

##### Observer

```python
from src.observer import OrderSubject, KitchenObserver, CustomerObserver
from src.strategy import EmailNotification

subject = OrderSubject()
subject.attach(KitchenObserver())
subject.attach(CustomerObserver(EmailNotification()))
subject.notify(order)  # Notifica todos os observers sobre o novo pedido
```

##### Strategy

```python
from src.strategy import EmailNotification, SMSNotification

notifier = EmailNotification()
notifier.notify(order)  # Envia email

notifier = SMSNotification()
notifier.notify(order)  # Envia SMS
```

No sistema, a estratégia de notificação pode ser trocada dinamicamente conforme o tipo de pagamento ou preferência do cliente.

---

## Testes

- Testes unitários cobrem os decoradores, o facade, o observer e o strategy, garantindo que a composição de funcionalidades e os comportamentos dinâmicos funcionem corretamente.

---

## Interface Gráfica

O sistema possui uma interface gráfica feita com Tkinter, onde o usuário pode:
- Escolher pizzas do cardápio
- Personalizar ingredientes
- Selecionar forma de pagamento
- Escolher embalagem (normal ou presente)
- Visualizar o pedido sendo montado e cortado
- Finalizar o pedido com notificações automáticas para cozinha e cliente

---

## Como executar

1. Instale os requisitos (se houver).
2. Execute o sistema:
   ```bash
   python src/order_gui.py
   ```
3. Execute os testes:
   ```bash
   python -m unittest discover tests
   ```

---