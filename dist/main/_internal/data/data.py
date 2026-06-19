import sqlite3

class db():
    def __init__(self,directorio='gluten.db'):
        self.conn = sqlite3.connect(directorio)
        self.cursor = self.conn.cursor()
        self.iniciar_db()

    def iniciar_db(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            referencia TEXT)''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio_venta REAL NOT NULL,
        precio_costo REAL NOT NULL,
        categoria TEXT
        );
        ''')
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS ventas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TIMESTAMP,
        cliente_id INTEGER,
        total REAL NOT NULL,
        estado TEXT NOT NULL,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        );
        ''')
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS detalle_ventas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        venta_id INTEGER NOT NULL,
        producto_id INTEGER NOT NULL,
        cantidad INTEGER NOT NULL,
        precio_unitario REAL NOT NULL,
        FOREIGN KEY (venta_id) REFERENCES ventas(id),
        FOREIGN KEY (producto_id) REFERENCES productos(id)
        );
        ''')
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS gastos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TIMESTAMP,
        categoria TEXT NOT NULL,
        monto REAL NOT NULL,
        descripcion TEXT,
        tipo TEXT
        );
        ''')
     
        self.guardar_cambios()
    
    def guardar_cambios(self):
        self.conn.commit()

    def cerrar_conexion(self):
        self.conn.close()

    # --- CRUD PRODUCTOS ---
    def insertar_producto(self, data: tuple):
        self.cursor.execute('''
        INSERT INTO productos(nombre,precio_venta,precio_costo,categoria) VALUES(?,?,?,?)
        ''', data)
        self.guardar_cambios()

    def obtener_productos(self):
        self.cursor.execute('SELECT * FROM productos')
        return self.cursor.fetchall()

    def eliminar_producto(self, producto_id: int):
        self.cursor.execute('DELETE FROM productos WHERE id = ?', (producto_id,))
        self.guardar_cambios()

    def actualizar_producto(self, producto_id: int, data: tuple):
        self.cursor.execute('''
        UPDATE productos SET nombre = ?, precio_venta = ?, precio_costo = ?, categoria = ? WHERE id = ?
        ''', (data[0], data[1], data[2], data[3], producto_id))
        self.guardar_cambios()

    # --- CRUD CLIENTES ---
    def insertar_cliente(self, data: tuple):
        self.cursor.execute('''
        INSERT INTO clientes(nombre, referencia) VALUES (?, ?)
        ''', data)
        self.guardar_cambios()

    def obtener_clientes(self):
        self.cursor.execute('SELECT * FROM clientes')
        return self.cursor.fetchall()
    
    def buscar_clientes(self,id):
        self.cursor.execute('''SELECT *FROM clientes WHERE id=?''',(id,))
        return self.cursor.fetchone()

    def eliminar_cliente(self, cliente_id: int):
        self.cursor.execute('DELETE FROM clientes WHERE id = ?', (cliente_id,))
        self.guardar_cambios()

    def actualizar_cliente(self, cliente_id: int, data: tuple):
        self.cursor.execute('''
        UPDATE clientes SET nombre = ?, referencia = ? WHERE id = ?
        ''', (data[0], data[1], cliente_id))
        self.guardar_cambios()

    # --- CRUD VENTAS ---
    def insertar_venta(self, data: tuple):
        self.cursor.execute('''
        INSERT INTO ventas(fecha, cliente_id, total, estado) VALUES (?, ?, ?, ?)
        ''', data)
        self.guardar_cambios()
        return self.cursor.lastrowid

    def obtener_ventas(self):
        self.cursor.execute('SELECT * FROM ventas')
        return self.cursor.fetchall()

    def eliminar_venta(self, venta_id: int):
        self.cursor.execute('DELETE FROM ventas WHERE id = ?', (venta_id,))
        self.guardar_cambios()

    def actualizar_venta(self, venta_id: int, data: tuple):
        self.cursor.execute('''
        UPDATE ventas SET fecha = ?, cliente_id = ?, total = ?, estado = ? WHERE id = ?
        ''', (data[0], data[1], data[2], data[3], venta_id))
        self.guardar_cambios()

    # --- CRUD DETALLE_VENTAS ---
    def insertar_detalle_venta(self, data: tuple):
        self.cursor.execute('''
        INSERT INTO detalle_ventas(venta_id, producto_id, cantidad, precio_unitario) VALUES (?, ?, ?, ?)
        ''', data)
        self.guardar_cambios()

    def obtener_detalles_venta(self, venta_id: int):
        self.cursor.execute('SELECT * FROM detalle_ventas WHERE venta_id = ?', (venta_id,))
        return self.cursor.fetchall()

    def eliminar_detalle_venta(self, detalle_id: int):
        self.cursor.execute('DELETE FROM detalle_ventas WHERE id = ?', (detalle_id,))
        self.guardar_cambios()

    # --- CRUD GASTOS ---
    def insertar_gasto(self, data: tuple):
        self.cursor.execute('''
        INSERT INTO gastos(fecha, categoria, monto, descripcion) VALUES (?, ?, ?, ?)
        ''', data)
        self.guardar_cambios()

    def obtener_gastos(self):
        self.cursor.execute('SELECT * FROM gastos')
        return self.cursor.fetchall()

    def eliminar_gasto(self, gasto_id: int):
        self.cursor.execute('DELETE FROM gastos WHERE id = ?', (gasto_id,))
        self.guardar_cambios()

    def actualizar_gasto(self, gasto_id: int, data: tuple):
        self.cursor.execute('''
        UPDATE gastos SET fecha = ?, categoria = ?, monto = ?, descripcion = ? WHERE id = ?
        ''', (data[0], data[1], data[2], data[3], gasto_id))
        self.guardar_cambios()


database = db()