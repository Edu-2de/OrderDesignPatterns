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
        self.saved_pizza_snapshot = None
        self.slices_var = tk.IntVar(value=4)
        self.init_frames()
        self.show_frame("order")

    def init_frames(self):
        self.frames = {}
        self.frames["order"] = self.create_order_frame()
        self.frames["kitchen"] = self.create_kitchen_frame()
        self.frames["cutting"] = self.create_cutting_frame()
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

        tk.Label(form_frame, text="Dados do Cliente", bg="#23272e", fg="#ffb347",
                 font=("Segoe UI", 18, "bold")).pack(pady=(20, 2))
        self.entry_name = ttk.Entry(form_frame, width=38, font=("Segoe UI", 12))
        self.entry_name.pack(pady=8)
        self.entry_name.insert(0, "Nome do Cliente")
        self.entry_name.bind("<FocusIn>", lambda e: self.clear_placeholder(self.entry_name, "Nome do Cliente"))

        self.entry_address = ttk.Entry(form_frame, width=38, font=("Segoe UI", 12))
        self.entry_address.pack(pady=8)
        self.entry_address.insert(0, "Endereço de Entrega")
        self.entry_address.bind("<FocusIn>", lambda e: self.clear_placeholder(self.entry_address, "Endereço de Entrega"))

        pizza_box = tk.LabelFrame(form_frame, text="Escolha a pizza", bg="#23272e", fg="#ffb347",
                                 font=("Segoe UI", 13, "bold"), bd=2, relief="groove", labelanchor="n")
        pizza_box.pack(fill="x", pady=(18, 5), padx=10)
        for pizza, _ in MENU:
            rb = ttk.Radiobutton(pizza_box, text=pizza, variable=self.selected_pizza, value=pizza,
                                 style="Pizza.TRadiobutton", command=self.sync_menu_selection)
            rb.pack(anchor="w", padx=18, pady=2)

        pay_box = tk.LabelFrame(form_frame, text="Forma de Pagamento", bg="#23272e", fg="#ffb347",
                               font=("Segoe UI", 13, "bold"), bd=2, relief="groove", labelanchor="n")
        pay_box.pack(fill="x", pady=(18, 5), padx=10)
        self.payment = tk.StringVar(value="Cartão")
        ttk.Combobox(pay_box, textvariable=self.payment, values=["Cartão", "Pix", "Dinheiro"],
                     width=35, state="readonly", font=("Segoe UI", 12)).pack(pady=5, padx=10)

        self.gift_wrap = tk.BooleanVar()
        gift_frame = tk.Frame(form_frame, bg="#23272e")
        gift_frame.pack(pady=10)
        ttk.Checkbutton(gift_frame, text="Embalagem para presente 🎁", variable=self.gift_wrap).pack()

        btn = tk.Button(form_frame, text="Fazer Pedido", bg="#ffb347", fg="#23272e",
                        font=("Segoe UI", 15, "bold"), bd=0, relief="flat", activebackground="#ffd580",
                        command=self.go_to_kitchen, cursor="hand2")
        btn.pack(pady=30, ipadx=18, ipady=8)

        footer = tk.Frame(frame, bg="#23272e")
        footer.pack(fill="x", side="bottom")
        tk.Label(footer, text="© 2025 Pizzaria. Todos os direitos reservados.",
                 bg="#23272e", fg="#888", font=("Segoe UI", 10)).pack(pady=6)

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
        side_menu = tk.Frame(frame, bg="#23272e", width=220)
        side_menu.grid(row=0, column=0, sticky="ns", padx=(0, 0), pady=0)
        tk.Label(side_menu, text="Cardápio", bg="#23272e", fg="#ffb347",
                 font=("Segoe UI", 15, "bold")).pack(pady=(18, 8))
        for pizza, ingredientes in MENU:
            pizza_lbl = tk.Label(
                side_menu,
                text=pizza,
                bg="#23272e",
                fg="#ffb347",
                font=("Segoe UI", 12, "bold"),
                anchor="w",
                justify="left"
            )
            pizza_lbl.pack(fill="x", padx=14, pady=(8, 0))
            ing_lbl = tk.Label(
                side_menu,
                text="  " + ", ".join(ingredientes),
                bg="#23272e",
                fg="#f5f6fa",
                font=("Segoe UI", 10),
                anchor="w",
                justify="left",
                wraplength=180
            )
            ing_lbl.pack(fill="x", padx=18, pady=(0, 2))

        center_area = tk.Frame(frame, bg="#181a1b")
        center_area.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.info_label = tk.Label(center_area, text="", bg="#23272e", fg="#ffb347",
                                   font=("Segoe UI", 14, "bold"), anchor="w", justify="left")
        self.info_label.pack(fill="x", padx=0, pady=(10, 8))
        pizza_canvas_frame = tk.Frame(center_area, bg="#181a1b")
        pizza_canvas_frame.pack(expand=True)
        self.pizza_canvas = Canvas(
            pizza_canvas_frame, width=370, height=370,
            bg="#f5e6ca", highlightthickness=2, highlightbackground="#ffb347"
        )
        self.pizza_canvas.pack(padx=10, pady=10)
        self.draw_base_pizza()
        self.pizza_ingredients = []

        btn_frame = tk.Frame(center_area, bg="#181a1b")
        btn_frame.pack(fill="x", pady=(10, 20))
        tk.Button(
            btn_frame, text="Cortar Pizza", bg="#ffb347", fg="#23272e",
            font=("Segoe UI", 13, "bold"), command=self.go_to_cutting,
            bd=0, relief="flat", activebackground="#ffd580", cursor="hand2"
        ).pack(ipadx=18, ipady=8)

        ing_frame = tk.Frame(frame, bg="#23272e", width=220)
        ing_frame.grid(row=0, column=2, sticky="ns", padx=(0, 0), pady=0)
        tk.Label(ing_frame, text="Ingredientes", bg="#23272e", fg="#ffb347",
                 font=("Segoe UI", 14, "bold")).pack(pady=(18, 8))
        for name, color in INGREDIENTS:
            lbl = tk.Label(
                ing_frame, text=name, bg=color, fg="#23272e",
                font=("Segoe UI", 12, "bold"), width=15, relief="raised", bd=1, cursor="hand2"
            )
            lbl.pack(pady=8, padx=18)
            lbl.bind("<ButtonPress-1>", lambda e, n=name, c=color: self.add_ingredient(n, c))

        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        return frame

    def create_cutting_frame(self):
        frame = tk.Frame(self, bg="#181a1b")
        tk.Label(frame, text="Corte sua Pizza!", bg="#181a1b", fg="#ffb347", font=("Segoe UI", 18, "bold")).pack(pady=20)
        self.cutting_canvas = Canvas(frame, width=370, height=370, bg="#f5e6ca", highlightthickness=2, highlightbackground="#ffb347")
        self.cutting_canvas.pack(pady=10)
        cut_frame = tk.Frame(frame, bg="#181a1b")
        cut_frame.pack(pady=10)
        tk.Label(cut_frame, text="Escolha em quantos pedaços cortar:", bg="#181a1b", fg="#ffb347", font=("Segoe UI", 13)).pack()
        for n in [2, 4, 6, 8]:
            ttk.Radiobutton(cut_frame, text=f"{n} pedaços", variable=self.slices_var, value=n).pack(side="left", padx=10)
        tk.Button(frame, text="Cortar e Embalar", bg="#ffb347", fg="#23272e", font=("Segoe UI", 13, "bold"),
                  command=self.go_to_packaging, bd=0, relief="flat", activebackground="#ffd580", cursor="hand2").pack(pady=20)
        return frame

    def create_packaging_frame(self):
        frame = tk.Frame(self, bg="#181a1b")
        tk.Label(frame, text="Escolha a Embalagem", bg="#181a1b", fg="#ffb347", font=("Segoe UI", 18, "bold")).pack(pady=20)
        self.packaging_canvas = Canvas(frame, width=800, height=400, bg="#23272e", highlightthickness=0)
        self.packaging_canvas.pack(pady=20)
        self.packaging_canvas.create_rectangle(100, 100, 300, 300, fill="#ffe066", outline="#e1b12c", width=4, tags="normal_box")
        self.packaging_canvas.create_text(200, 320, text="Normal", fill="#f5f6fa", font=("Segoe UI", 14, "bold"))
        self.packaging_canvas.create_rectangle(500, 100, 700, 300, fill="#ffe066", outline="#ff69b4", width=4, tags="gift_box")
        self.packaging_canvas.create_text(600, 320, text="Presente", fill="#ff69b4", font=("Segoe UI", 14, "bold"))
        # Pizza desenhada no centro
        self.pizza_img_group = []
        self.pizza_drag = self.packaging_canvas.create_oval(350, 180, 450, 280, fill="#ffe066", outline="#e1b12c", width=8, tags="pizza_drag")
        self.packaging_canvas.tag_bind("pizza_drag", "<B1-Motion>", self.move_pizza_drag)
        self.packaging_canvas.tag_bind("pizza_drag", "<ButtonRelease-1>", self.check_packaging)
        self.selected_packaging = None
        return frame

    def draw_base_pizza(self, canvas=None):
        if canvas is None:
            canvas = self.pizza_canvas
        canvas.delete("all")
        canvas.create_oval(25, 25, 325, 325, fill="#ffe066", outline="#e1b12c", width=8)
        canvas.create_oval(50, 50, 300, 300, fill="#e74c3c", outline="", width=0, tags="molho")
        for i in range(20):
            x1 = 60 + (i * 10) % 200
            y1 = 60 + ((i * 23) % 200)
            x2 = x1 + 40
            y2 = y1 + 10
            canvas.create_line(x1, y1, x2, y2, fill="#fffbe6", width=3, tags="queijo")

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
        if hasattr(self, "info_label"):
            self.info_label.config(text=info)
        self.pizza_ingredients.clear()
        self.draw_base_pizza()
        self.show_frame("kitchen")

    def add_ingredient(self, name, color):
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
        self.pizza_canvas.tag_bind(item, "<ButtonPress-1>", lambda e, i=item: self.start_drag_ingredient(e, i))
        self.pizza_canvas.tag_bind(item, "<B1-Motion>", lambda e, i=item: self.drag_ingredient(e, i))
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

    def remove_ingredient(self, item, name):
        self.pizza_canvas.delete(item)
        for ing in self.pizza_ingredients:
            if ing[0] == name and item in ing[1]:
                ing[1].remove(item)
        self.pizza_ingredients = [ing for ing in self.pizza_ingredients if ing[1]]

    def go_to_cutting(self):
        # Salva a pizza montada (snapshot dos itens do canvas)
        self.saved_pizza_snapshot = []
        for item in self.pizza_canvas.find_all():
            item_type = self.pizza_canvas.type(item)
            coords = self.pizza_canvas.coords(item)
            opts = self.pizza_canvas.itemconfig(item)
            self.saved_pizza_snapshot.append((item_type, coords, opts))
        self.show_frame("cutting")
        self.render_saved_pizza_on_cutting()

    def render_saved_pizza_on_cutting(self):
        self.draw_base_pizza(self.cutting_canvas)
        # Redesenha os ingredientes salvos
        if not self.saved_pizza_snapshot:
            return
        for item_type, coords, opts in self.saved_pizza_snapshot:
            if item_type == "oval":
                self.cutting_canvas.create_oval(*coords, fill=opts["fill"][-1], outline=opts["outline"][-1], width=int(opts["width"][-1]))
            elif item_type == "arc":
                self.cutting_canvas.create_arc(*coords, start=int(opts["start"][-1]), extent=int(opts["extent"][-1]),
                                               style=opts["style"][-1], outline=opts["outline"][-1], width=int(opts["width"][-1]))
            elif item_type == "polygon":
                self.cutting_canvas.create_polygon(*coords, fill=opts["fill"][-1], outline=opts["outline"][-1], width=int(opts["width"][-1]))
            elif item_type == "line":
                self.cutting_canvas.create_line(*coords, fill=opts["fill"][-1], width=int(opts["width"][-1]))
        self.draw_cuts_on_cutting_canvas()
        self.slices_var.trace_add("write", lambda *args: self.draw_cuts_on_cutting_canvas())

    def draw_cuts_on_cutting_canvas(self):
        self.cutting_canvas.delete("cuts")
        slices = self.slices_var.get() if hasattr(self, "slices_var") else 4
        cx, cy, r = 175, 175, 150
        import math
        for i in range(slices):
            angle = (360 / slices) * i
            x = cx + r * math.cos(math.radians(angle))
            y = cy + r * math.sin(math.radians(angle))
            # Traço preto para indicar corte
            self.cutting_canvas.create_line(cx, cy, x, y, fill="black", width=4, tags="cuts")

    def go_to_packaging(self):
        self.show_frame("packaging")
        self.packaging_canvas.delete("pizza_img")
        # Centraliza a pizza na caixa de embalagem
        pizza_offset_x = 200 - 175  # centro da caixa - centro da pizza
        pizza_offset_y = 200 - 175

        # Desenha miniatura da pizza feita pelo usuário (em vez de pizza vazia)
        self.mini_pizza_items = []
        # Base da pizza
        base = self.packaging_canvas.create_oval(
            25 + pizza_offset_x, 25 + pizza_offset_y, 325 + pizza_offset_x, 325 + pizza_offset_y,
            fill="#ffe066", outline="#e1b12c", width=8, tags="pizza_img"
        )
        molho = self.packaging_canvas.create_oval(
            50 + pizza_offset_x, 50 + pizza_offset_y, 300 + pizza_offset_x, 300 + pizza_offset_y,
            fill="#e74c3c", outline="", width=0, tags="pizza_img"
        )
        self.mini_pizza_items.extend([base, molho])
        for i in range(20):
            x1 = 60 + (i * 10) % 200 + pizza_offset_x
            y1 = 60 + ((i * 23) % 200) + pizza_offset_y
            x2 = x1 + 40
            y2 = y1 + 10
            queijo = self.packaging_canvas.create_line(
                x1, y1, x2, y2, fill="#fffbe6", width=3, tags="pizza_img"
            )
            self.mini_pizza_items.append(queijo)

        # Redesenha ingredientes da pizza feita pelo usuário
        if self.saved_pizza_snapshot:
            for item_type, coords, opts in self.saved_pizza_snapshot:
                adj_coords = []
                for idx, val in enumerate(coords):
                    if idx % 2 == 0:
                        adj_coords.append(val + pizza_offset_x)
                    else:
                        adj_coords.append(val + pizza_offset_y)
                if item_type == "oval":
                    item = self.packaging_canvas.create_oval(
                        *adj_coords, fill=opts["fill"][-1], outline=opts["outline"][-1],
                        width=int(opts["width"][-1]), tags="pizza_img"
                    )
                elif item_type == "arc":
                    item = self.packaging_canvas.create_arc(
                        *adj_coords, start=int(opts["start"][-1]), extent=int(opts["extent"][-1]),
                        style=opts["style"][-1], outline=opts["outline"][-1],
                        width=int(opts["width"][-1]), tags="pizza_img"
                    )
                elif item_type == "polygon":
                    item = self.packaging_canvas.create_polygon(
                        *adj_coords, fill=opts["fill"][-1], outline=opts["outline"][-1],
                        width=int(opts["width"][-1]), tags="pizza_img"
                    )
                elif item_type == "line":
                    item = self.packaging_canvas.create_line(
                        *adj_coords, fill=opts["fill"][-1], width=int(opts["width"][-1]), tags="pizza_img"
                    )
                else:
                    continue
                self.mini_pizza_items.append(item)

        # Desenha cortes em preto
        slices = self.slices_var.get() if hasattr(self, "slices_var") else 4
        cx, cy, r = 200, 200, 150
        import math
        for i in range(slices):
            angle = (360 / slices) * i
            x = cx + r * math.cos(math.radians(angle))
            y = cy + r * math.sin(math.radians(angle))
            cut = self.packaging_canvas.create_line(cx, cy, x, y, fill="black", width=4, tags="pizza_img")
            self.mini_pizza_items.append(cut)

        # Cria a miniatura da pizza como um grupo arrastável
        # Calcula bounding box da pizza
        self.mini_pizza_bbox = [25 + pizza_offset_x, 25 + pizza_offset_y, 325 + pizza_offset_x, 325 + pizza_offset_y]
        # Cria um oval invisível para servir de "alça" de arrasto
        self.pizza_drag = self.packaging_canvas.create_oval(
            *self.mini_pizza_bbox, outline="", fill="", tags="pizza_drag"
        )
        self.packaging_canvas.tag_bind("pizza_drag", "<B1-Motion>", self.move_pizza_drag)
        self.packaging_canvas.tag_bind("pizza_drag", "<ButtonRelease-1>", self.check_packaging)
        self.packaging_canvas.tag_raise("pizza_drag")

    def move_pizza_drag(self, event):
        # Move todos os itens da miniatura da pizza junto com o oval invisível
        x, y = event.x, event.y
        # Calcula o centro atual da pizza
        bbox = self.packaging_canvas.coords(self.pizza_drag)
        cx = (bbox[0] + bbox[2]) / 2
        cy = (bbox[1] + bbox[3]) / 2
        dx = x - cx
        dy = y - cy
        # Move todos os itens da pizza_img e o oval invisível
        for item in self.packaging_canvas.find_withtag("pizza_img"):
            self.packaging_canvas.move(item, dx, dy)
        self.packaging_canvas.move(self.pizza_drag, dx, dy)

    def check_packaging(self, event):
        # Checa onde está o centro da pizza_drag
        coords = self.packaging_canvas.coords(self.pizza_drag)
        x = (coords[0] + coords[2]) / 2
        y = (coords[1] + coords[3]) / 2
        if 100 < x < 300 and 100 < y < 300:
            self.selected_packaging = "normal"
            self.finish_order()
        elif 500 < x < 700 and 100 < y < 300:
            self.selected_packaging = "gift"
            self.finish_order()
        else:
            messagebox.showinfo("Atenção", "Arraste a pizza para uma das embalagens!")

    def finish_order(self):
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
            gift_wrap=gift_wrap,
            notification_type="sms" if info["payment"] == "Pix" else "email"  # Exemplo de uso do strategy

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