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

def login(sckt, servicio, data):
    crsr = db.cursor()
    crsr.execute("SELECT * FROM `usuarios` WHERE `correo` LIKE %s AND `password` LIKE %s AND `tipo` LIKE %s", (data['correo'], data['password'], data['tipo']))
    respuesta = crsr.fetchone()
    print(respuesta)
    if respuesta != None:
        response = {"respuesta": "OK"}
        print('Login correcto: ', data['correo'])
        enviar(sckt, servicio, json.dumps(response))
    else:
        response = {"respuesta": "ERROR"}
        print('Login incorrecto: ', data['correo'])
        enviar(sckt, servicio, json.dumps(response))

def registrar(sckt, servicio, data):
    crsr = db.cursor()
    crsr.execute("INSERT INTO usuarios (`nombre`, `correo`, `password`, `saldo`, `tipo`) VALUES (%s, %s, %s, %s, %s)", (data['nombre'], data['correo'], data['password'], data['saldo'], data['tipo']))
    db.commit()
    response = {"respuesta": "OK"}
    print('Usuario registrado: ', data['correo'])
    enviar(sckt, servicio, json.dumps(response))

def id(sckt, servicio, data):
    crsr = db.cursor()
    crsr.execute("SELECT id_usuario FROM `usuarios` WHERE `correo` LIKE %s", (data['correo'],))
    respuesta = crsr.fetchone()
    if len(respuesta) == 0:
        response = {"respuesta": "OK", "id": respuesta[0]}
        print('ID obtenido: ', respuesta[0])
        enviar(sckt, servicio, json.dumps(response))
    else:
        response = {"respuesta": "ERROR"}
        print('ID no obtenido: ', data['correo'])
        enviar(sckt, servicio, json.dumps(response))

if __name__ == "__main__":
    servicio = 'sensn'
    try:
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 5000)
        print('Conectandose a {} port {}'.format(*server_address))
        sckt.connect(server_address)
        print('Conectado')
        print('Se está registrando el servicio')
        sckt.send(b'00010sinitsensn')
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
        if data['opcion'] == 'login':
            login(sckt, servicio, data)
        elif data['opcion'] == 'registrar':
            registrar(sckt, servicio, data)
        elif data['opcion'] == 'id':
            id(sckt, servicio, data)
        else:
            print('Opcion no valida')
    
    