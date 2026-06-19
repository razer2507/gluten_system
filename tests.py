from logic.logic import Logica
from data.data import db
from logic.models import Cliente,Producto,Venta,DetalleVentas,Gastos

'''
#PRUEBA DE INSERCION DE CLIENTES
basedatos = db()
reglas = Logica(basedatos)

cliente_prueba = Cliente(
    nombre='Paul',
    referencia='Venecia',
)
reglas.insertar_cliente(cliente_prueba)
clientes = basedatos.obtener_clientes()
if(len(clientes)>0):print('Prueba EXITOSA!!!');

'''

#PRUEBA DE ELIMINADO DE CLIENTES


'''
basedatos = db()
reglas = Logica(basedatos)


cliente_prueba = Cliente(
    id='2',
    nombre='Paul',
    referencia='Venecia',
)
reglas.eliminar_cliente(cliente_prueba)
cliente_busqueda = basedatos.buscar_clientes(cliente_prueba.id)
if not cliente_busqueda:print('prueba exitosa')
print(basedatos.obtener_clientes())
'''

basedatos = db()
reglas = Logica(basedatos)


cliente_modificar = Cliente(
    id=3,
    nombre='juandieguin',
    referencia='carupano'
    
)

reglas.actualizar_cliente(cliente_modificar)
print(basedatos.obtener_clientes())