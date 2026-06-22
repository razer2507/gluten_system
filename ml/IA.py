import numpy as np
from sklearn.linear_model import LinearRegression


class MachineLearing:
    def __init__(self):
        self.modelo = LinearRegression()
        self.entrenado = False

    '''
        Toma los datos dados por el diccionario de las ventas de cada mes
        y lo lleva a una lista bidimensional

        datos_x = [[1,es_festivo],[2,no_es_festivo]]
        datos_y = [[1200],[1100]]

        las variables info_mes y ventas_mes extraen la data del diccionario
        para insertarlas en la lista de x,y
    '''
    def entrenar_linear_regression_mes(self,data):
        data_dict = self.preparar_data_meses_linear_regression(data)
        datos_x = []
        datos_y = []
        for mes,datos in data_dict.items():
            info_mes = [mes,datos['festivo']]
            ventas_mes = datos['ventas']
            datos_x.append(info_mes)
            datos_y.append(ventas_mes)
        self.modelo.fit(datos_x,datos_y)
        self.entrenado = True


    '''
        1.Toma x(los meses) *el sistema determina automaticamente si es un mes festivo o no*
        2.Toma y (las ventas producidas)
        3.las convierte a un formato de diccionario mediante el metodo preparar_data
        4.luego entrena al modelo y este se encarga de convertirla al formato de lista bidimensional
        5.busca en el diccionario si es un dia festivo o no 
    '''
    def predecir_linear_regression_mes(self,mes,es_festivo):
        print(mes,es_festivo)
        data = self.modelo.predict([[mes,es_festivo]])
        prediccion = data[0]
        return prediccion

    
    '''
        Crea un diccionario donde
        La key es el numero del mes (0,1)
        El valor es otro diccionario que con tiene las ventas del mes y si se considera festivo
        ejemplo = {
            1:{'ventas':1200,'es_festivo':0}
        }

        el valor de es festivo esta determinado por el numero del mes
        si el mes esta en el mes 11 o 12, se considera festivo
    '''
        
    def preparar_data_meses_linear_regression(self,data:tuple):
        meses_considerados_festivos = [11,12]
        ventas_meses = {
        }
        for tupla in data:
            mes = int(tupla[0])
            total = int(tupla[1])
            es_festivo = 1 if mes in meses_considerados_festivos else 0
            ventas_meses[mes] = {
                'ventas':total,
                'festivo':es_festivo
            }

        return ventas_meses



