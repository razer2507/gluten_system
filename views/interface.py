
from logic.logic import Logica
import customtkinter as ctk


class InterfazGrafica():
    def __init__(self,logica:Logica):
        self.logica = logica
        self.ventana_principal = ctk.CTk()
        self.contenedor_pantallas = ctk.CTkFrame(self.ventana_principal, fg_color="transparent")
        self.contenedor_pantallas.pack(fill="both", expand=True, padx=20, pady=20)
        self.pantalla_inicio()
        self.index_pantalla_actual = 1
        self.pantallas = {
            1:self.pantalla_inicio,
            2:self.pantalla_ejemplo2,
            3:self.pantalla_ejemplo3
        }   

        
        self.ventana_principal.mainloop()


    '''
    def menu_loguin(self):
        usuario_label = ctk.CTkLabel(self.ventana_principal,text="Usuario")
        usuario_label.pack()
        usuario_entry = ctk.CTkEntry(self.ventana_principal)
        usuario_entry.pack()
    '''

    def cambiar_pantalla(self):
        #limpia la pantalla para cambiar a otra
        for widget in self.contenedor_pantallas.winfo_children():
            widget.destroy()
    
        n_pantallas = len(self.pantallas)
        print(self.index_pantalla_actual)
        print(range(1,n_pantallas))

        if self.index_pantalla_actual in range(1,n_pantallas):
            self.index_pantalla_actual += 1
            self.pantallas[self.index_pantalla_actual]()
            
        else:
            self.index_pantalla_actual = 1
            self.pantallas[self.index_pantalla_actual]()

    def pantalla_inicio(self):
        label_ejemplo = ctk.CTkLabel(self.contenedor_pantallas,text="8---->>>>>")
        label_ejemplo.pack()
        cambiar_pag_boton = ctk.CTkButton(self.contenedor_pantallas,text='>>',command=lambda:self.cambiar_pantalla())
        cambiar_pag_boton.pack()
    
    def pantalla_ejemplo2(self):
        label_ejemplo2 = ctk.CTkLabel(self.contenedor_pantallas,text="PAAKDAWMKDMAWDKMKDAMWKD")
        label_ejemplo2.pack()
        cambiar_pag_boton = ctk.CTkButton(self.contenedor_pantallas,text='>>',command=lambda:self.cambiar_pantalla())
        cambiar_pag_boton.pack()

    def pantalla_ejemplo3(self):
        label_ejemplo3 = ctk.CTkLabel(self.contenedor_pantallas,text="Print('hello world en tk')")
        label_ejemplo3.pack()
        cambiar_pag_boton = ctk.CTkButton(self.contenedor_pantallas,text='>>',command=lambda:self.cambiar_pantalla())
        cambiar_pag_boton.pack()



