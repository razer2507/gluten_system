
from logic.logic import Logica
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image
from tkcalendar import Calendar
from tkinter import simpledialog

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
            border_width=3,
            width=450,
            height=600
        )
        frame_botones_ventas.pack(side='top',padx=10,pady=10)
        frame_botones_ventas.pack_propagate(False)

        label_titulo_ventas = ctk.CTkLabel(
            frame_botones_ventas,
            text='VENTAS',
            font=('Arial',20,'bold')
        )
        label_titulo_ventas.pack(side='top',pady=10,padx=10)

        boton_registrar_ventas = ctk.CTkButton(
            frame_botones_ventas,
            text="Registrar Ventas",
            font=('Arial',15,'bold'),
            width=300,
            command=lambda: self.abrir_ventana_registro_ventas()
        )
        boton_registrar_ventas.pack(padx=10,pady=10)

    def abrir_ventana_registro_ventas(self):
      
        #TODO: falta completar el registro de la venta
        venta = {
            '''
            'fecha':,
            'cliente_id':,
            'total':,
            'estado':
            '''
        }
        ventana_registro_ventas = ctk.CTkToplevel(self.ventana_principal)

        titulo_ventana_ventas = ctk.CTkLabel(
            ventana_registro_ventas,
            text="REGISTAR VENTA",
            font=('Arial',25,'bold'))
        titulo_ventana_ventas.pack(pady=10,padx=10)

        frame_formulario = ctk.CTkFrame(
            ventana_registro_ventas,
            border_width=2,
            border_color='black',
            height=500,
            width=300
        )
        frame_formulario.pack(padx=10,pady=10)
        frame_formulario.pack_propagate(False)

        label_fecha = ctk.CTkLabel(
            frame_formulario,
            text='FECHA',
            font=('Arial',15,'bold')
        )
        label_fecha.pack(padx=10,pady=10,side='top')

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
            text='CLIENTE',
            font=('Arial',15,'bold')
        )
        label_cliente.pack(padx=10,pady=10,side='top')

        
        clientes = self.logica.obtener_clientes_ordenados_por_nombre_formato_dict()[0]
        clientes_nombres = list(clientes.keys())
        selector_cliente = ctk.CTkComboBox(
            frame_formulario,
            values = clientes_nombres,
            width=150,
            state='readonly'
        )
        selector_cliente.pack(padx=10,pady=10)

        
        label_productos = ctk.CTkLabel(
            frame_formulario,
            text='Productos',
            font=('Arial',15,'bold')
        )
        label_productos.pack()
        frame_productos = ctk.CTkFrame(
        frame_formulario,
        fg_color='transparent'
        )
        frame_productos.pack(pady=5)
        entry_productos = ctk.CTkEntry(
            frame_productos
        )
        entry_productos.pack(side='left',padx=(0,5))
        


        def construir_ticket():
            productos = self.logica.obtener_productos_en_ordenados_por_nombre_formato_dict()
            ticket_venta = {

            }

            ventana_construir_ticket = ctk.CTkToplevel(
                master=ventana_registro_ventas
            )

            #la hacemos modal
            ventana_construir_ticket.grab_set()

            frame_formulario = ctk.CTkFrame(
                ventana_construir_ticket,
                width=400,
                height=600,
                border_color='black',
                border_width=2
            )
            frame_formulario.pack(side='top',pady=10,padx=10)
            frame_formulario.pack_propagate(False)

            label_producto = ctk.CTkLabel(
                frame_formulario,
                text='PRODUCTO',
                font=('Arial',15,'bold')
            )
            label_producto.pack(pady=10,padx=10,side='top')

            entry_producto = ctk.CTkComboBox(
                master=frame_formulario,
                values=list(productos),
                width=300
            )
            entry_producto.pack()

            label_cantidad = ctk.CTkLabel(
                frame_formulario,
                text='CANTIDAD',
                font=('Arial',15,'bold')
            )
            label_cantidad.pack(pady=10,padx=10,side='top')

            
            entry_cantidad = ctk.CTkEntry(
                master=frame_formulario,
                placeholder_text='ingrese cantidad...',
                width=300
            )
            entry_cantidad.pack()
            label_cantidad = ctk.CTkLabel(
                frame_formulario,
                text='CANTIDAD',
                font=('Arial',15,'bold')
            )

            label_precio_unit = ctk.CTkLabel(
                frame_formulario,
                text='PRECIO UNITARIO',
                font=('Arial',15,'bold')
            )

            label_precio_unit.pack(pady=10,padx=10,side='top')

            entry_precio_unit = ctk.CTkEntry(
                master=frame_formulario,
                placeholder_text='ingrese precio unitario...',
                width=300
            )
            entry_precio_unit.pack()

            label_total = ctk.CTkLabel(
                frame_formulario,
                text='TOTAL',
                font=('Arial',15,'bold')
            )

            label_total.pack(pady=10,padx=10,side='top')

            entry_total = ctk.CTkEntry(
                master=frame_formulario,
                placeholder_text='el total se calculara automaticamente...',
                width=300
            )
            entry_total.pack()

            boton_registrar = ctk.CTkButton(
                master=frame_formulario,
                text='REGISTRAR',
                font=('Arial',15,'bold')
            )
            boton_registrar.pack(pady=10,padx=10)
            
            boton_salir = ctk.CTkButton(
                master=frame_formulario,
                text='SALIR',
                font=('Arial',15,'bold'),
                fg_color='red',
                command=lambda:ventana_construir_ticket.destroy()
            )
            boton_salir.pack(pady=10,padx=10)

            def registrar_producto_vendido():
                try:
                    print("funcion ejecutada")
                    id_producto = int(productos[entry_producto.get()])
                    cantidad = int(entry_cantidad.get())
                    precio_unit = float(entry_precio_unit.get())
                    total = cantidad * precio_unit
        
                    validacion = [
                        self.logica.validar_numero(precio_unit),
                        self.logica.validar_numero_entero(cantidad)
                    ]
                    print(validacion)
                    if all(validacion):
                        
                        ticket_venta[id_producto] = {
                            'cantidad':cantidad,
                            'precio_unit':precio_unit,
                            'total':total
                        }
                        boton_registrar.configure(
                            fg_color='green',
                            text='Registrado exitosamente',
                        )
                        entry_cantidad.delete(0,'end')
                        entry_precio_unit.delete(0,'end')



                    else:
                         CTkMessagebox(ventana_construir_ticket,title='ERROR',message='Datos no validados',icon='cancel')
                         boton_registrar.configure(
                            fg_color='red',
                            text='ERROR'
                         )
                except ValueError:
                    CTkMessagebox(ventana_construir_ticket,title='ERROR',message='Datos invalidos',icon='cancel')

            boton_registrar.configure(
                command=registrar_producto_vendido
            )
                    
            

            



        boton_productos = ctk.CTkButton(
            frame_productos,
            text="V",
            command=construir_ticket,
            fg_color='gray',
            width=3,
            height=3,
            border_width=2,
            border_color='gray'
        )

        boton_productos.pack(side='left')
        

        label_estado = ctk.CTkLabel(
            frame_formulario,
            text='Estado',
            font=('Arial',15,'bold')
        )
        label_estado.pack()
        
        estados_pago = self.logica.obtener_estados_de_pago_globales_en_lista()
        selector_estado = ctk.CTkComboBox(
            frame_formulario,
            values = estados_pago,
            width=150,
            state='readonly'
        )
        selector_estado.pack(padx=10,pady=10)
        

        

        def recoger_datos():
            #Recoger el id del cliente
            nombre_elegido = selector_cliente.get()
            id_cliente = clientes[nombre_elegido]

        boton_registrar = ctk.CTkButton(
            frame_formulario,
            text="Registrar",
            command=lambda:recoger_datos
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

