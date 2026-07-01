from data.data import db
from logic.logic import Logica
from views.interface import InterfazGrafica
from ml.IA import MachineLearing

ml = MachineLearing()
basedatos = db()
logic = Logica(basedatos,ml)
InterfazGrafica(logic)
