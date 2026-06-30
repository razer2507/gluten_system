
from logic.logic import Logica
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image
from tkcalendar import Calendar

class InterfazGrafica():
    #Inyecta la dependencia de la capa logica del sistema
    def __init__(self,logica:Logica):
        self.logica = logica
        #Incializa la ventana principal
        self.ventana_principal = ctk.CTk()
        self.ventana_principal.title("GLUTEN SYSTEM (1.0)")
        #Crea la el espacio(frame) en donde se construira el menu de lado
        self.contenedor_side_bar_visible = True

        self.contenedor_sidebar = ctk.CTkFrame(
            self.ventana_principal,
            width=220,
            corner_radius=0,
            border_color='black',
            border_width=1)
            
        #Lo empaqueta en el lado izquierdo y llena todo el espacio vertical restante
        self.contenedor_sidebar.pack(fill='y',side='left')
        self.contenedor_sidebar.pack_propagate(False)
        #Construye todo el contenido del menu de lado en el frame
        self.construir_sidebar()


        #Construye el contenedor dinamico en donde se veran las pantallas(ventas,deudas,clientes,etc)
        self.contenedor_pantallas = ctk.CTkFrame(
        self.ventana_principal,
        fg_color="transparent")

        self.contenedor_pantallas.pack(
        side='right',
        fill="both", 
        expand=True, 
        padx=20, 
        pady=20)

        self.dibujar_dashboard_principal()

        #Crea un diccionario que le asigna una indexacion a cada funcion para ejecutar las pantallas
        self.index_pantalla_actual = 1
        self.pantallas = {
            1:self.dibujar_dashboard_principal,
            2:self.dibujar_pantalla_ventas,
        }   

        #Crea el bucle principal (mainloop)
        self.ventana_principal.mainloop()
        
    #Dibuja los elementos del sidebar en el frame
    def construir_sidebar(self):
        #Coloca el logo de la empresa en la parte superior del sidebar
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

        boton_pantalla_inicio = ctk.CTkButton(
            self.contenedor_sidebar,
            text='INICIO',
            font=('Arial',16,'bold'),
            command=lambda:self.cambiar_pantalla_menu_lateral(1),
            width=10
            )
        boton_pantalla_inicio.pack(pady=10,padx=10)
        
        boton_pantalla_ventas = ctk.CTkButton(
                self.contenedor_sidebar,
                text='VENTAS',
                font=('Arial',16,'bold'),
                command=lambda:self.cambiar_pantalla_menu_lateral(2),
                width=10
                )
        boton_pantalla_ventas.pack(pady=10,padx=10)
        


    #oculta-muestra sidebar
    def togglear_sidebar(self):
        
        if self.contenedor_side_bar_visible == True:
            self.contenedor_side_bar_visible = False
            self.toggle_sidebar_boton.configure(text='>')
            self.contenedor_sidebar.pack_forget()
       
        else:
            self.contenedor_side_bar_visible = True
            self.toggle_sidebar_boton.configure(text='<')
            self.contenedor_sidebar.pack(fill='y',side='left')

    #Construye elementos que deben ser visibles en todas las paginas(como el boton para ocultar el sidebar)
    def construir_elementos_permanentes(self,frame:CTkFrame):

        self.toggle_sidebar_boton = ctk.CTkButton(
            frame,
            text='<',
            font=("Arial", 10, "bold"),
            command=lambda:self.togglear_sidebar(),
            width=10)

        self.toggle_sidebar_boton.pack(
            side="top", 
            anchor="nw",
            padx=2, 
            pady=2)

    #Limpia la pantalla actual y permite dibujar otra    
    def limpiar_pantalla(self,contenedor:CtkFrame):

        for widget in contenedor.winfo_children():
            widget.destroy()


    #Cambia la pantalla desde el menu lateral
    def cambiar_pantalla_menu_lateral(self,index):#2

        self.limpiar_pantalla(self.contenedor_pantallas)
        self.index_pantalla_actual = index
        self.pantallas[self.index_pantalla_actual]()

    def construir_tarjeta(self,contenedor,titulo,valor):
        # 1. El contenedor principal de la tarjeta
        tarjeta_frame = ctk.CTkFrame(
            contenedor, 
            corner_radius=3,    # Esquinas redondeadas como en la imagen
            border_width=2,       # Un borde fino
            border_color="black", # Color gris claro para el borde
            width=135,
            height=100,

            )
        tarjeta_frame.pack(side="left",anchor='nw',padx=15, pady=15)
        #El tamano del frame no se afectado por el ancho de su contenido
        tarjeta_frame.pack_propagate(False)

        titulo_tarjeta = ctk.CTkLabel(
            tarjeta_frame, 
            text=f"{titulo}", 
            font=("Arial",20),
            text_color="black"
            )

        #pady=(12,5) haz 12 pixeles de espacios arriba y 5 abajo
        titulo_tarjeta.pack(anchor="w",padx=10,pady=(12,5))

        valor_label = ctk.CTkLabel(
        tarjeta_frame, 
        text=f"{valor}", 
        font=("Arial", 23, "bold"),
        text_color="black"
        )
        valor_label.pack(anchor="w",padx=15)

        
        





    def dibujar_dashboard_principal(self):
        self.construir_elementos_permanentes(self.contenedor_pantallas)
        self.construir_tarjeta(self.contenedor_pantallas,'Ventas',"147$")
        self.construir_tarjeta(self.contenedor_pantallas,'Deudas',"47$(35%)")
        


    #Dibuja la pantalla de ventas en el contenedor de pantallas
    def dibujar_pantalla_ventas(self):
        self.construir_elementos_permanentes(self.contenedor_pantallas)

        frame_botones_ventas = ctk.CTkFrame(
            self.contenedor_pantallas,
            border_color='black',
            border_width=2
        )
        frame_botones_ventas.pack()

        boton_registrar_ventas = ctk.CTkButton(
            frame_botones_ventas,
            text="Registrar Ventas",
            command=lambda: self.abrir_ventana_registro_ventas()
        )
        boton_registrar_ventas.pack()

    def abrir_ventana_registro_ventas(self):
        ventana_registro_ventas = ctk.CTkToplevel(self.ventana_principal)

        titulo_ventana_ventas = ctk.CTkLabel(
            ventana_registro_ventas,
            text="REGISTAR VENTA",
            font=('Arial',25,'bold'))
        titulo_ventana_ventas.pack(pady=10,padx=10)

        frame_formulario = ctk.CTkFrame(
            ventana_registro_ventas,
            border_width=2,
            border_color='black'
        )
        frame_formulario.pack(padx=10,pady=10)


        label_fecha = ctk.CTkLabel(
            frame_formulario,
            text='FECHA'
        )
        label_fecha.pack(padx=10,pady=10)

        frame_fecha = ctk.CTkFrame(
        frame_formulario,
        fg_color='transparent'
        )
        frame_fecha.pack(pady=5)

        entry_fecha = ctk.CTkEntry(
            frame_fecha
        )
        entry_fecha.pack(side='left',padx=(0,5))
        
        

        def elegir_fecha():
            ventana_fecha = ctk.CTkToplevel(ventana_registro_ventas)
            ventana_fecha.grab_set()
            resultado = {'fecha':None}
            cal = Calendar(
                ventana_fecha,
                selectmode='day',
                date_pattern='yyyy-mm-dd',
                background="#2B2B2B", 
                foreground="white",
                selectbackground="#1F6AA5", 
                headersbackground="#1F6AA5",
                normalbackground="#2B2B2B", 
                normalforeground="white")
    
            cal.pack(padx=20,pady=20)

            def confirmar():
                resultado['fecha'] = cal.get_date()

                if resultado['fecha']:
                    print(resultado['fecha'])
                    entry_fecha.insert(0,resultado['fecha'])
                    ventana_fecha.destroy()
            
            boton_elegir_fecha = ctk.CTkButton(
                ventana_fecha,
                text='Registrar fecha',
                command=confirmar
            )
            
            boton_elegir_fecha.pack(pady=10,padx=10)


        boton_fecha = ctk.CTkButton(
            frame_fecha,
            text="V",
            command=elegir_fecha,
            fg_color='gray',
            width=3,
            height=3,
            border_width=2,
            border_color='gray'
        )

        boton_fecha.pack(side='left')
        

        label_cliente = ctk.CTkLabel(
            frame_formulario,
            text='CLIENTE'
        )
        label_cliente.pack(padx=10,pady=10)


        clientes = self.logica.obtener_clientes_ordenados_por_nombre_formato_dict()[0]
        clientes_nombres = list(clientes.keys())
        selector_cliente = ctk.CTkComboBox(
            frame_formulario,
            values = clientes_nombres,
            width=150,
            state='readonly'
        )
        selector_cliente.pack(padx=10,pady=10)

        label_referencia = ctk.CTkLabel(
            frame_formulario,
            text='Referencia'
        )
        label_referencia.pack(pady=10,padx=10)

        referencias = self.logica.obtener_referencias_globales()

        entry_referencia = ctk.CTkComboBox(
            frame_formulario,
            values= [referencia[0] for referencia in referencias],
            width=150,
            state='readonly'
        )
        entry_referencia.pack(padx=10,pady=10)




        def recoger_datos():
            #Recoger el id del cliente
            nombre_elegido = selector_cliente.get()
            id_cliente = clientes[nombre_elegido]
            #TODO:completar formulario de pantalla de ventas

        boton_registrar = ctk.CTkButton(
            frame_formulario,
            text="Registrar",
            command=lambda:recoger_datos()
        )
        boton_registrar.pack(padx=10,pady=10)

        
    
    def dibujar_pantalla_deudas(self):
        self.construir_elementos_permanentes(self.contenedor_pantallas)

    def dibujar_pantalla_productos(self):
        self.construir_elementos_permanentes(self.contenedor_pantallas)

    def dibujar_pantalla_analiticas(self):
        self.construir_elementos_permanentes(self.contenedor_pantallas)

  


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

