
from logic.logic import Logica
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image

class InterfazGrafica():
    def __init__(self,logica:Logica):
        self.logica = logica
        self.ventana_principal = ctk.CTk()
        self.ventana_principal.title("GLUTEN SYSTEM (1.0)")

        self.contenedor_side_bar_visible = True
        self.contenedor_sidebar = ctk.CTkFrame(self.ventana_principal,width=220,corner_radius=0)
        self.contenedor_sidebar.pack(fill='y',side='left')
        self.contenedor_sidebar.pack_propagate(False)
        self.construir_sidebar()

        self.contenedor_pantallas = ctk.CTkFrame(self.ventana_principal, fg_color="transparent")
        self.contenedor_pantallas.pack(side='right',fill="both", expand=True, padx=20, pady=20)
        self.pantalla_inicio()

        self.index_pantalla_actual = 1
        self.pantallas = {
            1:self.pantalla_inicio,
            2:self.pantalla_ejemplo2,
            3:self.pantalla_ejemplo3,
            4:self.pantalla_ejemplo4
        }   

        
        self.ventana_principal.mainloop()
        

    def construir_sidebar(self):
        imagen_logo = ctk.CTkImage(
            light_image=Image.open('views/assets/gluten_logo.png'),
            dark_image=Image.open('views/assets/gluten_logo.png'),
            size=(100,100)
        )

        self.logo_imagen_label = ctk.CTkLabel(
            self.contenedor_sidebar,
            image=imagen_logo,
            text=""
        )
        self.logo_imagen_label.pack(pady=30,padx=20)

        

    def togglear_sidebar(self):
        
        if self.contenedor_side_bar_visible == True:#Entra como True
            self.contenedor_side_bar_visible = False#Sale como false
            self.toggle_sidebar_boton.configure(text='>')
            self.contenedor_sidebar.pack_forget()#Ejecuta la funcion de ocultacion
       
        else:#Entra como False
            self.contenedor_side_bar_visible = True#Sale como True
            self.toggle_sidebar_boton.configure(text='<')
            self.contenedor_sidebar.pack(fill='y',side='left')#Devuelve a la vida a la sidebar


    def construir_elementos_permanentes(self,frame:CTkFrame):

        self.toggle_sidebar_boton = ctk.CTkButton(frame,text='<',font=("Arial", 10, "bold"),command=lambda:self.togglear_sidebar(),width=10)
        self.toggle_sidebar_boton.pack(side="top", anchor="nw", padx=2, pady=2)

        
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

    def cambiar_pantalla_menu_lateral(self,index):#2
        self.index_pantalla_actual = index
        self.pantallas[self.index_pantalla_actual]()


    
    def pantalla_inicio(self):
        self.construir_elementos_permanentes(self.contenedor_pantallas)
    
    def pantalla_ejemplo2(self):
        self.construir_elementos_permanentes(self.contenedor_pantallas)

    def pantalla_ejemplo3(self):
        self.construir_elementos_permanentes(self.contenedor_pantallas)

    def pantalla_ejemplo4(self):
        self.construir_elementos_permanentes(self.contenedor_pantallas)

    def obtener_credenciales_usuario(self,user_entry:CTkEntry,clave_entry:CTkEntry):

        usuario = user_entry.get()
        clave = clave_entry.get()

        return usuario,clave
    


class LoginUser():

        def __init__(self,logica:Logica,verificado=False):
            self.logica = logica
            self.verificado = verificado
            self.ejecutar_menu_loguin()

        def ejecutar_menu_loguin(self):
            self.ventana_loguin = ctk.CTk()

            imagen_logo = ctk.CTkImage(
            light_image=Image.open('views/assets/gluten_logo.png'),
            dark_image=Image.open('views/assets/gluten_logo.png'),
            size=(150,150)
            )
            self.logo_imagen_label = ctk.CTkLabel(
            self.ventana_loguin,
            image=imagen_logo,
            text=""
            )
            self.logo_imagen_label.pack(pady=30,padx=20)

            self.ventana_loguin.title("LOGIN")
            usuario_label = ctk.CTkLabel(self.ventana_loguin,text="Usuario")
            usuario_label.pack()
            usuario_entry = ctk.CTkEntry(self.ventana_loguin)
            usuario_entry.pack()
        

            clave_label = ctk.CTkLabel(self.ventana_loguin,text="Clave")
            clave_label.pack()
            clave_entry = ctk.CTkEntry(self.ventana_loguin,show='*')
            clave_entry.pack()


            boton_ingresar = ctk.CTkButton(
            self.ventana_loguin,
            text="Ingresar",
            command=lambda:self.validar_credenciales(usuario_entry,clave_entry))
            boton_ingresar.pack(pady=20)


            self.ventana_loguin.mainloop()
        
        def validar_credenciales(self,usuario_entry,clave_entry):
            print(usuario_entry.get(),clave_entry.get())
            usuario = usuario_entry.get()
            clave = clave_entry.get()

            validacion = self.logica.revisar_si_credenciales_son_validas(usuario,clave)

            if validacion == True:
                msg = CTkMessagebox(title='Exito',message=f'Acceso concedido.\nBienvenido {usuario}',icon='check')
                
                if msg.get() == "OK": 
                    self.verificado = True
                    self.ventana_loguin.destroy()
            else:
                CTkMessagebox(title='Error',message=f'Credenciales Invalidas',icon='cancel')

