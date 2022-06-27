import json
import socket 

servicio1 = 'sensn'
servicio2 = 'prodt'

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
    * Usuario administrador               *
    *-------------------------------------*
    * Elija una opción:                   *
    * 1) Registrar administracor          *
    * 2) Ingresar usuario administrador   *
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
    tipo = 'admin'

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
        enviar(sckt, servicio1, json.dumps(arg))
        nombre_servicio, mensaje = escuchar(sckt)
        mensaje = json.loads(mensaje[12:])
        if nombre_servicio == servicio1:
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

    arg = {"correo": correo, "password": password, "tipo": "admin", 'opcion': 'login'}
    arg = json.dumps(arg)
    enviar(sckt, servicio1, arg)
    nombre_servicio, mensaje = escuchar(sckt)
    mensaje = json.loads(mensaje[12:])
    if nombre_servicio == servicio1:
        if mensaje["respuesta"] == "ERROR":
            print("No se ha podido iniciar sesión.")
            menu_inicio_sesion() 
        else:
            print("Sesión iniciada con éxito.")
            menu_administrador()

def menu_administrador():
    menu = """
    ***************************************
    * Usuario administrador               *
    *-------------------------------------*
    * Elija una opción:                   *
    * 1) Crear nuevo producto             *
    * 2) Ver listado de productos         *
    * 3) Eliminar productos               *
    ***************************************

    Opción: """
    option = input(menu)
    if option == "1":
        menu_crear_producto()
    elif option == "2":
        menu_listar_productos()
    elif option == "3":
        menu_eliminar_productos()
    else:
        print("Opción ingresada no válida.")
        menu_administrador()

def menu_crear_producto():
    nombre = None
    descripcion = None
    stock = None
    precio = None
    categoria = None

    menu1 = """
    ***************************************
    * Usuario administrador               *
    *-------------------------------------*
    * Crear nuevo producto                *
    * Ingresar nombre del producto        *
    ***************************************

    Nombre: """ 
    nombre = input(menu1)

    menu2 = """
    ***************************************
    * Usuario administrador               *
    *-------------------------------------*
    * Crear nuevo producto                *
    * Ingresar descripción del producto   *
    ***************************************

    Descripción: """ 
    descripcion = input(menu2)

    menu3 = """
    ***************************************
    * Usuario administrador               *
    *-------------------------------------*
    * Crear nuevo producto                *
    * Ingresar precio del producto        *
    ***************************************

    Precio: """ 
    precio = input(menu3)

    menu4 = """
    ***************************************
    * Usuario administrador               *
    *-------------------------------------*
    * Crear nuevo producto                *
    * Ingresar stock del producto         *
    ***************************************

    Stock: """ 
    stock = input(menu4)
    menu5 = f"""
    ***************************************
    * Usuario administrador               *
    *-------------------------------------*
    * Registro de usuario                 *
    * Confirme sus datos [y/n]            *
    ***************************************
    
    Nombre: {nombre}
    Descripcion: {descripcion}
    Precio: {precio}
    Stock: {stock}
    
    Opción: """
    yn = input(menu5)
    yn = yn.lower()
    if yn == 'y' or yn == 'yes' or yn == 's' or yn == 'si':
        arg = {"nombre": nombre, "descripcion": descripcion, "precio": precio, "stock": stock, 'opcion': 'crear'}
        arg = json.dumps(arg)
        enviar(sckt, servicio2, arg)
        nombre_servicio, mensaje = escuchar(sckt)
        mensaje = json.loads(mensaje[12:])
        if nombre_servicio == servicio2:
            if mensaje["respuesta"] == 'OK':
                print("Producto creado con éxito.")
                menu_administrador()
            else:
                print("No se ha podido crear el producto.")
                menu_crear_producto()
    else:
        menu_crear_producto()

def menu_listar_productos():
    arg = {"opcion": "listar"}
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
                ID producto: {i[0]}
                Nombre:{i[1]} 
                Descripcion: {i[2]} 
                Stock: {i[3]}
                Precio: {i[4]}
                -------------------------------------------------""")
            menu_administrador()
        else:
            print("No se ha podido listar los productos.")
            menu_administrador()
    else:
        print("No se ha podido listar los productos.")
        menu_administrador()

def menu_eliminar_productos():
    arg = {"opcion": "listar"}
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
                ID producto: {i[0]}
                Nombre:{i[1]} 
                Descripcion: {i[2]} 
                Stock: {i[3]}
                Precio: {i[4]}
                -------------------------------------------------""")
        else:
            print("No se ha podido listar los productos.")
            menu_administrador()
    else:
        print("No se ha podido listar los productos.")
        menu_administrador()

    menu = """
    ***************************************
    * Usuario administrador               *
    *-------------------------------------*
    * Eliminar productos                  *
    * Ingresar el id del producto         *
    ***************************************

    Id: """ 
    id = input(menu)
    arg = {"id_producto": id, 'opcion': 'eliminar'}
    arg = json.dumps(arg)
    enviar(sckt, servicio2, arg)
    nombre_servicio, mensaje = escuchar(sckt)
    mensaje = json.loads(mensaje[12:])
    if nombre_servicio == servicio2:
        if mensaje["respuesta"] == 'OK':
            print("Producto eliminado con éxito.")
            menu_administrador()
        else:
            print("No se ha encontrado el producto.")
            menu_administrador()
    else:
        print("No se ha podido eliminar el producto.")
        menu_administrador()

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
    

