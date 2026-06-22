from data.data import db
from logic.models import Cliente,Producto,Venta,DetalleVentas,Gastos
from ml.IA import MachineLearing
from datetime import datetime
class Logica:
    def __init__(self,bd:db,AI:MachineLearing):
        self.bd = bd
        self.AI = AI
        self.entrenar_prediccion_mes()

    #Metodos de validacion
    def validar_texto(self,texto):
        if len(texto) <= 0 :
            return False
        if texto.isdigit():
            return False
        if not isinstance(texto,str):
            return False
        return True

    def validar_numero(self,numero):
        if numero <= 0:
            return False
        if not isinstance(numero,float):
            return False
        return True

    def validar_numero_entero(self,numero):
        if numero <= 0:
            return False
        if not isinstance(numero,int):
            return False
        return True

    def es_festivo(self,mes):
        festivos = [11,12]
        if mes in festivos:
            return 1
        else:
            return 0

    def obtener_mes_actual(self):
        return datetime.today().month
    
    def entrenar_prediccion_mes(self):
        data = self.bd.obtener_venta_agrupada_por_mes()
        if data:
            self.AI.entrenar_linear_regression_mes(data)
        else:
            print('no hay data')


    #CRUD:Clientes
    def insertar_cliente(self,cliente:Cliente):
        if not self.validar_texto(cliente.nombre):
            return False,'El nombre del cliente no es valido'
        self.bd.insertar_cliente(cliente.a_tupla())
        return True,'Exito'
    
    def obtener_data_cliente(self,cliente:Cliente):
        busqueda_cliente = self.bd.obtener_data_cliente(cliente.id)
        if not busqueda_cliente:
            return False,'El cliente no existe'
        return self.bd.buscar_cliente(cliente.id),'Exito'
    
    def obtener_todos_clientes(self):
        return self.bd.obtener_clientes()
    
    def actualizar_cliente(self,cliente:Cliente):
        busqueda_cliente = self.bd.buscar_cliente(cliente.id)
        if not busqueda_cliente:
            return False,'El cliente no existe'
        if not self.validar_texto(cliente.nombre):
            return False,'El nombre del cliente no es valido'
        self.bd.actualizar_cliente(cliente.id,cliente.a_tupla())
        return True,'Exito'

    def eliminar_cliente(self,cliente:Cliente):
        busqueda_cliente = self.bd.buscar_cliente(cliente.id)
        if not busqueda_cliente:
            return False,'El cliente no existe'
        self.bd.eliminar_cliente(cliente.id)
        return True,'Exito'

    #CRUD:Productos
    def insertar_producto(self,producto:Producto):
        if not self.validar_texto(producto.nombre):
            return False,'El producto no tiene un nombre valido'
        if not self.validar_numero(producto.precio_costo):
            return False,'El producto no tiene un costo valido'
        self.bd.insertar_producto(producto.a_tupla())
        return True,'Exito'

    def obtener_data_producto(self,producto:Producto):
        if not self.bd.obtener_data_producto(producto.id):
            return False,'El producto no existe'
        return self.bd.obtener_data_producto(producto.id),'Exito'
    def obtener_todos_productos(self):
        return self.bd.obtener_productos()

    def actualizar_producto(self,producto:Producto):
        if not self.validar_texto(producto.nombre):
            return False,'El producto no tiene un nombre valido'
        if not self.validar_numero(producto.precio_costo):
            return False,'El producto no tiene un costo valido'
        self.bd.actualizar_producto(producto.id,producto.a_tupla())#('pan',2.5,5.0)
        return True,'Exito'
        
    def eliminar_producto(self,producto:Producto):
        busqueda_producto = self.obtener_data_producto()
        if not busqueda_producto:
            return False,'El producto no existe'
        self.bd.eliminar_producto(producto.id)
        return True,'Exito'

   
    #CRUD:ventas
    def insertar_venta(self,venta:Venta):
        if not self.validar_numero(venta.total):
            return False,'La venta no tiene un total valido',False
        id_retornado = self.bd.insertar_venta(venta.a_tupla())
        return True,'Exito',id_retornado

    def obtener_data_venta(self,venta:Venta):
        if not self.bd.obtener_data_venta(venta.id):
            return False,'La venta no existe'
        return self.bd.obtener_data_venta(venta.id),'Exito'

    def obtener_todas_ventas(self):
        return self.bd.obtener_ventas()

    def actualizar_venta(self,venta:Venta):
        if not self.obtener_data_venta(venta):
            return False,'La venta no existe'
        if not self.validar_numero(venta.total):
            return False,'La venta no tiene un total valido'
        self.bd.actualizar_venta(venta.id,venta.a_tupla())
        return True,'Exito'

    def eliminar_venta(self,venta):
        if not self.obtener_data_venta(venta):
            return False,'La venta no existe'
        self.bd.eliminar_venta(venta.id)
        return True,'Exito'

    def calcular_total_venta(self,precio_unitario,cantidad):
        return precio_unitario * cantidad

    def obtener_suma_ventas(self):
        suma_ventas = self.bd.obtener_suma_ventas()[0] 
        if suma_ventas != None:
            return suma_ventas
        else:
            return 0 
            
    def obtener_ventas_en_deuda_nombres(self):
        ventas_en_deuda = self.bd.obtener_ventas_en_deuda_nombres()
        if ventas_en_deuda:
            return ventas_en_deuda
        else:
            print("NO HAY VENTAS")
            return False
            input("")
    
    def obtener_ventas_en_deuda_ids(self):
        ventas_en_deuda = self.bd.obtener_ventas_en_deuda_ids()
        if ventas_en_deuda:
            return ventas_en_deuda
        else:
            print("NO HAY VENTAS")
            return False
            input("")

    def obtener_prediccion_ventas_mes_actual(self):
        mes_actual = self.obtener_mes_actual()
        es_festivo = self.es_festivo(mes_actual)
        predict = self.AI.predecir_linear_regression_mes(
            mes=mes_actual,
            es_festivo = es_festivo
        )
        return predict

    def obtener_ventas_mes_actual(self):
        datos = self.bd.obtener_ventas_mes_actual()
        if datos:
            return datos[0]
        else:
            return 0
    
            

    #CRUD:detalle_ventas
    def insertar_detalle_venta(self,detalle_venta:DetalleVentas):
        if not self.validar_numero(detalle_venta.precio_unitario):
            return False,'El detalle_venta no tiene un precio unitario valido'
        if not self.validar_numero_entero(detalle_venta.cantidad):
            return False,'El detalle_venta no tiene una cantidad valida'
        self.bd.insertar_detalle_venta(detalle_venta.a_tupla())
        return True,'Exito'

    def obtener_data_detalle_venta(self,detalle_venta:DetalleVentas):
        if not self.db.obtener_data_detalles_venta(detalle_venta.venta_id):
            return False,'El detalle_venta no existe'
        return self.bd.obtener_data_detalles_venta(detalle_venta.venta_id),'Exito'

    def actualizar_detalle_venta(self,detalle_venta:DetalleVentas):
        if not self.bd.obtener_data_detalles_venta(detalle_venta.venta_id):
            return False,'El detalle_venta no existe'
        if not self.validar_numero(detalle_venta.precio_unitario):
            return False,'El detalle_venta no tiene un precio unitario valido'
        if not self.validar_numero_entero(detalle_venta.cantidad):
            return False,'El detalle_venta no tiene una cantidad valida'
        self.bd.actualizar_detalle_venta(detalle_venta.venta_id,detalle_venta.a_tupla())
        return True,'Exito'

    def eliminar_detalle_venta(self,detalle_venta:DetalleVentas):
        if not self.bd.obtener_data_detalles_venta(detalle_venta.venta_id):
            return False,'El detalle_venta no existe'
        self.bd.eliminar_detalles_venta(detalle_venta.venta_id)
        return True,'Exito'

    #CRUD:Gastos
    def insertar_gasto(self,gasto:Gastos):
        if not self.validar_numero(gasto.monto):
            return False,'El gasto no tiene un monto valido'
        self.bd.insertar_gasto(gasto.a_tupla())
        return True
    
    def obtener_data_gasto(self,gasto:Gastos):
        if not self.db.obtener_data_gasto(gasto.id):
            return False,"El gasto no existe"
        return self.db.obtener_data_gasto(gasto.id),"Exito"
    
    def actualizar_gasto(self,gasto:Gastos):
        if not self.db.obtener_data_gasto(gasto.id):
            return False,'El gasto no existe'
        if not self.validar_numero(gasto.monto):
            return False,'El gasto no tiene un monto valido'
        self.db.actualizar_gasto(gasto.id,gasto.a_tupla())
        return True,'Exito'

    def eliminar_gasto(self,gasto:Gastos):
        if not self.db.obtener_data_gasto(gasto.id):
            return False,'El gasto no existe'
        self.db.eliminar_gasto(gasto.id)
        return True,'Exito'

    def obtener_suma_gastos(self):
        suma_gastos = self.bd.obtener_suma_gastos()[0]
        if suma_gastos != None:
            return suma_gastos
        else:
            return 0
    #Estados de pago
    def obtener_estados_de_pago(self):
        return self.bd.obtener_estados_de_pago()

    #Categorias
    def obtener_categorias(self):
        return self.bd.obtener_categorias()

    #Referencias
    def obtener_referencias(self):
        return self.bd.obtener_referencias()



