import socket, json
from pagar import enviar, bus
pag="pagar"
sckt=None

def menu1(sckt):
    menu= """
    ***************************************
    * pagos                               *
    *-------------------------------------*
    * Elija una opción:                   *
    * 1) pagar                            *
    * 2) Log in (Ingresar con usuario)    *
    ***************************************

    Opción: """
    option = input(menu)
    ID=input("ingrese id del comprador")
    pago=input("ingrese pago del comprador")
    producto=input("ingrese id del producto a comprar")
    if option == "1":
        arg={"id":ID,"pago":pago,"producto":producto}
        enviar(sckt,pag,json.dumps(arg))


if __name__ == "__main__":
    try:
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_address = ('localhost', 5000)
        print('Cliente: Conectandose a {} puerto {}'.format(*server_address))
        sckt.connect(server_address)
    except: 
        print('No es posible la conexión al bus')
        quit()

    menu1(sckt)