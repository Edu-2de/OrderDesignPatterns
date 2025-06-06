import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, Canvas

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.order_facade import OrderProcessorFacade

MENU = [
    ("Margherita", ["Molho", "Queijo", "Tomate", "Manjericão"]),
    ("Calabresa", ["Molho", "Queijo", "Calabresa", "Cebola"]),
    ("Quatro Queijos", ["Molho", "Queijo", "Catupiry"]),
    ("Portuguesa", ["Molho", "Queijo", "Presunto", "Ovo", "Cebola", "Azeitona", "Pimentão"]),
    ("Frango com Catupiry", ["Molho", "Queijo", "Frango", "Catupiry"]),
    ("Vegetariana", ["Molho", "Queijo", "Tomate", "Cebola", "Azeitona", "Pimentão", "Manjericão"]),
]

INGREDIENTS = [
    ("Calabresa", "#d7263d"),
    ("Tomate", "#ff7f50"),
    ("Azeitona", "#4e944f"),
    ("Cebola", "#f7d6e0"),
    ("Manjericão", "#2e8b57"),
    ("Frango", "#f5c16c"),
    ("Catupiry", "#fffbe6"),
    ("Pimentão", "#8fd19e"),
]

class PizzaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pizzaria - Sistema de Pedidos")
        self.geometry("1100x700")
        self.configure(bg="#191c1f")
        self.facade = OrderProcessorFacade()
        self.order_info = {}
        self.pizza_ingredients = []
        self.drag_data = {"item": None, "offset_x": 0, "offset_y": 0}
        self.selected_pizza = tk.StringVar(value=MENU[0][0])
        self.init_frames()
        self.show_frame("order")

    def init_frames(self):
        self.frames = {}
        self.frames["order"] = self.create_order_frame()
        self.frames["kitchen"] = self.create_kitchen_frame()
        self.frames["packaging"] = self.create_packaging_frame()

    def show_frame(self, name):
        for f in self.frames.values():
            f.pack_forget()
        self.frames[name].pack(fill="both", expand=True)

    def create_order_frame(self):
        frame = tk.Frame(self, bg="#191c1f")

        # Header
        header = tk.Frame(frame, bg="#23272e")
        header.pack(fill="x")
        tk.Label(header, text="🍕 Bem-vindo à Pizzaria!", bg="#23272e", fg="#ffb347",
                 font=("Segoe UI", 24, "bold")).pack(pady=18)

        # Main content
        content = tk.Frame(frame, bg="#191c1f")
        content.pack(fill="both", expand=True, padx=0, pady=0)

        # Menu (left)
        menu_frame = tk.Frame(content, bg="#23272e", width=260, bd=0, relief="flat")
        menu_frame.pack(side="left", fill="y", padx=(0, 0), pady=0)
        tk.Label(menu_frame, text="Cardápio de Pizzas", bg="#23272e", fg="#ffb347",
                 font=("Segoe UI", 16, "bold")).pack(pady=(18, 8))

        # Clean pizza menu with hover effect
        self.menu_buttons = []
        for idx, (pizza, ingredientes) in enumerate(MENU):
            btn = tk.Button(
                menu_frame,
                text=f"🍕 {pizza}",
                bg="#23272e",
                fg="#f5f6fa",
                font=("Segoe UI", 13, "bold"),
                bd=0,
                relief="flat",
                anchor="w",
                activebackground="#ffb347",
                activeforeground="#23272e",
                cursor="hand2",
                command=lambda i=idx: self.select_pizza_from_menu(i)
            )
            btn.pack(fill="x", padx=18, pady=4)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#ffb347", fg="#23272e"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#23272e", fg="#f5f6fa"))
            self.menu_buttons.append(btn)

        self.ingredient_label = tk.Label(menu_frame, text="", bg="#23272e", fg="#b2bec3",
                                         font=("Segoe UI", 11), wraplength=220, justify="left")
        self.ingredient_label.pack(padx=18, pady=(10, 0), fill="x")

        self.select_pizza_from_menu(0)

        # Form (right)
        form_frame = tk.Frame(content, bg="#23272e", bd=0, relief="flat")
        form_frame.pack(side="left", fill="both", expand=True, padx=0, pady=0)

        # Nome
        tk.Label(form_frame, text="Dados do Cliente", bg="#23272e", fg="#ffb347",
                 font=("Segoe UI", 18, "bold")).pack(pady=(20, 2))
        self.entry_name = ttk.Entry(form_frame, width=38, font=("Segoe UI", 12))
        self.entry_name.pack(pady=8)
        self.entry_name.insert(0, "Nome do Cliente")
        self.entry_name.bind("<FocusIn>", lambda e: self.clear_placeholder(self.entry_name, "Nome do Cliente"))

        # Endereço
        self.entry_address = ttk.Entry(form_frame, width=38, font=("Segoe UI", 12))
        self.entry_address.pack(pady=8)
        self.entry_address.insert(0, "Endereço de Entrega")
        self.entry_address.bind("<FocusIn>", lambda e: self.clear_placeholder(self.entry_address, "Endereço de Entrega"))

        # Pizza - clean radio buttons
        pizza_box = tk.LabelFrame(form_frame, text="Escolha a pizza", bg="#23272e", fg="#ffb347",
                                 font=("Segoe UI", 13, "bold"), bd=2, relief="groove", labelanchor="n")
        pizza_box.pack(fill="x", pady=(18, 5), padx=10)
        for pizza, _ in MENU:
            rb = ttk.Radiobutton(pizza_box, text=pizza, variable=self.selected_pizza, value=pizza,
                                 style="Pizza.TRadiobutton", command=self.sync_menu_selection)
            rb.pack(anchor="w", padx=18, pady=2)

        # Pagamento
        pay_box = tk.LabelFrame(form_frame, text="Forma de Pagamento", bg="#23272e", fg="#ffb347",
                               font=("Segoe UI", 13, "bold"), bd=2, relief="groove", labelanchor="n")
        pay_box.pack(fill="x", pady=(18, 5), padx=10)
        self.payment = tk.StringVar(value="Cartão")
        ttk.Combobox(pay_box, textvariable=self.payment, values=["Cartão", "Pix", "Dinheiro"],
                     width=35, state="readonly", font=("Segoe UI", 12)).pack(pady=5, padx=10)

        # Embalagem presente
        self.gift_wrap = tk.BooleanVar()
        gift_frame = tk.Frame(form_frame, bg="#23272e")
        gift_frame.pack(pady=10)
        ttk.Checkbutton(gift_frame, text="Embalagem para presente 🎁", variable=self.gift_wrap).pack()

        # Botão
        btn = tk.Button(form_frame, text="Fazer Pedido", bg="#ffb347", fg="#23272e",
                        font=("Segoe UI", 15, "bold"), bd=0, relief="flat", activebackground="#ffd580",
                        command=self.go_to_kitchen, cursor="hand2")
        btn.pack(pady=30, ipadx=18, ipady=8)

        # Footer
        footer = tk.Frame(frame, bg="#23272e")
        footer.pack(fill="x", side="bottom")
        tk.Label(footer, text="© 2025 Pizzaria. Todos os direitos reservados.",
                 bg="#23272e", fg="#888", font=("Segoe UI", 10)).pack(pady=6)

        # Custom style for clean radio
        style = ttk.Style()
        style.configure("Pizza.TRadiobutton", background="#23272e", foreground="#f5f6fa", font=("Segoe UI", 12), indicatorcolor="#ffb347")
        style.map("Pizza.TRadiobutton",
                  background=[("active", "#23272e")],
                  foreground=[("active", "#ffb347")])

        return frame

    def select_pizza_from_menu(self, idx):
        pizza, ingredientes = MENU[idx]
        self.selected_pizza.set(pizza)
        self.ingredient_label.config(
            text="Ingredientes: " + ", ".join(ingredientes)
        )
        # Destaca botão selecionado
        for i, btn in enumerate(self.menu_buttons):
            if i == idx:
                btn.config(bg="#ffb347", fg="#23272e")
            else:
                btn.config(bg="#23272e", fg="#f5f6fa")

    def sync_menu_selection(self):
        pizza = self.selected_pizza.get()
        for idx, (name, _) in enumerate(MENU):
            if name == pizza:
                self.select_pizza_from_menu(idx)
                break

    def clear_placeholder(self, entry, text):
        if entry.get() == text:
            entry.delete(0, tk.END)

    def create_kitchen_frame(self):
        frame = tk.Frame(self, bg="#181a1b")
        # Cardápio lateral para consulta
        side_menu = tk.Frame(frame, bg="#23272e", width=220)
        side_menu.pack(side="left", fill="y", padx=(0, 0), pady=0)
        tk.Label(side_menu, text="Cardápio", bg="#23272e", fg="#ffb347",
                 font=("Segoe UI", 15, "bold")).pack(pady=(18, 8))
        for pizza, ingredientes in MENU:
            lbl = tk.Label(side_menu, text=f"{pizza}\n" + ", ".join(ingredientes),
                           bg="#23272e", fg="#f5f6fa", font=("Segoe UI", 11), anchor="w", justify="left", wraplength=180)
            lbl.pack(fill="x", padx=14, pady=5)

        # Área de montagem da pizza
        pizza_area = tk.Frame(frame, bg="#181a1b")
        pizza_area.pack(side="left", padx=40, pady=20)
        self.pizza_canvas = Canvas(pizza_area, width=350, height=350, bg="#f5e6ca", highlightthickness=2, highlightbackground="#ffb347")
        self.pizza_canvas.pack()
        self.draw_base_pizza()
        self.pizza_ingredients = []

        # Ingredientes para arrastar
        ing_frame = tk.Frame(frame, bg="#23272e")
        ing_frame.pack(side="left", fill="y", padx=30)
        tk.Label(ing_frame, text="Arraste os ingredientes:", bg="#23272e", fg="#ffb347", font=("Segoe UI", 13, "bold")).pack(pady=10)
        for name, color in INGREDIENTS:
            lbl = tk.Label(ing_frame, text=name, bg=color, fg="#23272e", font=("Segoe UI", 12, "bold"), width=15, relief="raised")
            lbl.pack(pady=8)
            lbl.bind("<ButtonPress-1>", lambda e, n=name, c=color: self.add_ingredient(n, c))
        tk.Button(frame, text="Escolher Embalagem", bg="#ffb347", fg="#23272e", font=("Segoe UI", 13, "bold"),
                  command=self.go_to_packaging).pack(side="bottom", pady=30)
        # Info do pedido
        self.info_label = tk.Label(frame, text="", bg="#23272e", fg="#ffb347", font=("Segoe UI", 15, "bold"), anchor="w", justify="left")
        self.info_label.pack(fill="x", padx=30, pady=20)
        return frame

    def create_packaging_frame(self):
        frame = tk.Frame(self, bg="#181a1b")
        tk.Label(frame, text="Escolha a Embalagem", bg="#181a1b", fg="#ffb347", font=("Segoe UI", 18, "bold")).pack(pady=20)
        self.packaging_canvas = Canvas(frame, width=800, height=400, bg="#23272e", highlightthickness=0)
        self.packaging_canvas.pack(pady=20)
        # Packaging areas
        self.packaging_canvas.create_rectangle(100, 100, 300, 300, fill="#ffe066", outline="#e1b12c", width=4)
        self.packaging_canvas.create_text(200, 320, text="Normal", fill="#f5f6fa", font=("Segoe UI", 14, "bold"))
        self.packaging_canvas.create_rectangle(500, 100, 700, 300, fill="#ffe066", outline="#ff69b4", width=4)
        self.packaging_canvas.create_text(600, 320, text="Presente", fill="#ff69b4", font=("Segoe UI", 14, "bold"))
        # Pizza to drag
        self.pizza_drag = self.packaging_canvas.create_oval(350, 180, 450, 280, fill="#ffe066", outline="#e1b12c", width=8)
        self.packaging_canvas.tag_bind(self.pizza_drag, "<B1-Motion>", self.move_pizza_drag)
        self.packaging_canvas.tag_bind(self.pizza_drag, "<ButtonRelease-1>", self.check_packaging)
        self.selected_packaging = None
        return frame

    def draw_base_pizza(self):
        self.pizza_canvas.delete("all")
        # Massa
        self.pizza_canvas.create_oval(25, 25, 325, 325, fill="#ffe066", outline="#e1b12c", width=8)
        # Molho (sempre presente)
        self.pizza_canvas.create_oval(50, 50, 300, 300, fill="#e74c3c", outline="", width=0, tags="molho")
        # Queijo (sempre presente, como linhas)
        for i in range(20):
            x1 = 60 + (i * 10) % 200
            y1 = 60 + ((i * 23) % 200)
            x2 = x1 + 40
            y2 = y1 + 10
            self.pizza_canvas.create_line(x1, y1, x2, y2, fill="#fffbe6", width=3, tags="queijo")

    def go_to_kitchen(self):
        name = self.entry_name.get().strip()
        address = self.entry_address.get().strip()
        pizza = self.selected_pizza.get()
        payment = self.payment.get()
        gift_wrap = self.gift_wrap.get()
        if not name or not address or name == "Nome do Cliente" or address == "Endereço de Entrega":
            messagebox.showwarning("Atenção", "Preencha todos os campos corretamente!")
            return
        self.order_info = {
            "name": name,
            "address": address,
            "pizza": pizza,
            "payment": payment,
            "gift_wrap": gift_wrap
        }
        info = f"Cliente: {name}\nEndereço: {address}\nPizza: {pizza}\nPagamento: {payment}\nEmbalagem presente: {'Sim' if gift_wrap else 'Não'}"
        # Atualiza info_label na tela de montagem
        if hasattr(self, "info_label"):
            self.info_label.config(text=info)
        self.pizza_ingredients.clear()
        self.draw_base_pizza()
        self.show_frame("kitchen")

    def add_ingredient(self, name, color):
        # Adiciona ingrediente visualmente realista e permite arrastar/remover
        items = []
        if name == "Calabresa":
            for i in range(5):
                x = 120 + (i * 25) % 100
                y = 120 + ((i * 17) % 100)
                circ = self.pizza_canvas.create_oval(x, y, x+30, y+30, fill=color, outline="#a71d31", width=2)
                self.setup_drag_and_remove(circ, name)
                items.append(circ)
        elif name == "Tomate":
            for i in range(3):
                x = 150 + (i * 30) % 80
                y = 160 + ((i * 27) % 80)
                circ = self.pizza_canvas.create_oval(x, y, x+25, y+25, fill=color, outline="#c0392b", width=2)
                self.setup_drag_and_remove(circ, name)
                items.append(circ)
        elif name == "Azeitona":
            for i in range(6):
                x = 110 + (i * 30) % 120
                y = 110 + ((i * 19) % 120)
                circ = self.pizza_canvas.create_oval(x, y, x+12, y+12, fill=color, outline="#23272e", width=1)
                self.setup_drag_and_remove(circ, name)
                items.append(circ)
        elif name == "Cebola":
            for i in range(4):
                x = 130 + (i * 20) % 80
                y = 130 + ((i * 15) % 80)
                arc = self.pizza_canvas.create_arc(x, y, x+40, y+40, start=30, extent=120, style=tk.ARC, outline=color, width=3)
                self.setup_drag_and_remove(arc, name)
                items.append(arc)
        elif name == "Manjericão":
            for i in range(3):
                x = 170 + (i * 30) % 60
                y = 120 + ((i * 23) % 60)
                leaf = self.pizza_canvas.create_polygon(
                    x, y, x+10, y+20, x-10, y+20, fill=color, outline="#145a32", width=2
                )
                self.setup_drag_and_remove(leaf, name)
                items.append(leaf)
        elif name == "Frango":
            for i in range(4):
                x = 140 + (i * 25) % 80
                y = 180 + ((i * 17) % 80)
                rect = self.pizza_canvas.create_rectangle(x, y, x+18, y+10, fill=color, outline="#b9770e", width=1)
                self.setup_drag_and_remove(rect, name)
                items.append(rect)
        elif name == "Catupiry":
            for i in range(4):
                x = 160 + (i * 18) % 70
                y = 140 + ((i * 21) % 70)
                circ = self.pizza_canvas.create_oval(x, y, x+18, y+18, fill=color, outline="#e1e1e1", width=1)
                self.setup_drag_and_remove(circ, name)
                items.append(circ)
        elif name == "Pimentão":
            for i in range(3):
                x1 = 120 + (i * 30) % 80
                y1 = 200 + ((i * 17) % 80)
                x2 = x1 + 40
                y2 = y1 + 5
                line = self.pizza_canvas.create_line(x1, y1, x2, y2, fill=color, width=5)
                self.setup_drag_and_remove(line, name)
                items.append(line)
        if items:
            self.pizza_ingredients.append((name, items))

    def setup_drag_and_remove(self, item, name):
        # Arrastar
        self.pizza_canvas.tag_bind(item, "<ButtonPress-1>", lambda e, i=item: self.start_drag_ingredient(e, i))
        self.pizza_canvas.tag_bind(item, "<B1-Motion>", lambda e, i=item: self.drag_ingredient(e, i))
        # Remover com duplo clique
        self.pizza_canvas.tag_bind(item, "<Double-Button-1>", lambda e, i=item, n=name: self.remove_ingredient(i, n))

    def start_drag_ingredient(self, event, item):
        self.drag_data["item"] = item
        self.drag_data["offset_x"] = event.x - self.pizza_canvas.coords(item)[0]
        self.drag_data["offset_y"] = event.y - self.pizza_canvas.coords(item)[1]

    def drag_ingredient(self, event, item):
        coords = self.pizza_canvas.coords(item)
        w = coords[2] - coords[0] if len(coords) == 4 else 0
        h = coords[3] - coords[1] if len(coords) == 4 else 0
        if len(coords) == 4:
            self.pizza_canvas.coords(item, event.x, event.y, event.x + w, event.y + h)
        elif len(coords) == 6:  # polygon
            dx = event.x - coords[0]
            dy = event.y - coords[1]
            new_coords = []
            for i in range(0, len(coords), 2):
                new_coords.append(coords[i] + dx)
                new_coords.append(coords[i+1] + dy)
            self.pizza_canvas.coords(item, *new_coords)
        # Para linhas/arcos, lógica similar pode ser adicionada se necessário

    def remove_ingredient(self, item, name):
        self.pizza_canvas.delete(item)
        # Remove do pizza_ingredients
        for ing in self.pizza_ingredients:
            if ing[0] == name and item in ing[1]:
                ing[1].remove(item)
        # Remove entradas vazias
        self.pizza_ingredients = [ing for ing in self.pizza_ingredients if ing[1]]

    def go_to_packaging(self):
        self.show_frame("packaging")

    def move_pizza_drag(self, event):
        x, y = event.x, event.y
        self.packaging_canvas.coords(self.pizza_drag, x-50, y-50, x+50, y+50)

    def check_packaging(self, event):
        x, y = event.x, event.y
        # Normal: dentro do retângulo 100,100,300,300
        # Presente: dentro do retângulo 500,100,700,300
        if 100 < x < 300 and 100 < y < 300:
            self.selected_packaging = "normal"
            self.finish_order()
        elif 500 < x < 700 and 100 < y < 300:
            self.selected_packaging = "gift"
            self.finish_order()
        else:
            messagebox.showinfo("Atenção", "Arraste a pizza para uma das embalagens!")

    def finish_order(self):
        # Sempre inclui molho e queijo
        ingredientes = ["Molho", "Queijo"]
        for n, items in self.pizza_ingredients:
            if n not in ingredientes:
                ingredientes.append(n)
        info = self.order_info
        gift_wrap = info.get("gift_wrap") or self.selected_packaging == "gift"
        order = self.facade.criar_e_processar_pedido(
            customer=info["name"],
            items=[info["pizza"]],
            address=info["address"],
            payment=info["payment"],
            gift_wrap=gift_wrap
        )
        msg = (
            f"🎉 Pedido Finalizado! 🎉\n\n"
            f"Cliente: {info['name']}\n"
            f"Endereço: {info['address']}\n"
            f"Pizza: {info['pizza']}\n"
            f"Pagamento: {info['payment']}\n"
            f"Ingredientes: {', '.join(ingredientes)}\n"
            f"Embalagem: {'Presente 🎁' if gift_wrap else 'Normal'}\n\n"
            f"Resumo do pedido:\n{order}\n\n"
            f"Obrigado por pedir conosco! 🍕"
        )
        messagebox.showinfo("Resumo do Pedido", msg)
        self.destroy()

if __name__ == "__main__":
    app = PizzaApp()
    app.mainloop()