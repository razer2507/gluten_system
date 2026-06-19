from logic.logic import Logica
from data.data import db
from logic.models import Cliente,Producto,Venta,DetalleVentas,Gastos
import sys
import time
import os 
from datetime import datetime

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
        self.reglas = reglas
        self.menu_principal()
    
    def menu_principal(self):
        while True:
            ventas_totales = self.reglas.obtener_suma_ventas()
            gastos_totales = self.reglas.obtener_suma_gastos()
            balance = (ventas_totales-gastos_totales)
            clear()
            try:
                print('''
#####################################
|   GLUTEN FULL SYSTEM 1.0 TERMINAL |
#####################################''')

                print(f'''1-Registrar Productos\n2-Registrar Clientes\n3-Registrar Deudas\n4-Registrar Ventas\n5-Ver Ventas\n0-Salir\n{'='*38}''')
                print(f'VENTAS:{int(ventas_totales)}$\nGASTOS:{int(gastos_totales)}$\nBALANCE:{int(balance)}$\n')
                op = int(input("Escriba una opcion-->\n"))
                
                if op == 0:
                    clear()
                    print("Saliendo...")
                    break
                if op in range(0,6):
                    self.elegir_opcion(op)

            except ValueError as e:
                print(e)
            except KeyboardInterrupt:
                clear()
                print("Volviendo al menu principal")
                presione_enter_para_continuar()

            
    def elegir_opcion(self,op):
                match op:
                    case 1:
                        self.registrar_productos()
                    case 2:
                        self.registrar_clientes()
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
                print(mensaje2)
        else:
            print(mensaje1)

        presione_enter_para_continuar()






    #FUNCIONES AUX:FIXME
    def elegir_referencia(self):
        while True:
            clear()
            carga_programa()
            print("Referencia a elegir")
            referencias = self.reglas.obtener_referencias()

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
            categorias = self.reglas.obtener_categorias()

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
        clientes = self.reglas.obtener_todos_clientes()
        while True:
            print("Clientes a elegir")
            for index,cliente in enumerate(clientes,start=1):
                print(f'{index}. {cliente[1]}')
            opcion = int(input("Opcion:"))-1
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
            productos = self.reglas.obtener_todos_productos()

            for index,producto in enumerate(productos,start=1):
                print(f'{index}. {producto[1]}')
            opcion = int(input("Opcion:"))-1

            if opcion in productos_vendidos.keys():
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
        print(total)
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
            estados = self.reglas.obtener_estados_de_pago()
            for index,estado in enumerate(estados,start=1):
                print(f'{index}. {estado[0]}')
            opcion = int(input("Escriba una opcion\n:"))
            if opcion in range(len(estados)):
                return estados[opcion][0]
            else:
                print('Invalido')
                presione_enter_para_continuar()
                continue
        

mibd = db()
milogica = Logica(mibd)
miapp_terminal = TerminalInterface(milogica)