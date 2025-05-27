# Padrões de Projeto - Entrega 1

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

## Testes

- Testa se o pedido é criado corretamente com todos os campos.
- Testa se não é possível criar um pedido incompleto.