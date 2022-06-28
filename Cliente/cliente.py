import socket, json

from SOA.Servicios.pagar import enviar,bus
pag="pagar"
sckt=None


def realizar_pago(ID,pago,id_producto,cantidad):
    arg={}
    enviar(sckt, pag, arg)
    nombre_servicio, mensaje = escuchar(sckt)
    mensaje = json.loads(mensaje[12:])
    if

if __name__ == "__main__":
    try:
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_address = ('localhost', 5000)
        print('Cliente: Conectandose a {} puerto {}'.format(*server_address))
        sckt.connect(server_address)
    except: 
        print('No es posible la conexión al bus')
        quit()
