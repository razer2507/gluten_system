from data.data import db
from logic.models import Cliente,Producto,Venta,DetalleVentas,Gastos
class Logica:
    def __init__(self,bd:db):
        self.bd = bd
    


    def insertar_cliente(self,cliente:Cliente):
        if len(cliente.nombre)==0:
            return False
        if cliente.nombre.isdigit():
            return False
        self.bd.insertar_cliente(cliente.a_tupla())
        return True
    
    def eliminar_cliente(self,cliente:Cliente):
        busqueda_cliente = self.bd.buscar_clientes(cliente.id)
        if not busqueda_cliente:
            return False
        self.bd.eliminar_cliente(cliente.id)
        return True



