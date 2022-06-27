import socket, sys, json
from os import system, name
from db import db


servicio1 = 'carri'
servicio2 = 'pagos'

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
        print("Funcion Pagar")
    elif opcion == 4:
        print("Saliendo...")
        sys.exit()
    else:
        print('Opcion no valida')
        menu_cliente()



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
                arg={"opcion": "agregar","id_orden": id_orden, "id_producto": id_producto, "cantidad": cantidad, "subtotal": subtotal, "id_usuario": 1}
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


#            if msg:
#                print(msg)
#
#                enter = input("Presione enter para continuar...")
#                menu_cliente()



if __name__ == "__main__":
    try:
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 5000)
        print('Conectandose a {} port {}'.format(*server_address))
        sckt.connect(server_address)
    except:
        print('No se pudo conectar')
        quit()
    
    menu_cliente()

