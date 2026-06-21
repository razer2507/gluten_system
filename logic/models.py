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

    @classmethod
    def desde_tupla(cls,tupla):
        if not tupla:return None

        id_bd = tupla[0]
        nombre = tupla[1]
        referencia = tupla[2]

        return cls(
        id=id_bd,
        nombre=nombre,
        referencia=referencia
        )

class Producto:
    def __init__(self, nombre,precio_costo, categoria=None, id=None):
        self.id = id
        self.nombre = nombre          # TEXT NOT NULL
        self.precio_costo = precio_costo  # REAL NOT NULL
        self.categoria = categoria    # TEXT

    def a_tupla(self):
        """Utilitario para empaquetar los datos al usar INSERT en SQL"""
        return (self.nombre,self.precio_costo, self.categoria)
    @classmethod
    def desde_tupla(cls,tupla):
        if not tupla:return None

        id_bd = tupla[0]
        nombre = tupla[1]
        precio_costo = tupla[2]
        categoria = tupla[3]
        return cls(
            id=id_bd,
            nombre=nombre,
            precio_costo=precio_costo,
            categoria=categoria
            )
        

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

    @classmethod
    def desde_tupla(cls,tupla):
        if not tupla:return None
        return cls(
            id=tupla[0],
            fecha=tupla[1],
            cliente_id=tupla[2],
            total=tupla[3],
            estado=tupla[4],
        )
    def imprimir_venta(self):
        print(f"date{self.fecha}\ncliente_id:{self.cliente_id}\ntotal:{self.total}\nestado:{self.estado}\nid:{self.id}")

class DetalleVentas:
    def __init__(self,venta_id,producto_id,cantidad,precio_unitario,id=None):
        self.id = id
        self.venta_id = venta_id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
    
    def a_tupla(self):
        return(self.venta_id,self.producto_id,self.cantidad,self.precio_unitario)
    @classmethod
    def desde_tupla(cls,tupla):
        if not tupla:return None
        id_bd = tupla[0]
        venta_id = tupla[1]
        producto_id = tupla[2]
        cantidad = tupla[3]
        precio_unit = tupla[4]
        return cls(
            id=id_bd,
            venta_id=venta_id,
            producto_id=producto_id,
            cantidad=cantidad,
            precio_unitario=precio_unit
        )

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
    
    @classmethod
    def desde_tupla(cls,tupla):
        if not tupla:return None
        id_bd = tupla[0]
        fecha = tupla[1]
        categoria = tupla[2]
        monto = tupla[3]
        descripcion = tupla[4]
        tipo = tupla[5]

        return cls(
            id=id_bd,
            fecha=fecha,
            categoria=categoria,
            monto=monto,
            descripcion=descripcion,
            tipo=tipo
        )
        