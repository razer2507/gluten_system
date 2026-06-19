#models 

# logic/models.py

class Cliente:
    def __init__(self, nombre, referencia=None, id=None):
        self.id = id                  # El ID inicia en None porque SQLite lo genera solo al guardar
        self.nombre = nombre          # TEXT NOT NULL
        self.referencia = referencia  # TEXT (Instagram, vecino, etc.)

    def a_tupla(self):
        """Utilitario para empaquetar los datos al usar INSERT en SQL"""
        return (self.nombre, self.referencia)
    def a_objeto(self,data:tuple):
        return Cliente(data[0],data[1])


class Producto:
    def __init__(self, nombre,precio_costo, categoria=None, id=None):
        self.id = id
        self.nombre = nombre          # TEXT NOT NULL
        self.precio_costo = precio_costo  # REAL NOT NULL
        self.categoria = categoria    # TEXT

    def a_tupla(self):
        """Utilitario para empaquetar los datos al usar INSERT en SQL"""
        return (self.nombre,self.precio_costo, self.categoria)

class Venta:
    def __init__(self,fecha,cliente_id,total,estado,id=None):
        self.fecha = fecha
        self.cliente_id = cliente_id
        self.total = total
        self.estado = estado
        self.id = id

    def a_tupla(self):
        """Utilitario para empaquetar los datos al usar INSERT en SQL"""
        return(self.fecha,self.cliente_id,self.total,self.estado) 

class DetalleVentas:
    def __init__(self,venta_id,producto_id,cantidad,precio_unitario,id=None):
        self.id = id
        self.venta_id = venta_id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
    
    def a_tupla(self):
        return(self.venta_id,self.producto_id,self.cantidad,self.precio_unitario)

class Gastos:
    def __init__(self,fecha,categoria,monto,descripcion,tipo,id=None):
        self.id = id
        self.fecha = fecha
        self.categoria = categoria
        self.monto = monto
        self.descripcion = descripcion
        self.tipo = tipo
    
    def a_tupla(self):
        return(self.fecha,self.categoria,self.monto,self.descripcion,self.tipo)
        