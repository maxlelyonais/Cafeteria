import os, pathlib, sys, shutil
import sqlite3 as sql
from functools import partial
import subprocess
import requests
import json
import http.client

# --- dotenv module
# @installation:   pip install python-dotenv
# @version:        python-dotenv==1.0.0
# --- 
from dotenv import load_dotenv

# --- kyvy module
# @installation:   pip install kivy
# @version:        Kivy==2.2.1
#                  Kivy-Garden==0.1.5
# --- 
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen   # ---> !TODO: Irrelevant
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.clock import Clock

# Own package
from module.kivyElements import *


# Constant Variables ----
load_dotenv()


USER_HOME_DIR = os.path.expanduser( '~' )

# Get the absolute path of the python script directory
ABS_SCRIPT_PATH = pathlib.Path(__file__).parent.resolve()

MAIN_KV_PATH = os.path.join(ABS_SCRIPT_PATH, 'main.kv')
DDBB_FOLDER_NAME = os.getenv('DATABASE_FOLDER_NAME')
IMAGE_FOLDER_NAME = os.getenv('IMAGE_FOLDER_NAME')
CHECK_FOLDER_NAME = os.getenv('CHECK_FOLDER_NAME')
CLIENT_FOLDER_NAME = os.getenv('CLIENT_FOLDER_NAME')

# GET ABSOLUTE PATH OF ALL SUB FOLDERS
FOLDER_PATH = [
    os.path.join(ABS_SCRIPT_PATH, DDBB_FOLDER_NAME),
    os.path.join(ABS_SCRIPT_PATH, IMAGE_FOLDER_NAME),

    # Last one always check folder
    os.path.join(ABS_SCRIPT_PATH, CHECK_FOLDER_NAME)
]

# GET ABSOLUTE PATH OF ALL FILES
FILE_PATH = [
    os.path.join(ABS_SCRIPT_PATH, DDBB_FOLDER_NAME, os.getenv('ELEMENT_DB_FILENAME')),
    os.path.join(ABS_SCRIPT_PATH, DDBB_FOLDER_NAME, os.getenv('TABLELIST_DB_FILENAME')),
    os.path.join(ABS_SCRIPT_PATH, DDBB_FOLDER_NAME, os.getenv('ORDER_DB_FILENAME')),
]

#Connect to client

file_path = r"C:\Users\super\OneDrive\Desktop\Cafeteria(Cliente)\Cafeteria\Cafeteria\Client\client.js"
try:
    subprocess.Popen(["node",file_path],shell = True)
except:
    print(f'Failed to open')


# Functions

class MyApp(App):
    
    print(CLIENT_FOLDER_NAME)
    button_added = False
    button_pressed = False
    button_connected = False
    def build(self):
        self.createTablePedidosAuxiliares()
        self.createTableMesa()
        self.root = Builder.load_file(MAIN_KV_PATH)
        self.createContents()
        self.Boton3 = Button(text = "Eliminar Elemento", size_hint_y = 0.1)
        self.BotonVuelta = Button(text = "Volver", size_hint_y = 0.1)
        self.Boton2 = Button(text = "Volver", size_hint_y= 0.1)
        self.Boton4 = Button(text = "Volver", size_hint_y = 0.1)   
        return self.root
    
    def createContents(self):

        button_grid = self.root.get_screen('AnyadirPedidos').ids.pedidos ## Take into account where are you trying to acces ##
        mesas_grid = self.root.get_screen('Pedidos').ids.mesas
        Pedidos_grid = self.root.get_screen('Adding').ids.TodosPedidos
        Elementos_grid = self.root.get_screen('Elementos').ids.Elementos
                                    
        Pedidos = Label(text = "Pedidos")
        Cantidad = Label(text = "Cantidad")
        Nota = Label(text = "Nota")

        Pedidos_grid.add_widget(Pedidos)
        Pedidos_grid.add_widget(Cantidad)
        Pedidos_grid.add_widget(Nota)

    ## Añadir los diferentes Pedidos a la pantalla de Pedidos Totales----------------------------------------------- Finalizado

        nombres = self.readRowEnPedidos(1)
        imagenesDireccion = self.readRowEnPedidos(3)
        Cantidad = self.readRowEnPedidos(4)
        Nota = self.readRowEnPedidos(5)
        TodosLosDatos = self.readRowEnPedidos(6)

        for i in range(len(nombres)):
            boton1 = Button(text = nombres[i][0], background_normal = imagenesDireccion[i][0] )
            boton1.bind(on_release = partial(self.EditarPedido,TodosLosDatos[i]))
            Cantidad1 = Label(text = str(Cantidad[i][0]))
            Nota1 = Label(text = Nota[i][0])
            Pedidos_grid.add_widget(boton1)
            Pedidos_grid.add_widget(Cantidad1)
            Pedidos_grid.add_widget(Nota1)

        Boton = self.root.get_screen('PedidoAñadir').ids.EditarPedido
        Boton.bind(on_release = self.guardarJSONPedido)

    ## Añadir las diferentes Mesas a Todos Los Pedidos---------------------------------------------------------------------------

        NumeroMesas = self.readRowMesa(1)
        for i in range(len(NumeroMesas)):

            boton1 = Button(text = str(NumeroMesas[i][0]))
            boton1.bind(on_release = partial(self.cambiarAMesa,NumeroMesas[i][0]))
            mesas_grid.add_widget(boton1)


## Para actualziar cada una de las ventanas---------------------------------------------------------------------------------------

    def UpdateMesa(self):
        pass
        
    def UpdateElementos(self):
        pass

    def UpdatePedidos(self):
       
        Pedidos_grid = self.root.get_screen('Adding').ids.TodosPedidos
        button_grid = self.root.get_screen('AnyadirPedidos').ids.pedidos

        nombres = self.readRowEnPedidos(1)
        imagenesDireccion = self.readRowEnPedidos(3)
        Cantidad = self.readRowEnPedidos(4)
        Nota = self.readRowEnPedidos(5)
        TodosLosDatos = self.readRowEnPedidos(6)

        for widget in Pedidos_grid.children[:]:  # Create a copy of the children list to avoid modification during iteration
            Pedidos_grid.remove_widget(widget)

        for widget in button_grid.children[:]:
            button_grid.remove_widget(widget)

        for i in range(len(nombres)):
            boton1 = Button(text = nombres[i][0], background_normal = imagenesDireccion[i][0] )
            boton1.bind(on_release = partial(self.EditarPedido,TodosLosDatos[i]))
            Cantidad1 = Label(text = str(Cantidad[i][0]))
            Nota1 = Label(text = Nota[i][0])
            Pedidos_grid.add_widget(boton1)
            Pedidos_grid.add_widget(Cantidad1)
            Pedidos_grid.add_widget(Nota1)

        for i in range(len(nombres)):
            boton2 = Button(text = nombres[i][0], background_normal = imagenesDireccion[i][0])
            boton2.bind(on_release = partial(self.AnyadirProducto,TodosLosDatos[i]))
            button_grid.add_widget(boton2)

        Boton = self.root.get_screen('PedidoAñadir').ids.EditarPedido
        Boton.bind(on_release = self.guardarJSONPedido)

    def UpdateBotones(self):
        pass

## Retrieve/Send data from/To the server-------------------------------------------------------------------------------------

    def retrieve_dataElementos(self,numeroMesa):
        try:
            response = requests.get('http://localhost:3000/api/Elementos')
            if response.status_code == 200:

                Elementos_grid = self.root.get_screen('Elementos').ids.Elementos
                button_grid = self.root.get_screen('AnyadirPedidos').ids.pedidos
                PedidosEnMesa = self.root.get_screen('AnyadirPedidosAMesa').ids.pedidos
                for widget in Elementos_grid.children[:]:  # Create a copy of the children list to avoid modification during iteration
                    Elementos_grid.remove_widget(widget)

                for widget in button_grid.children[:]:
                    button_grid.remove_widget(widget)

                for widget in PedidosEnMesa.children[:]:  # Create a copy of the children list to avoid modification during iteration
                    PedidosEnMesa.remove_widget(widget)

                data = response.json()
                for i in data:

                    ## Añadir los diferentes elementos en la pantalla de ELEMENTOS------------------------------------- Finalizado
                    boton1 = Button(text = i["NombreProducto"], background_normal = i["ImagenDireccion"] )
                    boton1.bind(on_release = partial(self.VentanaParaEditar2,i))
                    Elementos_grid.add_widget(boton1)

                    ## Añadir los diferentes elementos en la pantalla de Pedidos
                    boton2 = Button(text = i["NombreProducto"], background_normal = i["ImagenDireccion"])
                    boton2.bind(on_release = partial(self.AnyadirProducto,i))
                    button_grid.add_widget(boton2)

                    Boton2 = Button(text = str(i["NombreProducto"]), background_normal = str(i["ImagenDireccion"]))
                    Boton2.bind(on_release = partial(self.anyadirProductoEnMesa,i,numeroMesa))
                    PedidosEnMesa.add_widget(Boton2)

            else:
                print(f"HTTP Error {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"Request Error: {str(e)}")
        except ValueError as e:
            print(f"JSON Parsing Error: {str(e)}")

    def send_dataElementos(self):

        try:
            response = requests.get('http://localhost:3000/api/Elementos')
            if response.status_code == 200:
                data = response.json()
            else:
                print(f"HTTP Error {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {str(e)}")
        except ValueError as e:
            print(f"JSON Parsing Error: {str(e)}")
            
        def cancel(instance):
            Repetido.dismiss()

        Repetido = False

        nombreElemento = self.root.get_screen('ElementoAñadir').ids.nombreElemento
        precioElemento = self.root.get_screen('ElementoAñadir').ids.precioElemento
        imagen = self.root.get_screen('ElementoAñadir').ids.SelectedImage

        if(imagen.source == ''):
            imagen.source = 'Cafe.png'
        ImagenDirect = os.path.join(FOLDER_PATH[1], os.path.basename(imagen.source))

        for i in data:
            if nombreElemento.text == i["NombreProducto"]:
                Repetido = True

        if Repetido == False:

            try:
                resultado = float(precioElemento.text)
                params = {
                "NombreProducto": str(nombreElemento.text),
                "PrecioProducto": resultado,
                "ImagenDireccion": str(ImagenDirect)}
            except:
                params = {
                "NombreProducto": str(nombreElemento.text),
                "PrecioProducto": 0.0,
                "ImagenDireccion": str(ImagenDirect)
                }

            response = requests.get('http://localhost:3000/api/updateElemento',params = params)

            if response.status_code == 200:
                print("Request was successful.")
                print(response.text)
            else:
                print("Request failed with status code:", response.status_code)
                print("Response content:", response.text)
            imagen = self.root.get_screen('ElementoAñadir').ids.SelectedImage

            try:
                with open(ImagenDirect, 'rb') as source_file:
                    imagen_bits = source_file.read()
                    files = {'imagen': (imagen.source, imagen_bits, 'application/octet-stream')}
                
                response = requests.post('http://localhost:3000/upload/images', files=files)
            except Exception as e:
                print("An error occurred:", e)
            
        else:
            layout = BoxLayout()
            Mensaje = Label(text = "Elemento ya repetido")
            Boton1 = Button(text = "Volver")
            layout.add_widget(Mensaje)
            layout.add_widget(Boton1)
                
            Repetido = Popup(title= 'Alerta' , content = layout)
            Boton1.bind(on_release = cancel)
            Repetido.open()

    def delete_dataElementos(self,nombreProducto):
        params = {
            "NombreEliminar" : nombreProducto,
        }
        response = requests.get('http://localhost:3000/api/deleteElemento',params = params)


    def delete_dataAllElementos(self):
        requests.get('http://localhost:3000/api/deleteAllElementos')

    def send_dataMesa(self,number):
        
        conn = sql.connect(FILE_PATH[2])
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM PedidosAuxiliares')

        rows = cursor.fetchall()
        data = [
            {
                "id": number
            }
        ]

        for row in rows:
            record = {
                "NombreProducto": row[0],
                "PrecioProducto": row[1],
                "ImagenDireccion": row[2],
                "CantidadProducto": row[3],
                "NotasProducto": row[4]
            }

            data.append(record)

        json_data = json.dumps(data, indent = 4)
        conn.close()
        headers = {'content-type':'application/json'}

        response = requests.post('http://localhost:3000/upload/Pedidos',data = json_data,headers = headers)

        if response.status_code == 200:
            print('Request was successful')
        else:
            print('Request failed')


    def delete_dataMesa(self,numeroMesa):

        params = {
            "NumeroMesa": numeroMesa,
        }
        response = requests.get('http://localhost:3000/api/deleteMesa', params = params)

    def send_onedataPedidos(self,numeroMesa,nombreElemento,precioElemento,ImagenDirect, cantidad,Notas):

        try:
            resultado = float(precioElemento)
            params = {
            "NumeroMesa": numeroMesa,
            "NombreProducto": str(nombreElemento),
            "PrecioProducto": resultado,
            "CantidadProducto": str(cantidad),
            "ImagenDireccion": str(ImagenDirect),
            "NotasProducto": str(Notas)
            }
        except:
            params = {
            "NumeroMesa": numeroMesa,
            "NombreProducto": str(nombreElemento),
            "PrecioProducto": 0.0,
            "CantidadProducto": str(cantidad),
            "ImagenDireccion": str(ImagenDirect),
            "NotasProducto": str(Notas)
            }
        response = requests.get('http://localhost:3000/api/addPedido', params = params)

        if response.status_code == 200:
            print('Request was successful')
        else:
            print('Request failed')
        

    def send_dataPedidos(self,numeroMesa,Producto,instance):
         
        imagen = self.root.get_screen('ElementoEditar').ids.SelectedImage

        if(imagen.source == ''):
            imagen.source = 'Cafe.png'
        ImagenDirect = os.path.join(FOLDER_PATH[1], os.path.basename(imagen.source))

        CantidadIntroducir = self.root.get_screen('ElementoEditar').ids.Cantidad2  
        NotaIntroducir = self.root.get_screen('ElementoEditar').ids.Detalles2
        nombre = self.root.get_screen('ElementoEditar').ids.nombreAEditar
        precio = self.root.get_screen('ElementoEditar').ids.precioAEditar

        try:
            resultado = float(precio.text)
            params = {
            "NombrePrevio": str(Producto["NombreProducto"]),
            "NumeroMesa": numeroMesa,
            "NombreProducto": str(nombre.text),
            "PrecioProducto": resultado,
            "CantidadProducto": str(CantidadIntroducir.text),
            "ImagenDireccion": str(ImagenDirect),
            "NotasProducto": str(NotaIntroducir.text)
            }
        except:
            params = {
            "NombrePrevio": str(Producto["NombreProducto"]),
            "NumeroMesa": numeroMesa,
            "NombreProducto": str(nombre.text),
            "PrecioProducto": 0.0,
            "CantidadProducto": str(CantidadIntroducir.text),
            "ImagenDireccion": str(ImagenDirect),
            "NotasProducto": str(NotaIntroducir.text)
            }
        response = requests.get('http://localhost:3000/api/editPedido', params = params)

        if response.status_code == 200:
            print('Request was successful')
        else:
            print('Request failed')

    def delete_dataPedidos(self,numeroMesa,NombreProducto):
        params = {

            "NumeroMesa": numeroMesa,
            "NombreProducto": NombreProducto
        }

        response = requests.get('http://localhost:3000/api/deletePedido', params = params)

    def send_editElemento(self,nombrePrevio,instance):
        try:
            response = requests.get('http://localhost:3000/api/Elementos')
            if response.status_code == 200:
                data = response.json()
            else:
                print(f"HTTP Error {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {str(e)}")
        except ValueError as e:
            print(f"JSON Parsing Error: {str(e)}")
            
        def cancel(instance):
            Repetido.dismiss()

        Repetido = False

        imagen = self.root.get_screen('ElementoEditar').ids.SelectedImage
        nombreElemento = self.root.get_screen('ElementoEditar').ids.nombreAEditar
        precioElemento = self.root.get_screen('ElementoEditar').ids.precioAEditar

        if(imagen.source == ''):
            imagen.source = 'Cafe.png'
        ImagenDirect = os.path.join(FOLDER_PATH[1], os.path.basename(imagen.source))

        for i in data:
            if nombreElemento.text == i["NombreProducto"]:
                Repetido = True

        if Repetido == False:

            try:
                resultado = float(precioElemento.text)
                params = {
                "NombrePrevio": str(nombrePrevio),
                "NombreProducto": str(nombreElemento.text),
                "PrecioProducto": resultado,
                "ImagenDireccion": str(ImagenDirect)}
            except:
                params = {
                "NombrePrevio": str(nombrePrevio),
                "NombreProducto": str(nombreElemento.text),
                "PrecioProducto": 0.0,
                "ImagenDireccion": str(ImagenDirect)
                }

            response = requests.get('http://localhost:3000/api/editElemento',params = params)
            imagen = self.root.get_screen('ElementoAñadir').ids.SelectedImage

            try:
                with open(ImagenDirect, 'rb') as source_file:
                    imagen_bits = source_file.read()
                    files = {'imagen': (imagen.source, imagen_bits, 'application/octet-stream')}
                
                response = requests.post('http://localhost:3000/upload/images', files=files)
            except Exception as e:
                print("An error occurred:", e)
            
        else:
            layout = BoxLayout()
            Mensaje = Label(text = "Elemento ya repetido")
            Boton1 = Button(text = "Volver")
            layout.add_widget(Mensaje)
            layout.add_widget(Boton1)
                
            Repetido = Popup(title= 'Alerta' , content = layout)
            Boton1.bind(on_release = cancel)
            Repetido.open()

    def delete_allMesa(self):
        requests.get('http://localhost:3000/api/deleteAllMesa')

    def retrieve_dataPedidos(self,numeroMesa):
        try:
            params =[
                {
            "NumeroMesa": numeroMesa
                },
            ]

            response = requests.post('http://localhost:3000/api/Pedidos', json = params)

            if response.status_code == 200:
                result_data = response.json()
                print(result_data)
                return result_data
            else:
                print(f"HTTP Error {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"Request Error: {str(e)}")
        except ValueError as e:
            print(f"JSON Parsing Error: {str(e)}")

    def retrieve_dataMesas(self):
        try:
            response = requests.get('http://localhost:3000/api/Mesas')

            mesas_grid = self.root.get_screen('Pedidos').ids.mesas
            for widget in mesas_grid.children[:]:  # Create a copy of the children list to avoid modification during iteration
                mesas_grid.remove_widget(widget)

            for i in response.json():
                boton1 = Button(text = str(i["NumeroMesa"]))
                boton1.bind(on_release = partial(self.cambiarAMesa,i["NumeroMesa"]))
                mesas_grid.add_widget(boton1)

        except requests.exceptions.RequestException as e:
            print(f"Request Error: {str(e)}")
        except ValueError as e:
            print(f"JSON Parsing Error: {str(e)}")

    def retrieve_imagenes(self,imageName):
        try:
            response = requests.get(f'http://localhost:3000/download/{imageName}')

            if response.status_code == 200:
                PATH = os.path.join(FOLDER_PATH[1],imageName)
                with open(PATH, 'wb') as f:
                    f.write(response.content)
            else:
                print('Error')
        except requests.exceptions.RequestException as req_err:
            print(f'Request Error: {req_err}')

##Editar Cosas---------------------------------------------------------------------------------------------------------

     ## Ventana para la edicion de los elementos
    def VentanaParaEditar2(self,TodosLosDatos,instance):
    
        self.root.current = 'ElementoEditar'
        Ventana = self.root.get_screen('ElementoEditar').ids.VentanaParaEditar

        CantidadTexto = self.root.get_screen('ElementoEditar').ids.Cantidad1
        CantidadIntroducir = self.root.get_screen('ElementoEditar').ids.Cantidad2  
        NotaTexto = self.root.get_screen('ElementoEditar').ids.Detalles1
        NotaIntroducir = self.root.get_screen('ElementoEditar').ids.Detalles2
        Boton4 = self.root.get_screen('ElementoEditar').ids.Boton4
    
        imagen = self.root.get_screen('ElementoEditar').ids.SelectedImage
        nombre = self.root.get_screen('ElementoEditar').ids.nombreAEditar
        precio = self.root.get_screen('ElementoEditar').ids.precioAEditar
        self.Boton4.bind(on_release= self.cambiarVentana3)

        if not self.button_pressed:
            ## Elimina los widgets no necesario para la pantalla de Editar los Elementos-----------------------------------------
            Ventana.remove_widget(CantidadTexto)
            Ventana.remove_widget(CantidadIntroducir)
            Ventana.remove_widget(NotaTexto)
            Ventana.remove_widget(Boton4)
            Ventana.remove_widget(NotaIntroducir)
            Ventana.remove_widget(self.Boton2)

            Ventana.add_widget(self.Boton4)
            Ventana.add_widget(self.Boton3)
            self.button_pressed = True

        precio.text = str(TodosLosDatos["PrecioProducto"])
        imagen.source = TodosLosDatos["ImagenDireccion"]
        nombre.text = TodosLosDatos["NombreProducto"]

        ## Boton3 Es para la eliminacion de un Elemento
        ## Boton2 Es para la edicion de un Elmento
        ## Boton4 Es para la vuelta a la pagina anterior
        self.Boton3.bind(on_release = partial(self.Eliminar,1,TodosLosDatos["NombreProducto"]))
        button2 = self.root.get_screen('ElementoEditar').ids.EditarElementos
        button2.bind(on_release = partial(self.send_editElemento,TodosLosDatos["NombreProducto"]))


    ##Cambiar al numero de Mesa------------------------------------------------------------------------------------------------
    def cambiarAMesa(self,numeroMesa,instance):
        
        datos = self.retrieve_dataPedidos(numeroMesa)
        self.retrieve_dataElementos(numeroMesa)
        self.root.current = 'NumeroMesa'
        elementosDeLaMesa = self.root.get_screen('NumeroMesa').ids.pedidosDeLaMesa
        

        Boton = self.root.get_screen('NumeroMesa').ids.EliminarMesa
        Boton.bind(on_release = lambda instance: self.delete_dataMesa(numeroMesa))

        if not self.button_added:

            NombreProducto = Label(text = "Nombre del Producto")
            Cantidad = Label( text = "Cantidad")
            Precio = Label(text = "Precio")
            Nota = Label(text = "Notas")
            TotalPrecio = Label(text = "Total Precio")

            elementosDeLaMesa.add_widget(NombreProducto)
            elementosDeLaMesa.add_widget(Cantidad)
            elementosDeLaMesa.add_widget(Precio)
            elementosDeLaMesa.add_widget(Nota)
            elementosDeLaMesa.add_widget(TotalPrecio)

            for i in datos:

                boton1 = Button( text = str(i["NombreProducto"]), background_normal = str(i["ImagenDireccion"]))
                boton1.bind(on_release = partial(self.VentanaParaEditar1,numeroMesa,i["NombreProducto"],i))
                Cantidad2 = Label(text = str(i["CantidadProducto"])) 
                Precio2 = Label(text = str(i["PrecioProducto"])) 
                Notas2 = Label(text = str(i["NotasProducto"]))
                totalEnNumero = round(i["PrecioProducto"] * i["CantidadProducto"])
                total = Label(text =str(totalEnNumero))

                elementosDeLaMesa.add_widget(boton1)
                elementosDeLaMesa.add_widget(Cantidad2)
                elementosDeLaMesa.add_widget(Precio2)
                elementosDeLaMesa.add_widget(Notas2)
                elementosDeLaMesa.add_widget(total)

            elementosDeLaMesa.do_layout()
            self.button_added = True


    def EditarPedido(self,Datos,instance):
        self.root.current = 'PedidoAñadir'
        Ventana = self.root.get_screen('PedidoAñadir').ids.Box

        nombreElemento = self.root.get_screen('PedidoAñadir').ids.nombreElemento
        precioElemento = self.root.get_screen('PedidoAñadir').ids.PrecioElemento
        imagen = self.root.get_screen('PedidoAñadir').ids.SelectedImage
        cantidad = self.root.get_screen('PedidoAñadir').ids.CantidadElemento
        Notas = self.root.get_screen('PedidoAñadir').ids.DetalleACompartir
        Boton2 = self.root.get_screen('PedidoAñadir').ids.Volver2

        imagen.source = Datos[2]
        nombreElemento.text = Datos[0]
        precioElemento.text = str(Datos[1])
        cantidad.text = str(Datos[3])
        Notas.text = Datos[4]

        Boton = self.root.get_screen('PedidoAñadir').ids.EditarPedido
        BotonEliminar = Button( text = "Eliminar", size_hint_y = 0.1)

        if not self.button_added:
            Ventana.add_widget(BotonEliminar)
            self.button_added = True

        Boton.text = "Editar"
        Boton.unbind(on_release = self.guardarJSONPedido)
        Boton2.bind(on_release = self.cambiarVentana4)
        Boton.bind( on_release = partial(self.EditarPedidos,str(Datos[3]),Datos[4]))
        BotonEliminar.bind(on_release = partial(self.Eliminar,3,Datos[0]))
        Ventana.do_layout()
    ## Calcular el Precio total que se obtiene----------------------------------------------------------------------------------------------------------------------

    def calcularElTotal(self):

        total = 0
        last_column_values = []
        cantidadElementos = 0

        for child in reversed(self.root.get_screen('NumeroMesa').ids.pedidosDeLaMesa.children):

            if isinstance(child,Label):

                index = self.root.get_screen('NumeroMesa').ids.pedidosDeLaMesa.children.index(child)

                if index % 5 == 0:

                    if cantidadElementos != 0:
                        last_column_values.append(child.text)
                    else:
                        cantidadElementos+=1

        for i in last_column_values:
            total+= float(i)

        cantidad = self.root.get_screen('NumeroMesa').ids.AnyadirExtra
        cantidadTotal = self.root.get_screen('NumeroMesa').ids.totalCantidad

        try:
            cantidadFloat = float(cantidad.text)
            total+=cantidadFloat

            if total < 0:
                cantidadTotal.text = "El total es un numero invalido"
            else:
                cantidadTotal.text = "El total es: " + str(total)

        except:
            cantidad.text = "Por favor introduce un numero correcto"

    ## Editar uno de los Pedidos que se encuentran antes de añadirlo a Mesa
    def EditarPedidos(self,old_cantidad,old_notas,instance):
        
        cantidad = self.root.get_screen('PedidoAñadir').ids.CantidadElemento
        Notas = self.root.get_screen('PedidoAñadir').ids.DetalleACompartir
        self.updateFieldsPedidos(cantidad.text,old_cantidad,Notas.text,old_notas)

    ##Ventana para la edicion de los pedidos de una Mesa
    def VentanaParaEditar1(self,numeroMesa,Nombre,TodosLosDatos,instance):
        self.root.current = 'ElementoEditar'
        Ventana = self.root.get_screen('ElementoEditar').ids.VentanaParaEditar
        CantidadTexto = self.root.get_screen('ElementoEditar').ids.Cantidad1
        CantidadIntroducir = self.root.get_screen('ElementoEditar').ids.Cantidad2  
        NotaTexto = self.root.get_screen('ElementoEditar').ids.Detalles1
        NotaIntroducir = self.root.get_screen('ElementoEditar').ids.Detalles2
        Boton4 = self.root.get_screen('ElementoEditar').ids.Boton4
        
        imagen = self.root.get_screen('ElementoEditar').ids.SelectedImage
        nombre = self.root.get_screen('ElementoEditar').ids.nombreAEditar
        precio = self.root.get_screen('ElementoEditar').ids.precioAEditar

        imagen.source = TodosLosDatos["ImagenDireccion"]
        nombre.text = TodosLosDatos["NombreProducto"]
        precio.text = str(TodosLosDatos["PrecioProducto"])
        CantidadIntroducir.text = str(TodosLosDatos["CantidadProducto"])
        NotaIntroducir.text = TodosLosDatos["NotasProducto"]
        precio.readonly = True
        nombre.readonly = True

        if not self.Boton2 in Ventana.children:
            Ventana.add_widget(self.Boton2)

        if self.button_pressed:
            Ventana.add_widget(CantidadTexto)
            Ventana.add_widget(CantidadIntroducir)
            Ventana.add_widget(NotaTexto)
            Ventana.add_widget(NotaIntroducir)
            Ventana.add_widget(Boton4)

            ## Eliminar los widgets que no son necesarios para la edicion de un elemento en un Pedido
            Ventana.remove_widget(self.Boton4)
            Ventana.remove_widget(self.Boton3)
            self.button_pressed = False

        Boton4.bind(on_release = lambda instance: self.delete_dataPedidos(numeroMesa,TodosLosDatos["NombreProducto"]))
        self.Boton2.bind(on_release= partial(self.cambiarVentana2))
        button2 = self.root.get_screen('ElementoEditar').ids.EditarElementos
        button2.bind(on_release = partial(self.send_dataPedidos,numeroMesa,TodosLosDatos))
    
    def EditarENJSONPedidosEnMesa(self,numeroMesa,old_cantidad,Old_Nota,instance):
        CantidadIntroducir = self.root.get_screen('ElementoEditar').ids.Cantidad2
        NotaIntroducir = self.root.get_screen('ElementoEditar').ids.Detalles2
        self.updateFieldsPedidosEnMesa(numeroMesa,CantidadIntroducir.text,old_cantidad,NotaIntroducir.text,Old_Nota)


 ## Hacer que aparezca el nombre, el precio, la foto y despues se guardara lo que se ha escrito en cada uno de los bloques´-------- Finalizado
    def AnyadirProducto(self,Datos,instance):
        self.root.current = 'PedidoAñadir'
        imagen = self.root.get_screen('PedidoAñadir').ids.SelectedImage
        nombre = self.root.get_screen('PedidoAñadir').ids.nombreElemento
        precio = self.root.get_screen('PedidoAñadir').ids.PrecioElemento

        imagen.source = Datos["ImagenDireccion"]
        nombre.text = Datos["NombreProducto"]
        precio.text = str(Datos["PrecioProducto"])

## Guardar un pedido antes de agregarlo en una Mesa
    def guardarJSONPedido(self,instance):
        nombreElemento = self.root.get_screen('PedidoAñadir').ids.nombreElemento
        precioElemento = self.root.get_screen('PedidoAñadir').ids.PrecioElemento
        imagen = self.root.get_screen('PedidoAñadir').ids.SelectedImage
        cantidad = self.root.get_screen('PedidoAñadir').ids.CantidadElemento
        Notas = self.root.get_screen('PedidoAñadir').ids.DetalleACompartir

        ImagenDirect = os.path.join(FOLDER_PATH[1], os.path.basename(imagen.source))

        def CerrarVentana(instance):
            Repetido.dismiss()

        if self.searchPedido(1,nombreElemento.text,"","","") != []:
            layout = BoxLayout()
            Cerrar = Button(text = "Cerrar")
            Texto = Label(text = "Elemento ya repetido")
            
            layout.add_widget(Cerrar)
            layout.add_widget(Texto)
            Repetido = Popup(title= 'Alerta' , content = layout)
            Cerrar.bind(on_release= CerrarVentana)
            Repetido.open()

        else:
            self.insertRowEnPedidos(nombreElemento.text, precioElemento.text, ImagenDirect,
                                    cantidad.text if cantidad.text.isnumeric() else 1,
                                    Notas.text)
            
## Seleccionar las imagenes que van apareciendo en los selectores
    def select_image(self,number):

        layout = BoxLayout(orientation = 'vertical')
        file = FileChooserIconView()
        file.filters = ['*.png', '*.jpg', '*.jpeg']
        file.path = USER_HOME_DIR
        Select = Button(text = "Select" , size_hint = (1,0.3))
        Cancel = Button(text = "Cancel", size_hint = (1,0.3))

        layout.add_widget(file)
        layout.add_widget(Select)
        layout.add_widget(Cancel)

        def on_cancel(instance):
            popup.dismiss()

            nombreElemento = self.root.get_screen('ElementoAñadir').ids.nombreElemento
            precioElemento = self.root.get_screen('ElementoAñadir').ids.precioElemento
            imagen = self.root.get_screen('ElementoAñadir').ids.SelectedImage

            nombreElemento.text = "Escribe el nombre del producto"
            precioElemento.text = "Escribe el precio del producto"
            imagen.source = ""

        def on_select(instance):
            popup.dismiss()
            selected_file = file.selection[0]
            filename = os.path.basename(selected_file)

            selected_image(selected_file , filename)

        def selected_image(path2,filename):

            if number == 1:
                imagen = self.root.get_screen('ElementoAñadir').ids.SelectedImage
            elif number == 2:
                imagen = self.root.get_screen('ElementoEditar').ids.SelectedImage
                
            imagen.source = path2
            with open(imagen.source,'rb') as source_file:
                image_data = source_file.read()

            destination_file_path = os.path.join(FOLDER_PATH[1], filename)
            
            with open(destination_file_path,'wb') as destination_file:
                destination_file.write(image_data)

        popup = Popup( title= 'Selecciona una imagen', content = layout, size_hint = (1,1) ) 
        Cancel.bind(on_release = on_cancel)
        Select.bind(on_release = on_select)

        popup.open()

    ## Restablecer las diversas Ventanas
        #1 Es para restablecer la ventana de añadir elemento
        #2 Restablece la ventana de añadir Pedidos a la Mesa
    def restablecer(self,number):

            if number == 1:
                nombreElemento = self.root.get_screen('ElementoAñadir').ids.nombreElemento
                precioElemento = self.root.get_screen('ElementoAñadir').ids.precioElemento
                imagen = self.root.get_screen('ElementoAñadir').ids.SelectedImage

                nombreElemento.text = "Escribe el nombre del producto"
                precioElemento.text = "Escribe el precio del producto"
                imagen.source = ""

            elif number == 2:
                cantidad = self.root.get_screen('PedidoAñadir').ids.CantidadElemento
                Nota = self.root.get_screen('PedidoAñadir').ids.DetalleACompartir

                cantidad.text = "Escribe la cantidad a desear"
                Nota.text = "Escribe alguna nota importante"

    ## 1: Eliminar Elemento
    ## 2: Eliminar todos los elementos
    ## 3: Eliminar Pedido
    ## 4: Eliminar todos los pedidos
    ## 5: Eliminar una Mesa
    ## 6: Eliminar un pedido de una Mesa
    ## 7: Eliminar toda las Mesas
    def Eliminar(self,number,nombreProducto,numeroMesa):
       if number == 1:
           self.delete_dataElementos(nombreProducto)
           self.UpdateElementos()
           self.root.current = 'Elementos'
       elif number == 2:
           self.deleteEverythingElementos()
           self.UpdateElementos()
       elif number == 3:
            self.deleteRowPedidos(nombreProducto)
            self.UpdatePedidos()
            self.root.current = 'Adding'
       elif number == 4:
            self.deleteEverythingPedidos()
            self.UpdatePedidos()
       elif number == 5:
           self.deleteRowMesa(numeroMesa)
           self.root.current = 'Pedidos'
       elif number == 6:
            self.deleteRowPedidoEnMesa(numeroMesa,nombreProducto)
            self.root.current = 'NumeroMesa'
       elif number == 7:
           self.deleteEverythingMesa()
       
    def anyadirProductoEnMesa(self,info,numeroMesa,instance):
        self.root.current = 'PedidoAñadir'
        imagen = self.root.get_screen('PedidoAñadir').ids.SelectedImage
        nombre = self.root.get_screen('PedidoAñadir').ids.nombreElemento
        precio = self.root.get_screen('PedidoAñadir').ids.PrecioElemento

        imagen.source = info["ImagenDireccion"]
        nombre.text =  str(info["NombreProducto"])
        precio.text = str(info["PrecioProducto"])

        Boton = self.root.get_screen('PedidoAñadir').ids.EditarPedido
        Boton.bind(on_release = partial(self.GuardarElNuevoProducto,numeroMesa))

    def GuardarElNuevoProducto(self,numeroMesa,instance):

        nombreElemento = self.root.get_screen('PedidoAñadir').ids.nombreElemento
        precioElemento = self.root.get_screen('PedidoAñadir').ids.PrecioElemento
        imagen = self.root.get_screen('PedidoAñadir').ids.SelectedImage
        cantidad = self.root.get_screen('PedidoAñadir').ids.CantidadElemento
        Notas = self.root.get_screen('PedidoAñadir').ids.DetalleACompartir

        ImagenDirect = os.path.join(FOLDER_PATH[1], os.path.basename(imagen.source))

        Pedidos = self.retrieve_dataPedidos(numeroMesa)
        Repetido = False

        def CerrarVentana(instance):
            Repetido.dismiss()
        
        for i in Pedidos:
            if i["NombreProducto"] == nombreElemento:
                Repetido = True

        if Repetido == False:
            self.send_onedataPedidos(numeroMesa,nombreElemento.text,precioElemento.text,ImagenDirect, 
                                           cantidad.text if cantidad.text.isnumeric() else 1,
                                           Notas.text)
        else:
            layout = BoxLayout()
            Cerrar = Button(text = "Cerrar")
            Texto = Label(text = "Elemento ya repetido")
            
            layout.add_widget(Cerrar)
            layout.add_widget(Texto)
            Repetido = Popup(title= 'Alerta' , content = layout)
            Cerrar.bind(on_release= CerrarVentana)
            Repetido.open()

    def check_number(self):
        NumeroMesa = self.root.get_screen('Adding').ids.NumeroMesa
        resultado = self.root.get_screen('Adding').ids.resultado
       
        try:
            number = int(NumeroMesa.text)
            MesaExistente = False

            if number < 0 or MesaExistente == True:
                resultado.text = "Introduce un numero de Mesa que no sea negativo o que no esté repetido"
            else:
                resultado.text = "Mesa añadido"
                self.guardarMesa()

        except ValueError:
            resultado.text = "Introduce un numero de Mesa valido"

    def guardarMesa(self):
        NumeroMesa = self.root.get_screen('Adding').ids.NumeroMesa
        numero = NumeroMesa.text

        def cancel(instance):
            Repetido.dismiss()

        if self.searchMesa(numero) == []:
            self.send_dataMesa(numero)
        else:
            layout = BoxLayout()
            Mensaje = Label(text = "Elemento ya repetido")
            Boton1 = Button(text = "Volver")
            layout.add_widget(Mensaje)
            layout.add_widget(Boton1)
                
            Repetido = Popup(title= 'Alerta' , content = layout)
            Boton1.bind(on_release = cancel)
            Repetido.open()

##------------------------------------------------------------- Cambiar las ventanas de manera manual------------------------------
    def cambiarVentana1(self,instance):
        self.root.current = 'AnyadirPedidosAMesa'

    
    def cambiarVentana2(self,instance):

        self.root.current = 'NumeroMesa'

    def cambiarVentana3(self,instance):

        self.root.current = 'Elementos'

    def cambiarVentana4(self,instance):
        self.root.current = 'Adding'

##------------------------------------------------------------ Actualizar las Ventanas----------------------------------------------
    def actualizarVentana(self):
        self.stop()
        python = sys.executable
        os.execl(python, python, *sys.argv)

    ##------------------------------------------ Treat with Pedidos DataBase----------------------------------------------------

    def createTablePedidosAuxiliares(self):
        
        conn = sql.connect(FILE_PATH[2])
        cursor = conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS PedidosAuxiliares (
                NombreProducto text,
                PrecioProducto float,
                ImagenDireccion text,
                CantidadProducto integer,
                NotasProducto text

            )"""
        )

        conn.commit()
        conn.close()

    def insertRowEnPedidos(self,nombreProduct, PrecioProducto, ImagenDireccion,cantidadProducto,NotasProducto):
        
        conn = sql.connect(FILE_PATH[2])
        cursor = conn.cursor()
        instruccion = f"INSERT INTO PedidosAuxiliares VALUES ('{nombreProduct}', {PrecioProducto}, '{ImagenDireccion}',{cantidadProducto},'{NotasProducto}')"
        cursor.execute(instruccion)

        conn.commit()
        conn.close()

    ## 1: To read nombreProduct
    ## 2: To read PrecioProduct
    ## 3: To read ImagenDireccion
    ## 4: To read QuantityProduct
    ## 5: To read NoteProduct
    ## 6: To read all the information
    def readRowEnPedidos(self,number):
        
        conn = sql.connect(FILE_PATH[2])
        cursor = conn.cursor()

        if number == 1:
            instruccion = f"SELECT NombreProducto from PedidosAuxiliares "
        elif number == 2:
            instruccion = f"SELECT PrecioProducto from PedidosAuxiliares "
        elif number == 3:
            instruccion = f"SELECT ImagenDireccion from PedidosAuxiliares"
        elif number == 4:
            instruccion = f"Select cantidadProducto from PedidosAuxiliares"
        elif number == 5:
            instruccion = f"Select NotasProducto from PedidosAuxiliares"
        elif number == 6:
            instruccion = f"Select * from PedidosAuxiliares"
            
        cursor.execute(instruccion)
        datos = cursor.fetchall()
        conn.commit()
        conn.close()
        return datos

    ## 1: Search by name
    ## 2: Search by price
    ## 3: Search by quantity
    ## 4: Search by Notes
    def searchPedido(self,number,nombreProduct,priceProduct,QuantityProduct,NoteProduct):
        
        conn = sql.connect(FILE_PATH[2])
        cursor = conn.cursor()

        if number == 1:
            instruccion = f"SELECT * from PedidosAuxiliares WHERE NombreProducto = '{nombreProduct}'"
        elif number == 2:
            instruccion = f"SELECT * from PedidosAuxiliares WHERE PrecioProducto = {priceProduct}"
        elif number == 3:
            instruccion = f"SELECT * from PedidosAuxiliares WHERE cantidadProducto = {QuantityProduct}"
        elif number == 4:
            instruccion = f"SELECT * from PedidosAuxiliares WHERE NotasProducto = '{NoteProduct}'"

        cursor.execute(instruccion)
        datos = cursor.fetchall()
        conn.commit()
        conn.close()
        return datos

    ##1: To update cantidadProducto
    ##2: To update notaProducto
    def updateFieldsPedidos(self,new_cantidadProducto,old_cantidadProducto,new_NotasProducto,old_NotasProducto):
        
        conn = sql.connect(FILE_PATH[2])
        cursor = conn.cursor()

        instruccion1 = f"UPDATE PedidosAuxiliares SET cantidadProducto= ? WHERE cantidadProducto like ?"
        cursor.execute(instruccion1,(new_cantidadProducto,old_cantidadProducto))
        instruccion2 = f"UPDATE PedidosAuxiliares SET NotasProducto= ? WHERE NotasProducto like ?"
        cursor.execute(instruccion2,(new_NotasProducto,old_NotasProducto))
        conn.commit()
        conn.close()

    def deleteRowPedidos(self,nameOfElement):
        
        conn = sql.connect(FILE_PATH[2])
        cursor = conn.cursor()
        instruccion = f"DELETE FROM PedidosAuxiliares WHERE NombreProducto = '{nameOfElement}'"
        cursor.execute(instruccion)
        conn.commit()
        conn.close()

    def deleteEverythingPedidos(self):
        
        conn = sql.connect(FILE_PATH[2])
        cursor = conn.cursor()
        instruccion = f"DELETE FROM PedidosAuxiliares"
        cursor.execute(instruccion)
        conn.commit()
        conn.close()

    ##------------------------------------------ Treat with Mesas DataBase---------------------------------------------------------

        ## La creacion de la tabla-----------------------------------------------------------------------------------------------------
    def createTableMesa(self):
        
        conn = sql.connect(FILE_PATH[1])
        cursor = conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS ListaDeMesas (
                NumeroMesa integer,
                NameOfAnotherDataBase text
            )"""
        )
        conn.commit()
        conn.close()

    def insertRowParaMesa(self,numeroMesa):
        
        conn = sql.connect(FILE_PATH[1])
        cursor = conn.cursor()
        instruccion = f"INSERT INTO ListaDeMesas VALUES (?, ?)"
        cursor.execute(instruccion,(numeroMesa,"PedidosAuxiliares" + str(numeroMesa)))
        conn.commit()
        conn.close()

    def insertRowParaPedidoEnMesa(self,numeroMesa,nombreProduct, PrecioProducto, ImagenDireccion,cantidadProducto,NotasProducto):
        datos = self.searchMesa(numeroMesa)
        
        filename = 'BasesDeDatos'
        dataBaseName = str(datos[0][1]) + ".db"
        path = os.path.join(ABS_SCRIPT_PATH,filename,dataBaseName)
        conn = sql.connect(path)

        cursor = conn.cursor()
        instruccion = f"INSERT INTO PedidosAuxiliares VALUES ('{nombreProduct}', {PrecioProducto}, '{ImagenDireccion}',{cantidadProducto},'{NotasProducto}')"
        cursor.execute(instruccion)
        conn.commit()
        conn.close()

    ## 1: para saber el numero de la mesa
    ## 2: para saber el nombre del pedidoAuxiliar

    def readRowMesa(self,numero):
        
        conn = sql.connect(FILE_PATH[1])
        cursor = conn.cursor()
        if numero == 1:
            instruccion = f"SELECT NumeroMesa from ListaDeMesas"
        elif numero == 2:
            instruccion = f"SELECT NameOfAnotherDataBase from ListaDeMesas"
        elif numero == 3:
            instruccion = f"Select * from ListaDeMesas"
        cursor.execute(instruccion)
        datos = cursor.fetchall()
        conn.commit()
        conn.close()
        return datos
    
    ## 1: To read nombreProduct
    ## 2: To read PrecioProduct
    ## 3: To read ImagenDireccion
    ## 4: To read QuantityProduct
    ## 5: To read NoteProduct
    ## 6: To read all the information
    def readRowEnPedidosEnMesa(self,numeroMesa,number):
        datos = self.searchMesa(numeroMesa)
        
        filename = 'BasesDeDatos'
        dataBaseName = str(datos[0][1]) + ".db"
        path = os.path.join(ABS_SCRIPT_PATH,filename,dataBaseName)
        conn = sql.connect(path)
        cursor = conn.cursor()
        if number == 1:
            instruccion = f"SELECT NombreProducto from PedidosAuxiliares"
        elif number == 2:
            instruccion = f"SELECT PrecioProducto from PedidosAuxiliares"
        elif number == 3:
            instruccion = f"SELECT ImagenDireccion from PedidosAuxiliares"
        elif number == 4:
            instruccion = f"Select cantidadProducto from PedidosAuxiliares"
        elif number == 5:
            instruccion = f"Select NotasProducto from PedidosAuxiliares"
        elif number == 6:
            instruccion = f"Select * from PedidosAuxiliares"

        cursor.execute(instruccion)
        datos = cursor.fetchall()
        conn.commit()
        conn.close()
        return datos

    def searchMesa(self,numeroMesa):
        
        conn = sql.connect(FILE_PATH[1])
        cursor = conn.cursor()
        instruccion = "SELECT * FROM ListaDeMesas WHERE NumeroMesa LIKE ?"
        cursor.execute(instruccion, (numeroMesa,))
        datos = cursor.fetchall()
        conn.commit()
        conn.close()
        return datos
    
    ## 1: Search by name
    ## 2: Search by price
    ## 3: Search by quantity
    ## 4: Search by Notes
    def searchPedidoEnMesa(self,numeroMesa,number,nombreProduct,priceProduct,QuantityProduct,NoteProduct):
        datos = self.searchMesa(numeroMesa)
        
        filename = 'BasesDeDatos'
        dataBaseName = str(datos[0][1]) + ".db"
        path = os.path.join(ABS_SCRIPT_PATH,filename,dataBaseName)
        conn = sql.connect(path)
        cursor = conn.cursor()

        if number == 1:
            instruccion = f"SELECT * from PedidosAuxiliares WHERE NombreProducto = '{nombreProduct}'"
        elif number == 2:
            instruccion = f"SELECT * from PedidosAuxiliares WHERE PrecioProducto = {priceProduct}"
        elif number == 3:
            instruccion = f"SELECT * from PedidosAuxiliares WHERE cantidadProducto = {QuantityProduct}"
        elif number == 4:
            instruccion = f"SELECT * from PedidosAuxiliares WHERE NotasProducto = '{NoteProduct}'"

        cursor.execute(instruccion)
        datos = cursor.fetchall()
        print(datos)
        conn.commit()
        conn.close()
        return datos
    
    def updateFieldsPedidosEnMesa(self,numeroMesa,new_cantidadProducto,old_cantidadProducto,new_NotasProducto,old_NotasProducto):
        datos = self.searchMesa(numeroMesa)
        
        filename = 'BasesDeDatos'
        dataBaseName = str(datos[0][1]) + ".db"
        path = os.path.join(ABS_SCRIPT_PATH,filename,dataBaseName)
        conn = sql.connect(path)
        cursor = conn.cursor()
        instruccion1 = f"UPDATE PedidosAuxiliares SET cantidadProducto= ? WHERE cantidadProducto like ?"
        cursor.execute(instruccion1,(new_cantidadProducto,old_cantidadProducto))
        instruccion2 = f"UPDATE PedidosAuxiliares SET NotasProducto= ? WHERE NotasProducto like ?"
        cursor.execute(instruccion2,(new_NotasProducto,old_NotasProducto))
        conn.commit()
        conn.close()
        
    ## We delete through the name
    def deleteRowPedidoEnMesa(self,numeroMesa,nameOfElement):
        datos = self.searchMesa(numeroMesa)
        
        filename = 'BasesDeDatos'
        dataBaseName = str(datos[0][1]) + ".db"
        path = os.path.join(ABS_SCRIPT_PATH,filename,dataBaseName)
        conn = sql.connect(path)
        cursor = conn.cursor()
        instruccion = f"DELETE FROM PedidosAuxiliares WHERE NombreProducto LIKE ?"
        cursor.execute(instruccion, ('%'+nameOfElement+'%',))
        conn.commit()
        conn.close()

    ## Delete one of the Mesa
    def deleteRowMesa(self,numeroMesa):
        
        conn = sql.connect(FILE_PATH[1])
        cursor = conn.cursor()
        NombrePedidos = self.searchMesa(numeroMesa)

        if(NombrePedidos != []):
            Nombre = NombrePedidos[0][1]

            print(Nombre)
            path2 = os.path.join(FOLDER_PATH[0], str(Nombre) + ".db")
            os.remove(path2)
            instruccion = f"DELETE FROM ListaDeMesas WHERE NumeroMesa LIKE ?"
            cursor.execute(instruccion, (numeroMesa,))
            conn.commit()
            conn.close()

    def deleteEverythingMesa(self):
        
        conn = sql.connect(FILE_PATH[1])
        cursor = conn.cursor()
        
        NombrePedidos = self.readRowMesa(2)
        for i in NombrePedidos:
            os.remove(os.path.join(FOLDER_PATH[0], str(i[0]) + ".db"))

        instruccion = f"DELETE FROM ListaDeMesas"
        cursor.execute(instruccion)
        conn.commit()
        conn.close()

##--------- Used in order to update all the changes --------
if __name__ == '__main__':
    
    if sys.argv.__len__() == 1:
        # Create the folder where the data will be stored
        if not(os.path.exists(FOLDER_PATH[FOLDER_PATH.__len__()-1])):
            for i in range(FOLDER_PATH.__len__()):
                os.mkdir(FOLDER_PATH[i]) if not(os.path.exists(FOLDER_PATH[i])) else None


        # Application().run()
        MyApp().run()
    
    else: 
        if sys.argv[1] == 'reset':
            for i in range(FOLDER_PATH.__len__()):
                shutil.rmtree(FOLDER_PATH[i]) if os.path.exists(FOLDER_PATH[i]) else None