import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askstring
import sys
import os

# Ajustar el path para importar el módulo db
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data')))
from data import db

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Gluten - Demo")
        self.db = db()

        tab_control = ttk.Notebook(root)
        self.tab_productos = ttk.Frame(tab_control)
        self.tab_clientes = ttk.Frame(tab_control)
        self.tab_ventas = ttk.Frame(tab_control)
        tab_control.add(self.tab_productos, text='Productos')
        tab_control.add(self.tab_clientes, text='Clientes')
        tab_control.add(self.tab_ventas, text='Ventas')
        tab_control.pack(expand=1, fill='both')

        self.setup_productos_tab()
        self.setup_clientes_tab()
        self.setup_ventas_tab()

    def setup_productos_tab(self):
        frame = self.tab_productos
        self.tree_productos = ttk.Treeview(frame, columns=('ID', 'Nombre', 'Venta', 'Costo', 'Categoria'), show='headings')
        for col in ('ID', 'Nombre', 'Venta', 'Costo', 'Categoria'):
            self.tree_productos.heading(col, text=col)
        self.tree_productos.pack(fill='both', expand=True)

        btn_add = ttk.Button(frame, text="Agregar Producto", command=self.agregar_producto)
        btn_add.pack(pady=5)

        self.cargar_productos()

    def cargar_productos(self):
        for row in self.tree_productos.get_children():
            self.tree_productos.delete(row)
        for prod in self.db.obtener_productos():
            self.tree_productos.insert('', 'end', values=prod)

    def agregar_producto(self):
        nombre = askstring("Nombre", "Nombre del producto:")
        if not nombre:
            return
        try:
            precio_venta = float(askstring("Precio Venta", "Precio de venta:"))
            precio_costo = float(askstring("Precio Costo", "Precio de costo:"))
        except (TypeError, ValueError):
            messagebox.showerror("Error", "Precios inválidos")
            return
        categoria = askstring("Categoría", "Categoría:")
        self.db.insertar_producto((nombre, precio_venta, precio_costo, categoria))
        self.cargar_productos()

    def setup_clientes_tab(self):
        frame = self.tab_clientes
        self.tree_clientes = ttk.Treeview(frame, columns=('ID', 'Nombre', 'Referencia'), show='headings')
        for col in ('ID', 'Nombre', 'Referencia'):
            self.tree_clientes.heading(col, text=col)
        self.tree_clientes.pack(fill='both', expand=True)

        btn_add = ttk.Button(frame, text="Agregar Cliente", command=self.agregar_cliente)
        btn_add.pack(pady=5)

        self.cargar_clientes()

    def cargar_clientes(self):
        for row in self.tree_clientes.get_children():
            self.tree_clientes.delete(row)
        for cli in self.db.obtener_clientes():
            self.tree_clientes.insert('', 'end', values=cli)

    def agregar_cliente(self):
        nombre = askstring("Nombre", "Nombre del cliente:")
        if not nombre:
            return
        referencia = askstring("Referencia", "Referencia:")
        self.db.insertar_cliente((nombre, referencia))
        self.cargar_clientes()

    def setup_ventas_tab(self):
        frame = self.tab_ventas
        self.tree_ventas = ttk.Treeview(frame, columns=('ID', 'Fecha', 'Cliente', 'Total', 'Estado'), show='headings')
        for col in ('ID', 'Fecha', 'Cliente', 'Total', 'Estado'):
            self.tree_ventas.heading(col, text=col)
        self.tree_ventas.pack(fill='both', expand=True)

        btn_add = ttk.Button(frame, text="Agregar Venta", command=self.agregar_venta)
        btn_add.pack(pady=5)

        self.cargar_ventas()

    def cargar_ventas(self):
        for row in self.tree_ventas.get_children():
            self.tree_ventas.delete(row)
        ventas = self.db.obtener_ventas()
        clientes = {c[0]: c[1] for c in self.db.obtener_clientes()}
        for venta in ventas:
            # venta: (id, fecha, cliente_id, total, estado)
            cliente_nombre = clientes.get(venta[2], "Sin cliente") if venta[2] is not None else "Sin cliente"
            self.tree_ventas.insert('', 'end', values=(venta[0], venta[1], cliente_nombre, venta[3], venta[4]))

    def agregar_venta(self):
        # Seleccionar cliente
        clientes = self.db.obtener_clientes()
        if not clientes:
            messagebox.showinfo("Sin clientes", "Debe agregar clientes antes de registrar ventas.")
            return
        cliente_nombres = [c[1] for c in clientes]
        cliente_id = None

        def seleccionar_cliente():
            nonlocal cliente_id
            idx = lb.curselection()
            if not idx:
                return
            cliente_id = clientes[idx[0]][0]
            top.destroy()

        top = tk.Toplevel(self.root)
        top.title("Seleccionar Cliente")
        tk.Label(top, text="Seleccione un cliente:").pack()
        lb = tk.Listbox(top)
        for nombre in cliente_nombres:
            lb.insert('end', nombre)
        lb.pack()
        btn_sel = tk.Button(top, text="Seleccionar", command=seleccionar_cliente)
        btn_sel.pack()
        top.grab_set()
        top.wait_window()

        if cliente_id is None:
            return

        total = askstring("Total", "Total de la venta:")
        if total is None:
            return
        try:
            total = float(total)
        except ValueError:
            messagebox.showerror("Error", "Total inválido")
            return

        estado = askstring("Estado", "Estado de la venta (ej: pagada, pendiente):")
        if not estado:
            estado = "pendiente"

        from datetime import datetime
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.db.insertar_venta((fecha, cliente_id, total, estado))
        self.cargar_ventas()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
