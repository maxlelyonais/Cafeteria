import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from functools import partial
import sys
import sqlite3 as sql
from kivy.clock import Clock

class WindowManager(ScreenManager):
    pass

class MainScreen(Screen):
    pass

class AddingScreen(Screen):
    pass

class AddingElementsScreen(Screen):
    pass

class AllPedidos(Screen):
    pass

class EditElementsScreen(Screen):
    pass

class ElElementoParaAnyadir(Screen):
    pass

class ElElementoParaEditar(Screen):
    pass

class ElPedidoParaAnyadir(Screen):
    pass

class ElPedidoParaEditar(Screen):
    pass

class ListaPedidosEnMesa(Screen):
    pass

class AddingMasPedidosAMesaScreen(Screen):
    pass



class MyApp(App):
    
    
    button_added = False
    button_pressed = False
    button_connected = False
    def build(self):
        self.createTableElementos()
        self.createTablePedidosAuxiliares()
        self.createTableMesa()
        self.root = Builder.load_file('main.kv')
        self.createContents()
        self.Boton3 = Button(text = "Eliminar Elemento", size_hint_y = 0.1)
        self.BotonVuelta = Button(text = "Volver", size_hint_y = 0.1)
        self.Boton2 = Button(text = "Volver", size_hint_y= 0.1)
        self.Boton4 = Button(text = "Volver", size_hint_y = 0.1)   

        button_grid = self.root.get_screen('AnyadirPedidos').ids.pedidos ## Take into account where are you trying to acces ##
        mesas_grid = self.root.get_screen('Pedidos').ids.mesas
        Pedidos_grid = self.root.get_screen('Adding').ids.TodosPedidos
        Elementos_grid = self.root.get_screen('Elementos').ids.Elementos

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
    
        nombres = self.readRowEnElementos(1)
        imagenesDireccion = self.readRowEnElementos(3)
        TodosLosDatos = self.readRowEnElementos(4)

        for i in range(len(nombres)):

            ## Añadir los diferentes elementos en la pantalla de ELEMENTOS------------------------------------- Finalizado
            boton1 = Button(text = nombres[i][0], background_normal = imagenesDireccion[i][0] )
            boton1.bind(on_release = partial(self.VentanaParaEditar2,TodosLosDatos[i]))
            Elementos_grid.add_widget(boton1)

            ## Añadir los diferentos elementos en la pantalla de Pedidos----------------------------------------- Finalizado

            boton2 = Button(text = nombres[i][0], background_normal = imagenesDireccion[i][0])
            boton2.bind(on_release = partial(self.AnyadirProducto,TodosLosDatos[i]))
            button_grid.add_widget(boton2)

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

        precio.text = str(TodosLosDatos[1])
        imagen.source = TodosLosDatos[2]
        nombre.text = TodosLosDatos[0]

        ## Boton3 Es para la eliminacion de un Elemento
        ## Boton2 Es para la edicion de un Elmeento
        ## Boton4 Es para la vuelta a la pagina anterior
        self.Boton3.bind(on_release = partial(self.Eliminar,1,TodosLosDatos[0]))
        button2 = self.root.get_screen('ElementoEditar').ids.EditarElementos
        button2.bind(on_release = partial(self.EditarElementos,TodosLosDatos[0],str(TodosLosDatos[1]),TodosLosDatos[2]))


    ##Cambiar al numero de Mesa------------------------------------------------------------------------------------------------
    def cambiarAMesa(self,numeroMesa,instance):
        
        self.root.current = 'NumeroMesa'
        elementosDeLaMesa = self.root.get_screen('NumeroMesa').ids.pedidosDeLaMesa
        PedidosEnMesa = self.root.get_screen('AnyadirPedidosAMesa').ids.pedidos

        if not self.button_connected:
            Info = self.readRowEnElementos(4)
            for i in range(len(Info)):
                Boton2 = Button(text = str(Info[i][0]), background_normal = str(Info[i][2]))
                Boton2.bind(on_release = partial(self.anyadirProductoEnMesa,Info[i],numeroMesa))
                PedidosEnMesa.add_widget(Boton2)

        Nombre1 = self.readRowEnPedidosEnMesa(numeroMesa,1)
        Imagen1 = self.readRowEnPedidosEnMesa(numeroMesa,3)
        Cantidad1 = self.readRowEnPedidosEnMesa(numeroMesa,4)
        Precio1 = self.readRowEnPedidosEnMesa(numeroMesa,2)
        Nota1 = self.readRowEnPedidosEnMesa(numeroMesa,5)
        Boton = self.root.get_screen('NumeroMesa').ids.EliminarMesa
        Boton.bind(on_release = lambda instance: self.Eliminar(5,"",numeroMesa))

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

            for i in range(len(Nombre1)):

                boton1 = Button( text = str(Nombre1[i][0]), background_normal = Imagen1[i][0])
                boton1.bind(on_release = partial(self.VentanaParaEditar1,numeroMesa,Nombre1[i][0]))
                Cantidad2 = Label(text = str(Cantidad1[i][0]) )
                Precio2 = Label(text = str(Precio1[i][0]) )
                Notas2 = Label(text = str(Nota1[i][0]))
                totalEnNumero = round(int(Cantidad1[i][0]) * float(Precio1[i][0]))
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
    ## Calcular el Precio total que se obtiene-------------------------------------------------------------------------------------

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
    def VentanaParaEditar1(self,numeroMesa,Nombre,instance):
        self.root.current = 'ElementoEditar'
        Ventana = self.root.get_screen('ElementoEditar').ids.VentanaParaEditar
        CantidadTexto = self.root.get_screen('ElementoEditar').ids.Cantidad1
        CantidadIntroducir = self.root.get_screen('ElementoEditar').ids.Cantidad2  
        NotaTexto = self.root.get_screen('ElementoEditar').ids.Detalles1
        NotaIntroducir = self.root.get_screen('ElementoEditar').ids.Detalles2
        Boton4 = self.root.get_screen('ElementoEditar').ids.Boton4
        Info = self.searchPedidoEnMesa(numeroMesa,1,Nombre,0,0,"")
        
        imagen = self.root.get_screen('ElementoEditar').ids.SelectedImage
        nombre = self.root.get_screen('ElementoEditar').ids.nombreAEditar
        precio = self.root.get_screen('ElementoEditar').ids.precioAEditar

        imagen.source = Info[0][2]
        nombre.text = Info[0][0]
        precio.text = str(Info[0][1])
        CantidadIntroducir.text = str(Info[0][3])
        NotaIntroducir.text = Info[0][4]
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

        Boton4.bind(on_release = lambda instance: self.Eliminar(6,Info[0][0],numeroMesa))
        self.Boton2.bind(on_release= partial(self.cambiarVentana2))
        button2 = self.root.get_screen('ElementoEditar').ids.EditarElementos
        button2.bind(on_release = partial(self.EditarENJSONPedidosEnMesa,numeroMesa,Info[0][3],Info[0][4]))
    
    def EditarENJSONPedidosEnMesa(self,numeroMesa,old_cantidad,Old_Nota,instance):
        CantidadIntroducir = self.root.get_screen('ElementoEditar').ids.Cantidad2
        NotaIntroducir = self.root.get_screen('ElementoEditar').ids.Detalles2
        self.updateFieldsPedidosEnMesa(numeroMesa,CantidadIntroducir.text,old_cantidad,NotaIntroducir.text,Old_Nota)

    ## Editar los elementos------------------------------------------------------------------------ Finalizado
    def EditarElementos(self,oldName,oldPrice,oldImage,instance):

        imagen = self.root.get_screen('ElementoEditar').ids.SelectedImage
        nombre = self.root.get_screen('ElementoEditar').ids.nombreAEditar
        precio = self.root.get_screen('ElementoEditar').ids.precioAEditar

        NewName = nombre.text
        NewPrice = precio.text
        NewImage = imagen.source
        self.updateFieldsElementos(NewName,NewPrice,NewImage,oldName,oldPrice,oldImage)

 ## Hacer que aparezca el nombre, el precio, la foto y despues se guardara lo que se ha escrito en cada uno de los bloques´-------- Finalizado
    def AnyadirProducto(self,Datos,instance):
        self.root.current = 'PedidoAñadir'

        imagen = self.root.get_screen('PedidoAñadir').ids.SelectedImage
        nombre = self.root.get_screen('PedidoAñadir').ids.nombreElemento
        precio = self.root.get_screen('PedidoAñadir').ids.PrecioElemento

        imagen.source = Datos[2]
        nombre.text = Datos[0]
        precio.text = str(Datos[1])

## Guardar un pedido antes de agregarlo en una Mesa
    def guardarJSONPedido(self,instance):
        nombreElemento = self.root.get_screen('PedidoAñadir').ids.nombreElemento
        precioElemento = self.root.get_screen('PedidoAñadir').ids.PrecioElemento
        imagen = self.root.get_screen('PedidoAñadir').ids.SelectedImage
        cantidad = self.root.get_screen('PedidoAñadir').ids.CantidadElemento
        Notas = self.root.get_screen('PedidoAñadir').ids.DetalleACompartir

        ruta = os.getcwd() 
        filename = 'Imagenes'
        ruta1 = os.path.join(ruta,filename)
        ImagenDirect = os.path.join(ruta1,os.path.basename(imagen.source))

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
            self.insertRowEnPedidos(nombreElemento.text,precioElemento.text , ImagenDirect,cantidad.text,Notas.text)
            
## Seleccionar las imagenes que van apareciendo en los selectores
    def select_image(self,number):

        layout = BoxLayout(orientation = 'vertical')
        file = FileChooserIconView()
        file.filters = ['*.png', '*.jpg', '*.jpeg']
        file.path = r''
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

            ruta = os.getcwd()
            file = 'Imagenes'
            destination_file_path = os.path.join(ruta,file,filename)
            

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

    ## Guardar un Elemento a la base de datos------------------------------------------------------------ Finalizado
    def guardarElemento(self):
            
            def cancel(instance):
                Repetido.dismiss()

            nombreElemento = self.root.get_screen('ElementoAñadir').ids.nombreElemento
            precioElemento = self.root.get_screen('ElementoAñadir').ids.precioElemento
            imagen = self.root.get_screen('ElementoAñadir').ids.SelectedImage
            ruta = os.getcwd()
            filename = 'Imagenes'
            ImagenDirect = os.path.join(ruta,filename,os.path.basename(imagen.source))

            if self.searchElemento(nombreElemento.text) == []:
                self.insertRowEnElementos(nombreElemento.text,float(precioElemento.text),ImagenDirect)
            else:
                layout = BoxLayout()
                Mensaje = Label(text = "Elemento ya repetido")
                Boton1 = Button(text = "Volver")
                layout.add_widget(Mensaje)
                layout.add_widget(Boton1)
                
                Repetido = Popup(title= 'Alerta' , content = layout)
                Boton1.bind(on_release = cancel)
                Repetido.open()

    ## 1: Eliminar Elemento
    ## 2: Eliminar todos los elementos
    ## 3: Eliminar Pedido
    ## 4: Eliminar todos los pedidos
    ## 5: Eliminar una Mesa
    ## 6: Eliminar un pedido de una Mesa
    ## 7: Eliminar toda las Mesas
    def Eliminar(self,number,nombreProducto,numeroMesa):
       print(number)
       print(nombreProducto)
       print(numeroMesa)
       if number == 1:
           self.deleteRowElementos(nombreProducto)
           self.root.current = 'Elementos'
       elif number == 2:
           self.deleteEverythingElementos()
       elif number == 3:
            self.deleteRowPedidos(nombreProducto)
            self.root.current = 'Adding'
       elif number == 4:
            self.deleteEverythingPedidos()
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

        imagen.source = info[2]
        nombre.text =  str(info[0])
        precio.text = str(info[1])

        Boton = self.root.get_screen('PedidoAñadir').ids.EditarPedido

        Boton.bind(on_release = partial(self.GuardarElNuevoProducto,numeroMesa))

    def GuardarElNuevoProducto(self,numeroMesa,instance):

        nombreElemento = self.root.get_screen('PedidoAñadir').ids.nombreElemento
        precioElemento = self.root.get_screen('PedidoAñadir').ids.PrecioElemento
        imagen = self.root.get_screen('PedidoAñadir').ids.SelectedImage
        cantidad = self.root.get_screen('PedidoAñadir').ids.CantidadElemento
        Notas = self.root.get_screen('PedidoAñadir').ids.DetalleACompartir


        ruta = os.getcwd()
        filename = 'Imagenes'
        ImagenDirect = os.path.join(ruta,filename,os.path.basename(imagen.source))

        def CerrarVentana(instance):
            Repetido.dismiss()
        
        if self.searchPedidoEnMesa(numeroMesa,1,nombreElemento.text,0,0,"") == []:
            self.insertRowParaPedidoEnMesa(numeroMesa,nombreElemento.text,precioElemento.text,ImagenDirect,cantidad.text,Notas.text)
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
            self.insertRowParaMesa(numero)
            self.createTablePedidosAuxiliaresConNumer(numero)
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

##----------------------------------------------------------------------------------------------------------------------------

    ##---------------------------------------Treat with Elementos DataBase--------------------------------------------------------
    def createTableElementos(self):
        ruta = os.getcwd()
        filename = 'BasesDeDatos'
        databaseName = 'Elementos.db'
        path = os.path.join(ruta,filename,databaseName)
        conn = sql.connect(path)

        cursor = conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS Elementos (
                NombreProducto text,
                PrecioProducto float,
                ImagenDireccion text
            )"""
        )

        conn.commit()
        conn.close()

    def insertRowEnElementos(self,nombreProduct, PrecioProducto, ImagenDireccion):
        ruta = os.getcwd()
        filename = 'BasesDeDatos'
        databaseName = 'Elementos.db'
        path = os.path.join(ruta,filename,databaseName)
        conn = sql.connect(path)
        cursor = conn.cursor()
        instruccion = f"INSERT INTO Elementos VALUES ('{nombreProduct}', {PrecioProducto}, '{ImagenDireccion}')"
        cursor.execute(instruccion)

        conn.commit()
        conn.close()

    ## 1: To read nombreProduct
    ## 2: To read PrecioProduct
    ## 3: To read ImagenDireccion
    ## 4: To read all the information
    def readRowEnElementos(self,number):
        ruta = os.getcwd()
        filename = 'BasesDeDatos'
        databaseName = 'Elementos.db'
        path = os.path.join(ruta,filename,databaseName)
        conn = sql.connect(path)
        cursor = conn.cursor()

        if number == 1:
            instruccion = f"SELECT NombreProducto from Elementos "
        elif number == 2:
            instruccion = f"SELECT PrecioProducto from Elementos "
        elif number == 3:
            instruccion = f"SELECT ImagenDireccion from Elementos"
        elif number == 4:
            instruccion = f"SELECT * from Elementos"
        cursor.execute(instruccion)
        datos = cursor.fetchall()
        conn.commit()
        conn.close()
        return datos

    def searchElemento(self,nombreProducto):
        ruta = os.getcwd()
        filename = 'BasesDeDatos'
        databaseName = 'Elementos.db'
        path = os.path.join(ruta,filename,databaseName)
        conn = sql.connect(path)
        cursor = conn.cursor()
        instruccion = "SELECT * FROM Elementos WHERE NombreProducto LIKE ?"
        cursor.execute(instruccion, ('%'+nombreProducto+'%',))
        datos = cursor.fetchall()
        conn.commit()
        conn.close()
        return datos
        
    ##1: To update name
    ##2: To update price
    def updateFieldsElementos(self,new_name,new_price,new_imageDirection,old_name,old_price,old_imageDirection):
        ruta = os.getcwd()
        filename = 'BasesDeDatos'
        databaseName = 'Elementos.db'
        path = os.path.join(ruta,filename,databaseName)
        conn = sql.connect(path)
        cursor = conn.cursor()
        instruccion1 = f"UPDATE Elementos SET NombreProducto= ? WHERE NombreProducto like ?"
        cursor.execute(instruccion1,(new_name,old_name))
        instruccion2 = f"UPDATE Elementos SET PrecioProducto= ? WHERE PrecioProducto like ?"
        cursor.execute(instruccion2,(new_price,old_price)),
        instruccion3 = f"UPDATE Elementos SET ImagenDireccion= ? WHERE ImagenDireccion like ?"
        cursor.execute(instruccion3,(new_imageDirection,old_imageDirection))
        conn.commit()
        conn.close()

    ## We delete through the name
    def deleteRowElementos(self,nameOfElement):
        ruta = os.getcwd()
        filename = 'BasesDeDatos'
        databaseName = 'Elementos.db'
        path = os.path.join(ruta,filename,databaseName)
        conn = sql.connect(path)
        cursor = conn.cursor()
        instruccion = f"DELETE FROM Elementos WHERE NombreProducto LIKE ?"
        cursor.execute(instruccion, ('%'+nameOfElement+'%',))
        conn.commit()
        conn.close()

    def deleteEverythingElementos(self):
        ruta = os.getcwd()
        filename = 'BasesDeDatos'
        databaseName = 'Elementos.db'
        path = os.path.join(ruta,filename,databaseName)
        conn = sql.connect(path)
        cursor = conn.cursor()
        instruccion = f"DELETE FROM Elementos"
        cursor.execute(instruccion)
        conn.commit()
        conn.close()

    ##------------------------------------------ Treat with Pedidos DataBase----------------------------------------------------

    def createTablePedidosAuxiliares(self):
        ruta = os.getcwd()
        filename = 'BasesDeDatos'
        databaseName = 'PedidosAuxiliares.db'
        path = os.path.join(ruta,filename,databaseName)
        conn = sql.connect(path)
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
    ## Crear un duplicado de PedidoAuxiliar, el cual tendra un numero de mesa correspondiente al cual estara linkeado.
    def createTablePedidosAuxiliaresConNumer(self,numeroMesa):
        ruta = os.getcwd()
        filename = 'BasesDeDatos'
        databaseName = 'PedidosAuxiliares.db'
        path = os.path.join(ruta,filename,databaseName)
        conn = sql.connect(path)
        cursor = conn.cursor()

        NuevaBase = "PedidosAuxiliares" + str(numeroMesa)+ ".db"
        path2 = os.path.join(ruta,filename,NuevaBase)
        print(path2)
        

        instruccion1 = f"ATTACH DATABASE '{path2}' AS new_db"
        cursor.execute(instruccion1)

        instruccion2 = f"CREATE TABLE new_db.PedidosAuxiliares AS SELECT * FROM PedidosAuxiliares"
        cursor.execute(instruccion2)

        instruccion3 = f"DETACH DATABASE new_db"
        cursor.execute(instruccion3)

        conn.commit()
        conn.close()
        self.deleteEverythingPedidos()

    def insertRowEnPedidos(self,nombreProduct, PrecioProducto, ImagenDireccion,cantidadProducto,NotasProducto):
        ruta = os.getcwd()
        filename = 'BasesDeDatos'
        databaseName = 'PedidosAuxiliares.db'
        path = os.path.join(ruta,filename,databaseName)
        conn = sql.connect(path)
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
        ruta = os.getcwd()
        filename = 'BasesDeDatos'
        databaseName = 'PedidosAuxiliares.db'
        path = os.path.join(ruta,filename,databaseName)
        conn = sql.connect(path)
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
        ruta = os.getcwd()
        filename = 'BasesDeDatos'
        databaseName = 'PedidosAuxiliares.db'
        path = os.path.join(ruta,filename,databaseName)
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
        conn.commit()
        conn.close()
        return datos

    ##1: To update cantidadProducto
    ##2: To update notaProducto
    def updateFieldsPedidos(self,new_cantidadProducto,old_cantidadProducto,new_NotasProducto,old_NotasProducto):
        ruta = os.getcwd()
        filename = 'BasesDeDatos'
        databaseName = 'PedidosAuxiliares.db'
        path = os.path.join(ruta,filename,databaseName)
        conn = sql.connect(path)
        cursor = conn.cursor()

        instruccion1 = f"UPDATE PedidosAuxiliares SET cantidadProducto= ? WHERE cantidadProducto like ?"
        cursor.execute(instruccion1,(new_cantidadProducto,old_cantidadProducto))
        instruccion2 = f"UPDATE PedidosAuxiliares SET NotasProducto= ? WHERE NotasProducto like ?"
        cursor.execute(instruccion2,(new_NotasProducto,old_NotasProducto))
        conn.commit()
        conn.close()

    def deleteRowPedidos(self,nameOfElement):
        ruta = os.getcwd()
        filename = 'BasesDeDatos'
        databaseName = 'PedidosAuxiliares.db'
        path = os.path.join(ruta,filename,databaseName)
        conn = sql.connect(path)
        cursor = conn.cursor()
        instruccion = f"DELETE FROM PedidosAuxiliares WHERE NombreProducto = '{nameOfElement}'"
        cursor.execute(instruccion)
        conn.commit()
        conn.close()

    def deleteEverythingPedidos(self):
        ruta = os.getcwd()
        filename = 'BasesDeDatos'
        databaseName = 'PedidosAuxiliares.db'
        path = os.path.join(ruta,filename,databaseName)
        conn = sql.connect(path)
        cursor = conn.cursor()
        instruccion = f"DELETE FROM PedidosAuxiliares"
        cursor.execute(instruccion)
        conn.commit()
        conn.close()

    ##------------------------------------------ Treat with Mesas DataBase---------------------------------------------------------

        ## La creacion de la tabla-----------------------------------------------------------------------------------------------------
    def createTableMesa(self):
        ruta = os.getcwd()
        filename = 'BasesDeDatos'
        dataBaseName = 'ListaDeMesas.db'
        path = os.path.join(ruta,filename,dataBaseName)
        conn = sql.connect(path)
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
        ruta = os.getcwd()
        filename = 'BasesDeDatos'
        dataBaseName = 'ListaDeMesas.db'
        path = os.path.join(ruta,filename,dataBaseName)
        conn = sql.connect(path)
        cursor = conn.cursor()
        instruccion = f"INSERT INTO ListaDeMesas VALUES (?, ?)"
        cursor.execute(instruccion,(numeroMesa,"PedidosAuxiliares" + str(numeroMesa)))
        conn.commit()
        conn.close()

    def insertRowParaPedidoEnMesa(self,numeroMesa,nombreProduct, PrecioProducto, ImagenDireccion,cantidadProducto,NotasProducto):
        datos = self.searchMesa(numeroMesa)
        ruta = os.getcwd()
        filename = 'BasesDeDatos'
        dataBaseName = str(datos[0][1]) + ".db"
        path = os.path.join(ruta,filename,dataBaseName)
        conn = sql.connect(path)

        cursor = conn.cursor()
        instruccion = f"INSERT INTO PedidosAuxiliares VALUES ('{nombreProduct}', {PrecioProducto}, '{ImagenDireccion}',{cantidadProducto},'{NotasProducto}')"
        cursor.execute(instruccion)
        conn.commit()
        conn.close()

    ## 1: para saber el numero de la mesa
    ## 2: para saber el nombre del pedidoAuxiliar

    def readRowMesa(self,numero):
        ruta = os.getcwd()
        filename = 'BasesDeDatos'
        dataBaseName = 'ListaDeMesas.db'
        path = os.path.join(ruta,filename,dataBaseName)
        conn = sql.connect(path)
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
        ruta = os.getcwd()
        filename = 'BasesDeDatos'
        dataBaseName = str(datos[0][1]) + ".db"
        path = os.path.join(ruta,filename,dataBaseName)
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
        ruta = os.getcwd()
        filename = 'BasesDeDatos'
        dataBaseName = 'ListaDeMesas.db'
        path = os.path.join(ruta,filename,dataBaseName)
        conn = sql.connect(path)
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
        ruta = os.getcwd()
        filename = 'BasesDeDatos'
        dataBaseName = str(datos[0][1]) + ".db"
        path = os.path.join(ruta,filename,dataBaseName)
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
        ruta = os.getcwd()
        filename = 'BasesDeDatos'
        dataBaseName = str(datos[0][1]) + ".db"
        path = os.path.join(ruta,filename,dataBaseName)
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
        ruta = os.getcwd()
        filename = 'BasesDeDatos'
        dataBaseName = str(datos[0][1]) + ".db"
        path = os.path.join(ruta,filename,dataBaseName)
        conn = sql.connect(path)
        cursor = conn.cursor()
        instruccion = f"DELETE FROM PedidosAuxiliares WHERE NombreProducto LIKE ?"
        cursor.execute(instruccion, ('%'+nameOfElement+'%',))
        conn.commit()
        conn.close()

    ## Delete one of the Mesa
    def deleteRowMesa(self,numeroMesa):
        print(numeroMesa)
        ruta = os.getcwd()
        filename = 'BasesDeDatos'
        dataBaseName = 'ListaDeMesas.db'
        path = os.path.join(ruta,filename,dataBaseName)
        conn = sql.connect(path)
        cursor = conn.cursor()
        NombrePedidos = self.searchMesa(numeroMesa)
        Nombre = NombrePedidos[0][1]
        print(Nombre)
        path2 = os.path.join(ruta,filename, str(Nombre) + ".db")
        os.remove(path2)
        instruccion = f"DELETE FROM ListaDeMesas WHERE NumeroMesa LIKE ?"
        cursor.execute(instruccion, (numeroMesa,))
        conn.commit()
        conn.close()

    def deleteEverythingMesa(self):
        ruta = os.getcwd()
        filename = 'BasesDeDatos'
        dataBaseName = 'ListaDeMesas.db'
        path = os.path.join(ruta,filename,dataBaseName)
        conn = sql.connect(path)
        cursor = conn.cursor()
        
        NombrePedidos = self.readRowMesa(2)
        for i in NombrePedidos:
            os.remove(str(i[0]) + ".db")

        instruccion = f"DELETE FROM ListaDeMesas"
        cursor.execute(instruccion)
        conn.commit()
        conn.close()

##---------------------------------------------------------------- Used in order to update all the changes--------
if __name__ == '__main__':
    ruta = os.getcwd()
    filename1 = 'BasesDeDatos'
    filename2 = 'Imagenes'
    fileToCheck = '.check'

    ruta1 = os.path.join(ruta,filename1)
    ruta2 = os.path.join(ruta,filename2)
    ruta3 = os.path.join(ruta,fileToCheck)

    if not(os.path.exists(ruta3)):
        os.mkdir(ruta1)
        os.mkdir(ruta2)
        os.mkdir(ruta3)
    MyApp().run()