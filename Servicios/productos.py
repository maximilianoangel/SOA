import socket
import json
from db import db

def enviar(sckt, servicio, arg):
    if len(servicio) != 5 or len(arg) < 1:
        print("Revisar argumentos")
        return
    largo = str(len(arg) + 5)
    while len(largo) < 5:
        largo = '0' + largo
    mensaje_enviado = largo + servicio + arg
    sckt.sendall(mensaje_enviado.encode())

def escuchar(sckt):
    mensaje = ''
    data = sckt.recv(4096)
    data = data.decode('utf-8')
    tamaño = int(data[:5])
    servicio = data[5:10]
    mensaje += data

    return servicio, mensaje

def crear_producto(sckt, servicio, data):
    crsr = db.cursor()
    crsr.execute("INSERT INTO producto (nombre, descripcion, precio, stock) VALUES (%s, %s, %s, %s)", (data['nombre'], data['descripcion'], data['precio'], data['stock']))
    db.commit()
    response = {"respuesta": "OK"}
    print('Producto creado: ', data['nombre'])
    enviar(sckt, servicio, json.dumps(response))

def listar_productos(sckt, servicio, data):
    crsr = db.cursor()
    crsr.execute("SELECT * FROM producto")
    respuesta = crsr.fetchall()
    Nrespuesta = {"respuesta": "OK", "productos": respuesta}
    enviar(sckt, servicio, json.dumps(Nrespuesta))

def eliminar_producto(sckt, servicio, data):
    crsr = db.cursor()
    crsr.execute("SELECT * FROM producto where id_producto = %s", (data['id_producto']))
    respuesta = crsr.fetchall()
    if respuesta != None:
        crsr = db.cursor()
        crsr.execute("DELETE FROM producto WHERE id_producto = %s", (data['id_producto'],))
        db.commit()
        response = {"respuesta": "OK"}
        print('Producto eliminado: ', data['id_producto'])
        enviar(sckt, servicio, json.dumps(response))
    else:
        response = {"respuesta": "ERROR"}
        print('Producto no encontrado: ', data['id_producto'])
        enviar(sckt, servicio, json.dumps(response))

if __name__ == "__main__":
    servicio = 'prodt'
    try:
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 5000)
        print('Conectandose a {} port {}'.format(*server_address))
        sckt.connect(server_address)
        print('Conectado')
        print('Se está registrando el servicio')
        sckt.send(b'00010sinitprodt')
        data = sckt.recv(4096)
        datos = data.decode('utf-8')
        status = datos[10:12]
        print('Status: {}'.format(status))
        if status != 'OK':
            0/0
        print('Servicio registrado')
    except:
        print('No se pudo conectar')
        quit()
    
    while True:
        servicio, data = escuchar(sckt)
        data = data[10:]
        data = json.loads(data)
        if data['opcion'] == 'crear':
            crear_producto(sckt, servicio, data)
        elif data['opcion'] == 'listar':
            listar_productos(sckt, servicio, data)
        elif data['opcion'] == 'eliminar':
            eliminar_producto(sckt, servicio, data)
        else:
            print('Opción no válida')
            enviar(sckt, servicio, json.dumps({"respuesta": "ERROR"}))
        