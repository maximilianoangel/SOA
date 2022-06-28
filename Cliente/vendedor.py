import json
import socket 

servicio1 = 'sensn'

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
    * Usuario Vendedor                    *
    *-------------------------------------*
    * Elija una opción:                   *
    * 1) Registrar vendedor               *
    * 2) Ingresar usuario vendedor        *
    ***************************************

    Opción: """
    option = input(menu)
    if option == "1":
        menu_registro_vendedor()
    elif option =="2":
        menu_inicio_sesion()
    else:
        print("Opción ingresada no válida.")
        menu_inicial()

def menu_registro_vendedor():
    nombre = None
    correo = None
    password = None
    tipo = 'vendedor'

    menu1 = """
    ***************************************
    * Usuario vendedor                    *
    *-------------------------------------*
    * Registro de usuario                 *
    * Ingresar nombre de usuario          *
    ***************************************

    Usuario: """ 
    nombre = input(menu1)

    menu2 = """
    ***************************************
    * Usuario vendedor                    *
    *-------------------------------------*
    * Registro de correo                  *
    * Ingresar su correo                  *
    ***************************************

    Correo: """ 
    correo = input(menu2)

    menu2 = """
    ***************************************
    * Usuario vendedor                    *
    *-------------------------------------*
    * Registro de usuario                 *
    * Ingresar contraseña                 *
    ***************************************
    
    Contraseña: """
    password = input(menu2)

    menu3 = f"""
    ***************************************
    * Usuario vendedor                    *
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
                menu_registro_vendedor()
    else:
        menu_registro_vendedor()

def menu_inicio_sesion():
    correo = None
    password = None

    menu1 = """
    ***************************************
    * Usuario vendedor                    *
    *-------------------------------------*
    * Inicio de sesión                    *
    * Ingresar su correo                  *
    ***************************************

    Usuario: """   
    correo = input(menu1)

    menu2 = """
    ***************************************
    * Usuario vendedor                    *
    *-------------------------------------*
    * Inicio de sesión                    *
    * Ingresar contraseña                 *
    ***************************************
    
    Contraseña: """
    password = str(input(menu2))

    arg = {"correo": correo, "password": password, "tipo": "vendedor", 'opcion': 'login'}
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
            menu_vendedor()

def menu_vendedor():
    pass

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