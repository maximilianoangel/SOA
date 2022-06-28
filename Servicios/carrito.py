import socket, json
from os import system, name
from urllib import response
from db import db

#Enviar transacción
def enviar(sckt, srv, arg):
    if len(srv) < 5 or len(arg) < 1:
        print("Revisar argumentos")
        return
    largo = str(len(arg) + 5)
    while len(largo) < 5:
        largo = '0' + largo
    mensaje_enviado = largo + servicio + arg
    sckt.sendall(mensaje_enviado.encode())

#Armar bus
def escuchar(sckt):
    mensaje = ''
    data = sckt.recv(4096)
    data = data.decode('utf-8')
    tamaño = int(data[:5])
    servicio = data[5:10]
    mensaje += data

    return servicio, mensaje

#Registrar servicio
# def registerS(sckt, srv):
#     enviar(sckt, 'sinit', srv)
#     nS, mT = Bus(sckt)
#     if nS == 'sinit' and mT[:2] == 'OK':
#         print('Servicio activado exitosamente.')
#     else:
#         print('No ha sido posible activar el servicio: ', srv, '.')
#         return




#Agregar productos a la base de datos orden_producto
def agregar_producto(sckt,servicio, data):
    crsr = db.cursor()
    crsr.execute("SELECT * FROM Orden WHERE id_usuario = %s", (data['id_usuario'],))
    respuesta = crsr.fetchall()
    print(respuesta)
    if len(respuesta) == 0:
        crsr = db.cursor()    
        crsr.execute("INSERT INTO Orden (id_usuario,estado,total) VALUES (%s,'por pagar',%s)", (data['id_usuario'],data['subtotal']))
        db.commit()
        crsr = db.cursor()
        crsr.execute("INSERT INTO orden_producto (id_orden, id_producto,cantidad,subtotal) VALUES (%s, %s,%s,%s)", (data['id_orden'], data['id_producto'],data['cantidad'],data['subtotal']))
        db.commit()
    else:
        crsr = db.cursor()
        crsr.execute("UPDATE Orden SET total = total + %s WHERE id_usuario = %s", (data['subtotal'],data['id_usuario']))
        db.commit()
        crsr = db.cursor()
        crsr.execute("INSERT INTO orden_producto (id_orden,id_producto,cantidad,subtotal) VALUES (%s, %s,%s,%s)", (data['id_orden'], data['id_producto'],data['cantidad'],data['subtotal']))
        db.commit()
    response ={"respuesta": "OK"}
    print('Producto agregado a la orden.')
    enviar(sckt, servicio, json.dumps(response))

#Ver productos en stock
def listar_productos(sckt, servicio, data):
    crsr = db.cursor()
    crsr.execute("SELECT * FROM producto")
    respuesta = crsr.fetchall()
    Nrespuesta = {"respuesta": "OK", "productos": respuesta}
    print(Nrespuesta)
    enviar(sckt, servicio, json.dumps(Nrespuesta))


#Ver productos en orden_producto
def ver_productos_orden(sckt, servicio, data):
    crsr = db.cursor()
    crsr.execute("SELECT * FROM `orden_producto` WHERE `id_orden` = %s", (data['id_orden'],))
    respuesta = crsr.fetchall()
    Nrespuesta = {"respuesta": "OK", "productos": respuesta}
    enviar(sckt, servicio, json.dumps(Nrespuesta))


#Ver productos de orden_producto
def ver_productos(sckt, servicio, data):
    crsr = db.cursor()
    crsr.execute("SELECT * FROM `orden_producto` WHERE `id_orden` = %s", (data['id_orden'],))
    respuesta = crsr.fetchall()
    Nrespuesta = {"respuesta": "OK", "productos": respuesta}
    enviar(sckt, servicio, json.dumps(Nrespuesta))


#Elimar uno o mas productos  de la base de datos orden_producto

def eliminar_producto(sckt, servicio, data):
    crsr = db.cursor()
    crsr.execute("DELETE FROM `orden_producto` WHERE `id_orden` = %s AND `id_producto` = %s AND `cantidad` = %s", (data['id_orden'], data['id_producto'], data['cantidad']))
    db.commit()
    response ={"respuesta": "OK"}
    print('Producto eliminado de la orden: ', data['id_producto'])
    enviar(sckt, servicio, json.dumps(response))

##Ver los productos de la base de datos orden_producto
# def ver_productos(id_orden):
#    crsr = db.cursor()
#    crsr.execute("SELECT * FROM `orden_producto` WHERE `id_orden` = %s", (id_orden,))
#    productos = crsr.fetchall()
#    print('Productos de la orden:')
#    for producto in productos:
#        print(producto)
#    return

#Ver productos disponibles de la base de datos producto
# def ver_productos_disponibles():
#     crsr = db.cursor()
#     crsr.execute("SELECT * FROM `producto`")
#     productos = crsr.fetchall()
#     print('Productos disponibles:')
#     for producto in productos:
#         print(producto)
#     return
 
#Añadir el subtotal de un producto segun su cantidad
def subtotal(sckt, servicio, data):
    id = int(data['id_producto'])
    crsr = db.cursor()
    crsr.execute("SELECT precio FROM producto WHERE id_producto = %s", (id,))
    precio = crsr.fetchone()
    subtotal = int(precio[0]) * int(data['cantidad'])
    response ={"respuesta": "OK", "subtotal": subtotal}
    enviar(sckt, servicio, json.dumps(response))


#Buscar id por su nombre en la base de datos producto
def buscar_id_producto(nombre):
    crsr = db.cursor()
    crsr.execute("SELECT id FROM `producto` WHERE `nombre` = %s", (nombre,))
    id_producto = crsr.fetchone()
    return id_producto[0]




if __name__=="__main__":
    servicio = 'bcart'
    try:
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 5000)
        print('Conectandose a {} port {}'.format(*server_address))
        sckt.connect(server_address)
        print('Conectado')
        print('Se está registrando el servicio')
        sckt.send(b'00010sinitbcart')
        print('Servicio registrado')
        data = sckt.recv(4096)
        datos = data.decode('utf-8')
        print(datos)
        largo_transaccion = datos[:5]
        nombre_servicio = datos[5:10]
        status= datos[10:12]
        print('Largo de la transacción: {}'.format(largo_transaccion))
        print('Nombre del servicio: {}'.format(nombre_servicio))
        crsr = db.cursor()
        crsr.execute("SELECT * FROM `usuarios` WHERE `nombre` LIKE 'admin' AND `password` LIKE 'admin'")
        respuesta = crsr.fetchone()
        print(respuesta)
    except:
        print('No se pudo conectar al servidor')
        quit()

    while True:
        servicio, data = escuchar(sckt)
        data = data[10:]
        data=json.loads(data)
        if data['opcion'] == 'agregar':
            agregar_producto(sckt, servicio, data)
        elif data['opcion'] == 'subtotal':
            subtotal(sckt, servicio, data)
        elif data['opcion'] == 'listar':
            listar_productos(sckt, servicio, data)
        elif data['opcion'] == 'listar1':
            ver_productos_orden(sckt, servicio, data)
        elif data['opcion'] == 'eliminar':
            eliminar_producto(sckt, servicio, data)
        else:
            print('Opcion no valida')
            
        