#Cliente RPC (Remote Procedure Call) con XML-RPC

from xmlrpc.client import ServerProxy
import os

proxy = ServerProxy('http://localhost:8000/', allow_none= True)

_infoRegistro = {}
_infoCliente = {}
_infoMascota = {}


def menu():
    """

    Función que limpia la pantalla y muestra nuevamente el menu

    """

    os.system('clear')  # NOTA para windows tienes que cambiar clear por cls

    print("Selecciona una opción")
    print("1 - Registrar mascota")
    print("2 - Retirar a una mascota del hotel")
    print("3 - Obtener el nro de cuartos ocupados ")
    print("4 - Listar a las mascotas albergadas y su nro. de cuarto asignado")
    print("5 - Obtener el nro. de visitas de una mascota determinada")
    print("6 - salir")


while True:

    # Mostramos el menu

    menu()

    # solicituamos una opción al usuario

    opcionMenu = input("inserta un numero valor >> ")

    if opcionMenu == "1":

        _infoCliente['cedula'] = input("Ingresar Cedula de Cliente >> ")
        _infoCliente['nombre'] = input("Ingresar Nombre de Cliente >> ")
        _infoMascota['nombre'] = input("Ingresar Nombre de Mascota >> ")
        nro_habitacion = input("Ingresar Nro de Habitacion >> ")
        proxy.registrar_mascota(_infoCliente, _infoMascota, _infoRegistro)
        print(proxy.asignar_habitacion(_infoCliente['cedula'], _infoMascota['nombre'], nro_habitacion))

    elif opcionMenu == "2":

        cedula_cliente = input("Ingresar Cedula de Cliente >> ")
        nombre_mascota = input("Ingresar Nombre de Mascota >> ")

        print(proxy.retirar_mascota(cedula_cliente, nombre_mascota))

    elif opcionMenu == "3":

        habs = proxy.habitaciones_ocupadas()
        print("Habitaciones Ocupadas ", habs)

    elif opcionMenu == "4":

        hosps = proxy.mascotas_hospedadas()

        print('Huesped :', *hosps, sep='\n')

    elif opcionMenu == "5":
        cedula_cliente = input("Ingresar Cedula de Cliente >> ")
        nombre_mascota = input("Ingresar Nombre de Mascota >> ")
        visits = proxy.total_visitas(nombre_mascota, cedula_cliente)
        print("Numero de visitas: ", visits)

    elif opcionMenu == "6":

        break

    else:

        print("")

        input("No has pulsado ninguna opción correcta...\npulsa una tecla para continuar")



