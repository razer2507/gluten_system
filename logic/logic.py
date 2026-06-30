from data.data import db
from logic.models import Cliente,Producto,Venta,DetalleVentas,Gastos,AnalisisCredito
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
        data = self.bd.obtener_ventas_agrupada_por_mes_total()

        if data:
            self.AI.entrenar_linear_regression_mes(data)
            
        else:
            print('no hay data')


    #CRUD:Clientes
    def insertar_cliente(self,cliente:Cliente):
        if not self.validar_texto(cliente.nombre):
            return False,'El nombre del cliente no es valido'

        else:
            self.bd.insertar_cliente(cliente.a_tupla())
            return True,'Exito'
    
    def obtener_cliente_por_id(self,cliente:Cliente):
        datos_cliente = self.bd.obtener_cliente_por_id(cliente.id)

        if not datos_cliente:
            return False,'El cliente no existe'

        else:
            return datos_cliente,'Exito'
    
    def obtener_clientes_globales(self):
        datos_clientes = self.bd.obtener_clientes_globales()

        if not datos_clientes:
            return False,'No hay clientes'

        else:
            return datos_clientes,'Exito'

    def obtener_clientes_busqueda_por_nombre(self,nombre):
        busqueda = self.bd.obtener_clientes_busqueda_por_nombre(nombre)

        if not busqueda:
            return False,'No hay clientes con ese nombre'

        if busqueda[0] == None:
            return False,'No hay clientes con ese nombre'

        else:
            return busqueda,'Exito'

    
    def actualizar_cliente_por_id(self,cliente:Cliente):
        datos_cliente = self.bd.obtener_cliente_por_id(cliente.id)

        if not datos_cliente:
            return False,'El cliente no existe'

        if not self.validar_texto(cliente.nombre):
            return False,'El nombre del cliente no es valido'

        else:
            self.bd.actualizar_cliente_por_id(cliente.id,cliente.a_tupla())
            return True,'Exito'

    def eliminar_cliente_por_id(self,cliente:Cliente):
        datos_cliente = self.bd.obtener_cliente_por_id(cliente.id)

        if not datos_cliente:
            return False,'El cliente no existe'

        else:
            self.bd.eliminar_cliente_por_id(cliente.id)
            return True,'Exito'

    def obtener_clientes_ordenados_por_nombre_formato_dict(self):
        clientes = self.bd.obtener_clientes_ordenados_por_nombre()
        print(clientes)
        if clientes[0] == None:
            return False,'No hay clientes'

        if clientes == None:
            return False,'No hay clientes'
            
        else:
            #Guarda a los clientes en un diccionario
            #{'id_cliente-nombre_cliente':id}
            #{'1-Paul':1}
            diccionario_clientes = {f'{cliente[0]}-{cliente[1]}':cliente[0] for cliente in clientes}
            return diccionario_clientes,'Exito'


    #CRUD:Productos
    def insertar_producto(self,producto:Producto):
        if not self.validar_texto(producto.nombre):
            return False,'El producto no tiene un nombre valido'

        if not self.validar_numero(producto.precio_costo):
            return False,'El producto no tiene un costo valido'

        else:
            self.bd.insertar_producto(producto.a_tupla())
            return True,'Exito'

    def obtener_producto_por_id(self,producto:Producto):
        datos_producto = self.bd.obtener_producto_por_id(producto.id)

        if not datos_producto:
            return False,'El producto no existe'

        else:
            return datos_producto,'Exito'
    
    def obtener_productos_globales(self):
        datos_productos_globales = self.bd.obtener_productos_globales()

        if not datos_productos_globales:
            return False,'No hay productos'

        else:
            return datos_productos_globales,'Exito'


    def actualizar_producto_por_id(self,producto:Producto):
        if not self.validar_texto(producto.nombre):
            return False,'El producto no tiene un nombre valido'

        if not self.validar_numero(producto.precio_costo):
            return False,'El producto no tiene un costo valido'

        else:
            self.bd.actualizar_producto_por_id(producto.id,producto.a_tupla())
            return True,'Exito'
        
    def eliminar_producto_por_id(self,producto:Producto):
        data_producto = self.bd.obtener.obtener_producto_por_id(producto.id)

        if not data_producto:
            return False,'El producto no existe'

        else:
            self.bd.eliminar_producto_por_id(producto.id)
            return True,'Exito'

   
    #CRUD:ventas
    def insertar_venta(self,venta:Venta):
        if not self.validar_numero(venta.total):
            return False,'La venta no tiene un total valido'

        else: 
            id_retornado = self.bd.insertar_venta(venta.a_tupla())
            return True,'Exito',id_retornado

    def obtener_venta_por_id(self,venta:Venta):
        if not self.bd.obtener_venta_por_id(venta.id):
            return False,'La venta no existe'

        else:
            return self.bd.obtener_venta_por_id(venta.id),'Exito'

    def obtener_ventas_globales_con_nombre(self):
        ventas = self.bd.obtener_ventas_globales_con_nombre()

        if not ventas:
            return False,'No hay ventas'

        else:
            return ventas,'Exito'

    def actualizar_venta_por_id(self,venta:Venta):
        if not self.bd.obtener_venta_por_id(venta.id):
            return False,'La venta no existe'

        if not self.validar_numero(venta.total):
            return False,'La venta no tiene un total valido'

        else:
            self.bd.actualizar_venta_por_id(venta.id,venta.a_tupla())
            return True,'Exito'

    def eliminar_venta_por_id(self,venta):
        if not self.obtener_venta_por_id(venta):
            return False,'La venta no existe'

        else:
            self.bd.eliminar_venta_por_id(venta.id)
            return True,'Exito'

    def calcular_total_venta(self,precio_unitario,cantidad):
        return precio_unitario * cantidad

    def obtener_ventas_globales_total(self):
        ventas_globales = self.bd.obtener_ventas_globales_total()

        if not ventas_globales:
            return 0,'No hay ventas'

        else:
            return ventas_globales,'Exito'
            
    def obtener_ventas_en_deuda_globales_con_nombre(self):
        ventas_en_deuda = self.bd.obtener_ventas_en_deuda_globales_con_nombres()

        if not ventas_en_deuda:
            return False,'No hay deudas'

        else:
            return ventas_en_deuda,'Exito'

    def obtener_ventas_en_deuda_globales(self):
        ventas_en_deuda = self.bd.obtener_ventas_en_deuda_globales()

        if not ventas_en_deuda:
            return False,'No hay deudas'

        else:
            return ventas_en_deuda,'Exito'

    def obtener_prediccion_ventas_mes_actual(self):
        mes_actual = self.obtener_mes_actual()
        es_festivo = self.es_festivo(mes_actual)

        predict = self.AI.predecir_linear_regression_mes(
            mes=mes_actual,
            es_festivo = es_festivo
        )

        return predict

    def obtener_ventas_mes_actual_total(self):
        ventas_mes_actual = self.bd.obtener_ventas_mes_actual_total()
        monto_ventas_mes_actual = ventas_mes_actual[0]

        if not ventas_mes_actual:
            return 0,'No hay ventas en este mes'

        else:
            return monto_ventas_mes_actual,'Exito'

    def obtener_ventas_en_deuda_mes_actual_total(self):
        ventas_en_deuda_mes_actual = self.bd.obtener_ventas_en_deuda_mes_actual_total()
        
        if not ventas_en_deuda_mes_actual:
            return 0,'No hay deudas en este mes'
        if ventas_en_deuda_mes_actual[0] == None:
            return 0

        else:
            return ventas_en_deuda_mes_actual,'Exito'


            

    #CRUD:detalle_ventas
    def insertar_detalle_venta(self,detalle_venta:DetalleVentas):
        if not self.validar_numero(detalle_venta.precio_unitario):
            return False,'El detalle_venta no tiene un precio unitario valido'

        if not self.validar_numero_entero(detalle_venta.cantidad):
            return False,'El detalle_venta no tiene una cantidad valida'
        else:
            self.bd.insertar_detalle_venta(detalle_venta.a_tupla())
            return True,'Exito'

    def obtener_detalle_venta_por_id(self,detalle_venta:DetalleVentas):
        if not self.bd.obtener_detalle_venta_por_id(detalle_venta.venta_id):
            return False,'El detalle_venta no existe'

        else:
            return self.bd.obtener_detalle_venta_por_id(detalle_venta.venta_id)

    def actualizar_detalle_venta_por_id(self,detalle_venta:DetalleVentas):
        if not self.bd.obtener_detalle_venta_por_id:
            return False,'El detalle_venta no existe'

        if not self.validar_numero(detalle_venta.precio_unitario):
            return False,'El detalle_venta no tiene un precio unitario valido'

        if not self.validar_numero_entero(detalle_venta.cantidad):
            return False,'El detalle_venta no tiene una cantidad valida'

        else:
            self.bd.actualizar_detalle_venta_por_id(detalle_venta.id,detalle_venta.a.tupla())
            return True,'Exito'

    def eliminar_detalle_venta_por_id(self,detalle_venta:DetalleVentas):
        if not self.obtener_detalle_venta_por_id(detalle_venta.id):
            return False,'El detalle_venta no existe'

        else:
            self.bd.eliminar_detalle_venta_por_id(detalle_venta.venta_id)
            return True,'Exito'

    #CRUD:Gastos
    def insertar_gasto(self,gasto:Gastos):
        if not self.validar_numero(gasto.monto):
            return False,'El gasto no tiene un monto valido'

        else:
            self.bd.insertar_gasto(gasto.a_tupla())
            return True
    
    def obtener_gasto_por_id(self,gasto:Gastos):
        if not self.db.obtener_gasto_por_id(gasto.id):
            return False,"El gasto no existe"

        else:
            return self.obtener_gasto_por_id(gasto.id)
    
    def actualizar_gasto(self,gasto:Gastos):
        if not self.bd.obtener_gasto_por_id(gasto.id):
            return False,'El gasto no existe'

        if not self.validar_numero(gasto.monto):
            return False,'El gasto no tiene un monto valido'

        else:
            self.bd.actualizar_gasto_por_id(gasto.id,gasto.a_tupla())
            return True,'Exito'

    def eliminar_gasto(self,gasto:Gastos):
        if not self.bd.obtener_gasto_por_id(gasto.id):
            return False,'El gasto no existe'

        else:
            self.bd.eliminar_gasto_por_id(gasto.id)
            return True,'Exito'

    def obtener_gastos_globales_total(self):
        suma_gastos = self.bd.obtener_gastos_globales_total()[0]

        if suma_gastos != None:
            return suma_gastos

        else:
            return 0


    def insertar_analisis_credito(self,analisis_credito:AnalisisCredito):
        if not self.validar_numero_entero(analisis_credito.dias_en_pagar):
            return False,'El analisis credito no tiene un dias en pagar valido'

        if not self.validar_numero_entero(analisis_credito.venta_id):
            return False,'El analisis credito no tiene un id_venta valido'

        if not self.validar_numero_entero(analisis_credito.cliente_id):
            return False,'El analisis credito no tiene un id_cliente valido'

        self.bd.insertar_analisis_credito(analisis_credito.a_tupla())
        return True,'Exito'


    #Estados de pago
    def obtener_estados_de_pago_globales(self):
        return self.bd.obtener_estados_de_pago_globales()

    #Categorias
    def obtener_categorias_globales(self):
        return self.bd.obtener_categorias_globales()

    #Referencias
    def obtener_referencias_globales(self):
        return self.bd.obtener_referencias_globales()

    #Usuarios
    def revisar_si_credenciales_son_validas(self,usuario,clave):
        existencia = self.bd.revisar_si_credenciales_son_validas(usuario,clave)
        return bool(existencia)


