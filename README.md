### Fase 1: Padrões de Projeto 
## Padrão Utilizado

- **Builder**

## Por que Builder?

O padrão Builder facilita a construção de objetos complexos (como um pedido de compra), permitindo configurar cada parte separadamente de forma legível e segura.

## Como foi implementado?

O `OrderBuilder` permite criar um pedido passo a passo, garantindo que nenhum pedido seja criado incompleto.

```python
order = (OrderBuilder()
         .set_customer("Maria")
         .add_item("Pizza")
         .add_item("Refrigerante")
         .set_address("Rua XPTO, 123")
         .set_payment("Cartão")
         .build())
```


### Fase 2: Estruturais

- **Decorator**
  utilizando dois padrões estruturais
  Permite adicionar funcionalidades extras ao pedido (ex: embalagem para presente, desconto), sem alterar sua estrutura base.
- **Facade**  
  Fornece uma interface simplificada para criar e processar pedidos, escondendo a complexidade dos detalhes internos (pagamento, notificação, etc).

## Por que foram escolhidos?

- **Decorator** foi escolhido para permitir adicionar novas funcionalidades ao pedido de forma flexível e sem modificar a classe principal.
- **Facade** foi escolhido para simplificar o fluxo de criação e processamento de pedidos, facilitando o uso do sistema por outras partes do código.

## Como foi implementado?

### Decorator

```python
order = Order("Maria", ["Pizza"], "Rua XPTO, 123", "Cartão")
order = GiftWrapDecorator(order)
order = DiscountDecorator(order, 10)
print(order)
# Order(customer=Maria, ...) [Embalagem para presente] [Desconto: 10%]
```

### Facade

```python
facade = OrderProcessorFacade()
order = facade.criar_e_processar_pedido(
    customer="João",
    items=["Hambúrguer"],
    address="Rua ABC, 45",
    payment="Pix",
    gift_wrap=True,
    discount=5
)
print(order)
```

## Testes

- Testes unitários cobrem os decoradores e o facade, garantindo que a composição de funcionalidades funcione corretamente.
