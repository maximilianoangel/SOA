import socket, json

from SOA.Servicios.pagar import enviar,bus
pag="pagar"
sckt=None


def realizar_pago(ID,pago,id_producto,cantidad):
    print("apunto de enviar la informacion del pago!")
    arg={"id":ID,"pago":pago,"producto":id_producto,"cantidad":cantidad}
    enviar(sckt,pag,json.dumps(arg))
    nombre,mensaje=bus(sckt)
    mensaje=json.loads(mensaje)
    print(mensaje["respuesta"])

if __name__ == "__main__":
    try:
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_address = ('localhost', 5000)
        print('Cliente: Conectandose a {} puerto {}'.format(*server_address))
        sckt.connect(server_address)
    except: 
        print('No es posible la conexión al bus')
        quit()
