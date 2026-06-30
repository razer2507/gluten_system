import tkinter as tk
from data.data import db
from logic.logic import Logica
from ml.IA import MachineLearing
from views.interface import InterfazGrafica
from views.interface import LoginUser
'''
if __name__ == "__main__":
    

    mi_db = db()
    mi_IA = MachineLearing()
    mi_logica = Logica(
        bd=mi_db,
        AI=mi_IA
    )

    mi_login = LoginUser(mi_logica)
    
    if mi_login.verificado == True:
        mi_interfaz = InterfazGrafica(
        logica=mi_logica
        )
'''