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
    msgT=''
    data=sckt.recv(4096)
    nameSrv = data[5:10].decode()
    msgT = msgT + data[10:].decode()
    return nameSrv, msgT


def registrar(socket,server):
    enviar(socket,'sinit',server)
    nombre_server,mensaje=bus(socket)
    if nombre_server=='sinit' and mensaje[:2]=='OK':
        print("Servicio activado")
    else:
        print("No se pudo conectar al servicio ",server)



def pagar(id,pago,producto,cantidad):
    i=0
    j=0
    exito=0
    fetched=None
    crsr = db.cursor()
    crsr.execute("SELECT id_orden FROM Orden WHERE id_usuario = %s AND estado = 'por pagar'", (id,))
    id_orden = crsr.fetchone()
    crsr=db.cursor()
    crsr.execute("SELECT saldo FROM usuarios WHERE id_usuario = %s", (id,))
    fetched = crsr.fetchone()
    while i<len(producto):
        crsr=db.cursor()
        fetched1=None
        prod=int(producto[i])
        cant=int(cantidad[i])
        if int(fetched[0]) < int(pago):
            exito=0
            response= {"respuesta ":" Saldo insuficiente"}
            break
        else:
            crsr.execute("SELECT stock FROM producto WHERE id_producto = %s", (prod,))
            fetched1 = crsr.fetchone()
            if int(fetched1[0]) == 0 or int(fetched1[0]<int(cant)):
                exito=0
                response={"respuesta":"no hay stock del producto"}
                break
            else:
                exito=1
                response={"respuesta":"Pago realizado con exito!"}
        i=i+1
    if exito==1:
        while j<len(producto):
            prod=int(producto[j])
            cant=int(cantidad[j])
            crsr.execute("UPDATE producto SET stock= %s where id_producto= %s", (int(fetched1[0])-int(cant),prod))
            db.commit()
            j=j+1
        crsr.execute("UPDATE usuarios SET saldo= %s where id_usuario= %s", (int(fetched[0])-int(pago),id))
        db.commit()
        crsr.execute("UPDATE Orden SET estado= %s where id_orden= %s", ("pagado",int(id_orden[0])))
        print("Se ah realizado el pago con exito!")
        enviar(sckt,server,json.dumps(response))
    else:
        print("Pago rechazado")
        print(response)
        print("Total: "+str(pago))
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
            pagar(id=data["id"],pago=data["pago"],producto=data["producto"],cantidad=data["cantidad"])
        else:
            response={"respuesta":"servicio incorrecto"}
            enviar(sckt,server,json.dumps(response))