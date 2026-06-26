from logic.logic import Logica
from data.data import db
from logic.models import Cliente,Producto,Venta,DetalleVentas,Gastos
import sys
import time
import os 
from datetime import datetime
from ml.IA import MachineLearing

fecha_actual = datetime.now().strftime("%Y-%m-%d")

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def carga_programa():
    carga = '...'
    print('Cargando',end='')
    for i in carga:
        print(i,end='',flush=True)
        time.sleep(0.5)
    print('\n')
    clear()

def presione_enter_para_continuar():
    input("PRESIONE ENTER PARA CONTINUAR")


class TerminalInterface():
    def __init__(self,reglas:Logica):
        self.reglas = reglas
        self.menu_principal()
    
    def menu_principal(self):
        while True:
            mes_actual = datetime.today().month
            prediccion = self.reglas.obtener_prediccion_ventas_mes_actual()
            ventas_actuales_mes = self.reglas.obtener_ventas_mes_actual_total()[0]
            deudas_totales_mes = self.reglas.obtener_ventas_en_deuda_mes_actual_total()[0][0]
            gananacia_real = (ventas_actuales_mes-deudas_totales_mes)
            porcentaje_deudas_mes = (deudas_totales_mes/ventas_actuales_mes)*100
            try:
                clear()
                carga_programa()
                print('''
#####################################
|   GLUTEN FULL SYSTEM 1.0 TERMINAL |
#####################################''')
                print(f"FECHA:{datetime.today().strftime('%d/%m/%Y')}")
                print('#####################################')
                print(f'''1-Registrar Productos\n2-Registrar Clientes\n3-Administar-Deudas\n4-Registrar Ventas\n5-Ver Ventas\n0-Salir\n{'='*38}''')
                print(f'VENTAS DEL MES ACTUAL:{(ventas_actuales_mes)}$')
                print(f'DEUDAS DEL MES ACTUAL:{(deudas_totales_mes)}$({int(porcentaje_deudas_mes)}%)')
                print(f'GANANCIA MENSUAL REAL: {int(gananacia_real)}$')
                print(f'PROYECCION MENSUAL DE VENTAS POR IA:{int(prediccion)}$')
                print("="*38)
                
                op = int(input("Escriba una opcion-->\n"))
                
                if op == 0:
                    clear()
                    print("Saliendo...")
                    break
                
                if op in range(0,6):
                    self.elegir_opcion(op)

            except ValueError as e:
                print("Opcion de menu no valida.")
            except KeyboardInterrupt:
                clear()
                print("Volviendo al menu principal.")
                presione_enter_para_continuar()

            
    def elegir_opcion(self,op):
                match op:
                    case 1:
                        self.registrar_productos()
                    case 2:
                        self.registrar_clientes()
                    case 3:
                        self.administar_deudas()
                    case 4:
                        self.registrar_venta()
                    case 5:
                        self.ver_ventas()


    #FUNCIONES PRINCIPALES
    def registrar_productos(self):
        try:
            clear()
            carga_programa()

            nombre_producto = input("Escriba el nombre del producto\n:")
            precio_costo = float(input("Escriba el precio costo\n:"))
            categoria = self.elegir_categoria()

            producto_creado = Producto(nombre_producto,precio_costo,categoria)
            resultado,mensaje = self.reglas.insertar_producto(producto_creado)

            print(mensaje)
            presione_enter_para_continuar()

        except ValueError:
            print("Datos invalidos")
            presione_enter_para_continuar


    def registrar_clientes(self):
        clear()
        carga_programa()

        nombre_cliente = input("Escriba el nombre del ciente\n:")
        referencia = self.elegir_referencia()

        cliente_creado = Cliente(nombre_cliente,referencia)
        resultado,mensaje = self.reglas.insertar_cliente(cliente_creado)

        
        print(mensaje)
        presione_enter_para_continuar()

    def registrar_venta(self):
        clear()
        carga_programa()

        fecha = self.elegir_fecha()
        cliente = self.elegir_cliente()
        cliente_id = cliente[0]
        cliente_nombre = cliente[1]
        ticket_venta = self.construir_ticket()
        total = self.calcular_total_ticket(ticket_venta)
        estado = self.elegir_estado()

        clear()

        print(f"CLIENTE:{cliente_nombre}")
        self.imprimir_ticket(ticket_venta)
        presione_enter_para_continuar()

        venta = Venta(
            fecha=fecha,
            cliente_id=cliente_id,
            total=total,
            estado=estado
        )
        resultado1,mensaje1,id_retornado = self.reglas.insertar_venta(venta)

        if resultado1 == True:
            for id_producto,detalle in ticket_venta.items():
                detalle = DetalleVentas(
                    venta_id=id_retornado,
                    producto_id=id_producto,
                    cantidad=ticket_venta[id_producto]['cantidad'],
                    precio_unitario=ticket_venta[id_producto]['precio_unitario']
                )
                resultado2,mensaje2 = self.reglas.insertar_detalle_venta(detalle)

                print(f'{ticket_venta[id_producto]['nombre_producto']} registrado exitosamente.')
        else:
            print(mensaje1)
            

        presione_enter_para_continuar()

    def administar_deudas(self):
            while True:
                clear()
                carga_programa()
                print("1. Cambiar estado de venta")
                opcion = int(input("Opcion:"))
                match opcion:
                    case 1:
                        self.levantar_deudas()
                        break
                    case _:
                        print("Invalido")

    def ver_ventas(self):
        clear()
        carga_programa()
        confirmacion_ventas = self.reglas.obtener_ventas_globales_con_nombre()[0]

        if confirmacion_ventas == False:
            print("No hay ventas")
            presione_enter_para_continuar()
        
        ventas = self.reglas.obtener_ventas_globales_con_nombre()[0]

        
        # 📏 Definimos los anchos fijos para cada columna
        # <20 significa: alineado a la izquierda, ocupando exactamente 20 caracteres.
        # >10 significa: alineado a la derecha (ideal para números), ocupando 10 caracteres.
        formato = "{:<20} | {:<20} | {:>10} | {:>10}"
    
        print("-" * 82)  # Una línea decorativa superior
        # Imprimimos el encabezado usando el molde de formato
        print(formato.format('NOMBRE', 'REFERENCIA', 'TOTAL','FECHA'))
        print("-" * 82)  # Línea separadora
    
        # Imprimimos cada fila usando exactamente el mismo molde
        for venta in ventas:
            print(formato.format(str(venta[0]), str(venta[1]), f"{venta[2]:.2f}",str(venta[3])))
        
        print("-" * 82)
        presione_enter_para_continuar()


   
    def elegir_referencia(self):
        while True:
            clear()
            carga_programa()
            print("Referencia a elegir")
            referencias = self.reglas.obtener_referencias_globales()

            for index,referencia in enumerate(referencias,start=1):
                print(f'{index}. {referencia[0]}')
            opcion = int(input("Opcion:"))-1
            if opcion in range(len(referencias)):
                return referencias[opcion][0]
            else:
                print('Invalido')
                presione_enter_para_continuar()
                continue

    def elegir_categoria(self):
        while True:
            clear()
            carga_programa()
            print("Categoria a elegir")
            categorias = self.reglas.obtener_categorias_globales()

            for index,categoria in enumerate(categorias,start=1):
                print(f'{index}. {categoria[0]}')
            opcion = int(input('Opcion:'))-1

            if opcion in range(len(categorias)):
                return categorias[opcion][0]
            else:
                print('Invalido')
                presione_enter_para_continuar()
                continue

        """
    Permite al usuario elegir la fecha de la venta.
    Ofrece la opción rápida de usar la fecha de hoy o ingresar una manual.
    """
    def elegir_fecha(self):
        while True:
            print("Fecha a elegir")
            print("1. Usar la fecha y hora actual (Hoy)")
            print("2. Ingresar una fecha manualmente")
        
            opcion = input("\nSelecciona una opcion (1 o 2): ").strip()
        
            if opcion == "1":
                # Captura año-mes-día hora:minuto:segundo del momento exacto
                fecha_lista = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                return fecha_lista
            
            elif opcion == "2":
                print("\n📝 Ingresa la fecha en formato: AÑO-MES-DIA (Ejemplo: 2026-06-19)")
                fecha_manual = input("Fecha: ").strip()
            
                try:
                    # 🕵️‍♂️ Validamos que el formato sea el correcto antes de guardarlo
                    fecha_validada = datetime.strptime(fecha_manual, "%Y-%m-%d")
                
                    # Le sumamos una hora genérica por defecto (ej: mediodía) para mantener el formato de la BD
                    return fecha_validada.strftime("%Y-%m-%d 12:00:00")
                
                except ValueError:
                    print("\n Formato de fecha invalido. Recuerda usar guiones cortos y el orden AÑO-MES-DIA.")
                    presione_enter_para_continuar()
                    # El bucle while se repite si hay error
                
            else:
                print("Fecha invalida")
                presione_enter_para_continuar()

    def elegir_cliente(self):
        clear()
        carga_programa()
        confirmacion_clientes = self.reglas.obtener_clientes_globales()[0]

        if confirmacion_clientes == False:
            print('No hay clientes, PRESIONE CTRL+C para salir')
            input('')

        clientes = self.reglas.obtener_clientes_globales()[0]
        while True:
            print("Clientes a elegir")
            for index,cliente in enumerate(clientes,start=1):
                print(f'{index}. {cliente[1]}')
            print(f'0. Buscar cliente por nombre')
        

            opcion = int(input("Opcion:"))-1

            if opcion == -1:
                return self.obtener_cliente_por_nombre()
            
            if opcion == -2:
                return self.obtener_cliente_por_nombre()

            if opcion in range(len(clientes)):
                return clientes[opcion]

            else:
                print('Invalido')
                presione_enter_para_continuar()
                continue

    def construir_ticket(self):
        clear()
        carga_programa()
        '''
        productos_vendidos = {
        1:{'cantidad':2,
            'precio_unitario':3.5}
        }
        '''
        productos_vendidos = {}
        
        while True:
            print("Productos a elegir")
            confirmacion_productos = self.reglas.obtener_productos_globales()[0]

            if confirmacion_productos == False:
                print('No hay producutos,PRESIONE CTRL + C para salir')
                input("")
            
            productos = self.reglas.obtener_productos_globales()[0]

            for index,producto in enumerate(productos,start=1):
                print(f'{index}. {producto[1]}')

            opcion = int(input("Opcion:"))-1

            if (opcion+1) in productos_vendidos.keys():
                clear()
                print("ERROR: Este producto ya ha sido registrado")
                presione_enter_para_continuar()
                continue

            if opcion in range(len(productos)):
                clear()

                nombre_producto = productos[opcion][1]
                id_producto = productos[opcion][0]

                print(f"Producto:{nombre_producto}")
                cantidad = int(input("Escriba la cantidad del producto vendido:"))
                precio_unitario = float(input("Escriba el precio unitario del producto vendido($):"))

                if all([self.reglas.validar_numero_entero(cantidad),
                        self.reglas.validar_numero(precio_unitario)]):
                        
                    productos_vendidos[id_producto] = {
                        'nombre_producto':nombre_producto,
                        'cantidad':cantidad,
                        'precio_unitario':precio_unitario
                    }

                    clear()
                    self.imprimir_ticket(productos_vendidos)

                    continuar = input("Desea Continuar registrando productos?(S/N):")

                    if continuar.lower() == 's':
                        clear()
                        continue

                    else:
                        return productos_vendidos
                else:
                    print("Datos invalidos")
                    presione_enter_para_continuar()

            else:
                print("Invalido")
                presione_enter_para_continuar()
            
            
    def calcular_total_ticket(self,ticket:dict):
        total = 0

        for producto,detalle in ticket.items():
            total += ticket[producto]['cantidad'] * ticket[producto]['precio_unitario']

        return total

    def imprimir_ticket(self,ticket:dict):
        print("="*30)
        n_prod = 1
        total_ticket = 0

        for producto,detalle in ticket.items():
            total_ticket += ticket[producto]['cantidad'] * ticket[producto]['precio_unitario']
            print(f'PRODUCTO N#{n_prod}\nNOMBRE:{ticket[producto]['nombre_producto']}\nCANTIDAD:{ticket[producto]['cantidad']}\nPRECIO_UNITARIO:{ticket[producto]['precio_unitario']}\nTOTAL:{ticket[producto]['precio_unitario']*ticket[producto]['cantidad']}\n')
            n_prod += 1

        print("-"*30)
        print(f"TOTAL VENTAS : {total_ticket}$")
        print('='*30)

    def elegir_estado(self):
        clear()
        carga_programa()

        print("Estados a elegir")
        while True:
            estados = self.reglas.obtener_estados_de_pago_globales()
            for index,estado in enumerate(estados,start=1):
                print(f'{index}. {estado[0]}')

            opcion = int(input("Escriba una opcion\n:"))-1

            if opcion in range(len(estados)):
                return estados[opcion][0]

            else:
                print('Invalido')
                presione_enter_para_continuar()
                continue

    def levantar_deudas(self):
        clear()
        carga_programa()
        #El usuario ve las ventas con nombres de clientes
        #El sistema lo ve con Id's
        while True:
            ventas_en_deuda_usuario = self.reglas.obtener_ventas_en_deuda_globales_con_nombre()[0]
            ventas_en_deuda_sistema = self.reglas.obtener_ventas_en_deuda_globales()[0]

            if ventas_en_deuda_usuario == False:
                print("No hay deudas pendientes. Presione CTRL+C para salir")
                input("")

            for index,venta in enumerate(ventas_en_deuda_usuario,start=1):
                print(f'{index} . {venta}')
            opcion = int(input("Opcion:"))-1

            if opcion in range(len(ventas_en_deuda_sistema)):
                clear()
                presione_enter_para_continuar()

                venta = Venta.desde_tupla(ventas_en_deuda_sistema[opcion])
                venta.estado = self.elegir_estado()

                venta.imprimir_venta()

                resultado,mensaje = self.reglas.actualizar_venta_por_id(venta)

                print(mensaje)
                presione_enter_para_continuar()
                break

            else:
                clear()
                print('Invalido')
                presione_enter_para_continuar()
                continue

    def obtener_cliente_por_nombre(self):

        #FIXME: revisar esta pingaaaaaaaaaaaaaa
        while True:
            clear()
            carga_programa

            nombre = input("Escriba el nombre del cliente a buscar: ")

            busqueda_cliente = self.reglas.obtener_clientes_busqueda_por_nombre(nombre)[0]

            if busqueda_cliente == None:
                print("Clientes no encontrados")
                presione_enter_para_continuar()
        
            elif busqueda_cliente[0] == None:
                print("Clientes no encontrados")
                presione_enter_para_continuar()
        
            else:    
                clientes = self.reglas.obtener_clientes_busqueda_por_nombre(nombre)[0]
        
                for index,cliente in enumerate(clientes,start=1):
                    cliente = Cliente.desde_tupla(cliente)
                    print(f'{index}. {cliente.nombre},{cliente.referencia}')
            
                try:
                    op = int(input("Opcion:"))-1

                    if op in range(len(clientes)):
                        return clientes[op]
                
                    else:
                        print("Opcion invalida.")

                except ValueError:
                        print("Opcion invalida.")

machineLearn = MachineLearing()
mibd = db()
milogica = Logica(mibd,machineLearn)
miapp_terminal = TerminalInterface(milogica)