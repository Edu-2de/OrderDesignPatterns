import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.order_facade import OrderProcessorFacade

class OrderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Order Design Patterns - Sistema de Pedidos")
        self.geometry("540x420")
        self.resizable(False, False)
        self.facade = OrderProcessorFacade()
        self.create_widgets()
        self.order_history = []

    def create_widgets(self):
        # Frame do formulário
        form_frame = ttk.LabelFrame(self, text="Novo Pedido", padding=(15, 10))
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Cliente
        ttk.Label(form_frame, text="Cliente:").grid(row=0, column=0, sticky="e")
        self.entry_customer = ttk.Entry(form_frame, width=30)
        self.entry_customer.grid(row=0, column=1, padx=5, pady=3)

        # Itens
        ttk.Label(form_frame, text="Itens (separados por vírgula):").grid(row=1, column=0, sticky="e")
        self.entry_items = ttk.Entry(form_frame, width=30)
        self.entry_items.grid(row=1, column=1, padx=5, pady=3)

        # Endereço
        ttk.Label(form_frame, text="Endereço:").grid(row=2, column=0, sticky="e")
        self.entry_address = ttk.Entry(form_frame, width=30)
        self.entry_address.grid(row=2, column=1, padx=5, pady=3)

        # Pagamento
        ttk.Label(form_frame, text="Pagamento:").grid(row=3, column=0, sticky="e")
        self.payment_var = tk.StringVar()
        self.combo_payment = ttk.Combobox(form_frame, textvariable=self.payment_var, values=["Cartão", "Pix", "Dinheiro"], state="readonly", width=28)
        self.combo_payment.grid(row=3, column=1, padx=5, pady=3)
        self.combo_payment.current(0)

        # Gift wrap e desconto
        self.var_gift_wrap = tk.BooleanVar()
        ttk.Checkbutton(form_frame, text="Embalagem para presente", variable=self.var_gift_wrap).grid(row=4, column=1, sticky="w", pady=3)

        ttk.Label(form_frame, text="Desconto (%):").grid(row=5, column=0, sticky="e")
        self.entry_discount = ttk.Entry(form_frame, width=10)
        self.entry_discount.grid(row=5, column=1, sticky="w", padx=5, pady=3)

        # Botão de criar pedido
        ttk.Button(form_frame, text="Criar Pedido", command=self.process_order).grid(row=6, column=0, columnspan=2, pady=10)

        # Frame do histórico
        history_frame = ttk.LabelFrame(self, text="Histórico de Pedidos", padding=(10, 5))
        history_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        self.txt_history = scrolledtext.ScrolledText(history_frame, height=8, width=62, state="disabled", font=("Consolas", 9))
        self.txt_history.pack(fill="both", expand=True)

    def process_order(self):
        customer = self.entry_customer.get().strip()
        items = self.entry_items.get().strip()
        address = self.entry_address.get().strip()
        payment = self.payment_var.get()
        gift_wrap = self.var_gift_wrap.get()
        discount = self.entry_discount.get().strip()

        # Validação básica
        if not customer or not items or not address or not payment:
            messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos obrigatórios!")
            return

        try:
            items_list = [item.strip() for item in items.split(",") if item.strip()]
            discount_val = int(discount) if discount else None
            order = self.facade.criar_e_processar_pedido(
                customer=customer,
                items=items_list,
                address=address,
                payment=payment,
                gift_wrap=gift_wrap,
                discount=discount_val
            )
            self.show_order(order)
            self.add_to_history(order)
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Erro ao criar pedido", str(e))

    def show_order(self, order):
        messagebox.showinfo("Pedido Criado", f"Pedido criado com sucesso!\n\n{order}")

    def add_to_history(self, order):
        self.txt_history.config(state="normal")
        self.txt_history.insert("end", f"{order}\n{'-'*60}\n")
        self.txt_history.see("end")
        self.txt_history.config(state="disabled")

    def clear_form(self):
        self.entry_customer.delete(0, "end")
        self.entry_items.delete(0, "end")
        self.entry_address.delete(0, "end")
        self.combo_payment.current(0)
        self.var_gift_wrap.set(False)
        self.entry_discount.delete(0, "end")

if __name__ == "__main__":
    app = OrderApp()
    app.mainloop()