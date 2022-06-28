import json
import socket
from os import system, name

servicio1 = 'carri'
servicio2 = 'bcart'
servicio3= 'pagar'
servicio4='sensn'
ID_usuario = ''
Total =0

def enviar(sckt, servicio, arg):
    if len(servicio) < 5 or len(arg) < 1:
        print("Revisar argumentos")
        return
    lT = str(len(arg) + 5)
    while len(lT) < 5:
        lT = '0' + lT
    T = lT + servicio + arg
    sckt.sendall(T.encode())

def escuchar(sckt):
    mensaje = ''
    data = sckt.recv(4096)
    data = data.decode('utf-8')
    tamaño = int(data[:5])
    servicio = data[5:10]
    mensaje += data

    return servicio, mensaje

def menu_inicial():
    menu = """
    ***************************************
    * Usuario Cliente                     *
    *-------------------------------------*
    * Elija una opción:                   *
    * 1) Registrar usuario                *
    * 2) Ingresar usuario                 *
    ***************************************

    Opción: """
    option = input(menu)
    if option == "1":
        menu_registro_usuario()
    elif option =="2":
        menu_inicio_sesion()
    else:
        print("Opción ingresada no válida.")
        menu_inicial()

def menu_registro_usuario():
    nombre = None
    correo = None
    password = None
    tipo = 'cliente'

    menu1 = """
    ***************************************
    * Usuario administrador               *
    *-------------------------------------*
    * Registro de usuario                 *
    * Ingresar nombre de usuario          *
    ***************************************

    Usuario: """ 
    nombre = input(menu1)

    menu2 = """
    ***************************************
    * Usuario administrador               *
    *-------------------------------------*
    * Registro de correo                  *
    * Ingresar su correo                  *
    ***************************************

    Correo: """ 
    correo = input(menu2)

    menu2 = """
    ***************************************
    * Usuario administrador               *
    *-------------------------------------*
    * Registro de usuario                 *
    * Ingresar contraseña                 *
    ***************************************
    
    Contraseña: """
    password = input(menu2)

    menu3 = f"""
    ***************************************
    * Usuario administrador               *
    *-------------------------------------*
    * Registro de usuario                 *
    * Confirme sus datos [y/n]            *
    ***************************************
    
    Usuario: {nombre}
    Correo: {correo}
    Contraseña: {password}
    
    Opción: """
    yn = input(menu3)
    yn = yn.lower()
    if yn == 'y' or yn == 'yes' or yn == 's' or yn == 'si':
        arg = {"nombre": nombre, "correo": correo, "password": password, 'saldo': '0', 'tipo': tipo, 'opcion': 'registrar' }
        enviar(sckt, servicio4, json.dumps(arg))
        nombre_servicio, mensaje = escuchar(sckt)
        mensaje = json.loads(mensaje[12:])
        if nombre_servicio == servicio4:
            if mensaje["respuesta"] == 'OK':
                print("Usuario registrado con éxito.")
                menu_inicial()
            else:
                print("No se ha podido registrar el usuario.")
                menu_registro_usuario()
    else:
        menu_registro_usuario()

def menu_inicio_sesion():
    correo = None
    password = None
    global ID_usuario

    menu1 = """
    ***************************************
    * Usuario administrador               *
    *-------------------------------------*
    * Inicio de sesión                    *
    * Ingresar su correo                  *
    ***************************************

    Usuario: """   
    correo = input(menu1)

    menu2 = """
    ***************************************
    * Usuario administrador               *
    *-------------------------------------*
    * Inicio de sesión                    *
    * Ingresar contraseña                 *
    ***************************************
    
    Contraseña: """
    password = str(input(menu2))

    arg = {"correo": correo, "password": password, "tipo": "cliente", 'opcion': 'login'}
    arg = json.dumps(arg)
    enviar(sckt, servicio4, arg)
    nombre_servicio, mensaje = escuchar(sckt)
    mensaje = json.loads(mensaje[12:])
    if nombre_servicio == servicio4:
        print(mensaje)
        if mensaje["respuesta"] == "ERROR":
            print("No se ha podido iniciar sesión.")
            menu_inicio_sesion() 
        else:
            arg = {"correo": correo, "tipo": "cliente", 'opcion': 'id'}
            arg = json.dumps(arg)
            enviar(sckt, servicio4, arg)
            nombre_servicio, mensaje = escuchar(sckt)
            mensaje = json.loads(mensaje[12:])
            ID_usuario = mensaje["id"]
            print("Sesión iniciada con éxito.")
            menu_cliente()

#Crear menu cliente agregar carrito y eliminar carrito
def menu_cliente():
    menCl = """
    *********************************************************
    *Modo usuario                                           *
    *-------------------------------------------------------*
    *1. Agregar producto a carrito                          *
    *2. Eliminar producto de carrito                        *
    *3. Pagar                                               *
    *-------------------------------------------------------*
    *4. Salir                                               *
    *********************************************************
    
    Opcion: """
    opcion=int(input(menCl))
    if opcion == 1:
        menu_listar_productos()
    elif opcion == 2:
        menu_eliminar_productos_carrito()
    elif opcion == 3:
        realizar_pago()
    elif opcion == 4:
        print("Saliendo...")
    elif opcion == 5:
        global Total
        Total=100
        realizar_pago()
    else:
        print('Opcion no valida')
        menu_cliente()


def realizar_pago():
    global ID_usuario
    global Total
    productos=[]
    cantidad=[]
    arg = {"opcion": "listar1"}
    arg = json.dumps(arg)
    enviar(sckt, servicio2, arg)
    nombre_servicio, mensaje = escuchar(sckt)
    mensaje = json.loads(mensaje[12:])
    if nombre_servicio == servicio2:
        if mensaje["respuesta"] == 'OK':
            for i in mensaje["productos"]:
                productos.append(int(i[0]))
                cantidad.append(int(i[3]))
        else:
            print("Carrito vacio")
            menu_cliente()
    arg={"id":ID_usuario,"pago":Total,"producto":productos,"cantidad":cantidad}
    enviar(sckt, servicio3, arg)
    nombre_servicio, mensaje = escuchar(sckt)
    mensaje = json.loads(mensaje[12:])
    if mensaje["respuesta"] == 'Pago realizado con exito!':
        print("Pago realizado con exito")
    else:
        print("No se pudo completar el pago")


def menu_listar_productos():
    arg = {"opcion": "listar"}
    arg = json.dumps(arg)
    enviar(sckt, servicio2, arg)
    nombre_servicio, mensaje = escuchar(sckt)
    mensaje = json.loads(mensaje[12:])
    if nombre_servicio == servicio2:
        print(mensaje)
        if mensaje["respuesta"] == 'OK':
            print("Listado de productos:")
            for i in mensaje["productos"]:
                print(f"""
                -------------------------------------------------
                ID producto: {i[0]}
                Nombre:{i[1]} 
                Descripcion: {i[2]} 
                Stock: {i[3]}
                Precio: {i[4]}
                -------------------------------------------------""")
            menu_agregar_producto()
        else:
            print("No se ha podido listar los productos.")
            menu_cliente()
    else:
        print("No se ha podido listar los productos.")
        menu_cliente()

def menu_agregar_producto():
    id_orden = 1
    id_producto = None
    cantidad = None
    subtotal = 0
    global Total
    global ID_usuario

    menu1 = """
    *********************************************************
    *Modo usuario                                           *
    *-------------------------------------------------------*
    *Ingresar ID producto                                   *
    *********************************************************
    ID_producto: """
    id_producto = input(menu1)

    menu2 = """
    *********************************************************
    *Modo usuario                                           *
    *-------------------------------------------------------*
    *Ingresar cantidad                                      *
    *********************************************************
    Cantidad: """
    cantidad = input(menu2)

    menu3 = f"""
    *********************************************************
    *Modo usuario                                           *
    *-------------------------------------------------------*
    *Confirme sus datos                                     *
    *********************************************************
    
    ID_producto: {id_producto}
    Cantidad: {cantidad}

    Opcion: """
    yn = input(menu3)
    yn=yn.lower()
    if yn == 'si':
        arg =  {"opcion": "subtotal", "id_producto": id_producto, "cantidad": cantidad}
        arg = json.dumps(arg)
        enviar(sckt, servicio2, arg)
        nombre_servicio, mensaje = escuchar(sckt)
        mensaje = json.loads(mensaje[12:])
        if nombre_servicio == servicio2:
            if mensaje["respuesta"] == 'OK':
                print("Subtotal: ", mensaje["subtotal"])
                subtotal=mensaje["subtotal"]
                Total=Total+int(subtotal)
                arg={"opcion": "agregar","id_orden": id_orden, "id_producto": id_producto, "cantidad": cantidad, "subtotal": subtotal, "id_usuario": int(ID_usuario)}
                arg = json.dumps(arg)
                enviar(sckt, servicio2, arg)
                nombre_servicio, mensaje = escuchar(sckt)
                mensaje = json.loads(mensaje[12:])
                if nombre_servicio == servicio2:
                    if mensaje["respuesta"] == 'OK':
                        print("Producto agregado al carrito.")
                        menu_cliente()
                    else:
                        print("No se ha podido agregar el producto al carrito.")
                        menu_agregar_producto()
            else:
                print("No se ha podido calcular el subtotal.")
                menu_agregar_producto()
                return
        else:
            print("No se ha podido calcular el subtotal.")
            menu_agregar_producto()
            


def menu_eliminar_productos_carrito():
    arg = {"opcion": "listar1"}
    arg = json.dumps(arg)
    enviar(sckt, servicio2, arg)
    nombre_servicio, mensaje = escuchar(sckt)
    mensaje = json.loads(mensaje[12:])
    if nombre_servicio == servicio2:
        if mensaje["respuesta"] == 'OK':
            print("Listado de productos:")
            for i in mensaje["productos"]:
                print(f"""
                -------------------------------------------------
                ID : {i[0]}
                ID Orden:{i[1]} 
                ID Producto: {i[2]} 
                Cantidad: {i[3]}
                Subtotal: {i[4]}
                -------------------------------------------------""")
        else:
            print("No se ha podido listar los productos.")
            menu_cliente()
    else:
        print("No se ha podido listar los productos.")
        menu_cliente()

    id_orden=1
    menu = """
    *********************************************************
    *Modo usuario                                           *
    *-------------------------------------------------------*
    * Ingresar ID producto a eliminar                       *
    *********************************************************
    ID_producto: """
    id_producto = input(menu)

    menu1 = """
    *********************************************************
    *Modo usuario                                           *
    *-------------------------------------------------------*
    *Ingrese cantidad a eliminar                            *
    
    Cantidad: """
    cantidad = input(menu1)
    arg = {"opcion": "eliminar","id_orden":id_orden ,"id_producto": id_producto, "cantidad": cantidad}
    arg = json.dumps(arg)
    enviar(sckt, servicio2, arg)
    nombre_servicio, mensaje = escuchar(sckt)
    mensaje = json.loads(mensaje[12:])
    if nombre_servicio == servicio2:
        if mensaje["respuesta"] == 'OK':
            print("Producto eliminado del carrito.")
            menu_cliente()
        else:
            print("No se ha podido eliminar el producto del carrito.")
            menu_eliminar_productos_carrito()
    else:
        print("No se ha podido eliminar el producto del carrito.")
        menu_eliminar_productos_carrito()
    
if __name__ == "__main__":
    try:
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 5000)
        print('Cliente: Conectandose a {} puerto {}'.format(*server_address))
        sckt.connect(server_address)
    except: 
        print('No es posible la conexión al bus')
        quit()
    menu_inicial()