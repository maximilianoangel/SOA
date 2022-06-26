import socket, json
from db import db
server='pagar'

def enviar(sckt, srv, arg):
    if len(srv) < 5 or len(arg) < 1:
        print("Revisar argumentos")
        return
    lT = str(len(arg) + 5)
    while len(lT) < 5:
        lT = '0' + lT
    T = lT + srv + arg
    sckt.sendall(T.encode())

def bus(sckt):
    amntRcvd = 0
    sT = None
    msgT = ''

    while True:
        data = sckt.recv(4096)
        if amntRcvd == 0:
            sT = int(data[:5].decode())
            nameSrv = data[5:10].decode()
            msgT = msgT + data[10:].decode()
            amntRcvd = amntRcvd + len(data)-5
        else:
            msgT = msgT + data.decode()
            amntRcvd = amntRcvd + len(data)
        if amntRcvd >= sT:
            break
    return nameSrv, msgT

def registrar(socket,server):
    enviar(socket,'sinit',server)
    nombre_server,mensaje=bus(socket)
    if nombre_server=='sinit' and mensaje[:2]=='OK':
        print("Servicio activado")
    else:
        print("No se pudo conectar al servicio ",server)



def pagar(id,pago,producto):
    crsr=db.cursor()
    fetched=None
    fetched1=None
    crsr.execute("SELECT saldo FROM usuarios WHERE id_usuario = %s", (id,))
    fetched = crsr.fetchone()
    if int(fetched[0]) < int(pago):
        response= {"respuesta ":" Saldo insuficiente"}
        enviar(sckt,server,json.dumps(response))
    else:
        crsr.execute("SELECT stock FROM producto WHERE id_producto = %s", (producto,))
        fetched1 = crsr.fetchone()
        if int(fetched1[0]) == 0:
            response={"respuesta":"no hay stock del producto"}
            enviar(sckt,server,json.dumps(response))
        else:
            crsr.execute("UPDATE producto SET stock= %s where id_producto= %s", (int(fetched1[0])-1,producto))
            db.commit()
            crsr.execute("UPDATE usuarios SET saldo= %s where id_usuario= %s", (int(fetched[0])-int(pago),id))
            db.commit()
            print("Se ah realizado el pago con exito!")
            response={"respuesta":"Pago realizado con exito!"}
            enviar(sckt,server,json.dumps(response))


if __name__ == "__main__":
    try:
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 5000)
        print('Servicio: Conectándose a {} en el puerto {}'.format(*server_address))
        sckt.connect(server_address)
    except:
        print('Conexion fallida')
        quit()
    registrar(sckt,server)
    while True:
        nombre,mensaje=bus(sckt)
        if nombre==server:
            data=json.loads(mensaje)
            pagar(id=data["id"],pago=data["pago"],producto=data["producto"])
        else:
            response={"respuesta":"servicio incorrecto"}
            enviar(sckt,server,json.dumps(response))