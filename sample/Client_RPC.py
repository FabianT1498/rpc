#Cliente RPC (Remote Procedure Call) con XML-RPC

from xmlrpc.client import ServerProxy
import pprint

proxy = ServerProxy('http://localhost:8000/', allow_none = True)

_infoRegistro = {'fecha_salida': '20/02/13'}
_infoCliente = {'cedula': '43404593','nombre': 'Luis', 'apellido': 'Jaramillo',
                'correo': 'fabiantrillo1498@gmail.com', 'direccion': 'Los mangos'}

_infoMascota = {'nombre': 'Puppi', 'edad': 20, 'raza': 'Poodle'}


pprint.pprint(proxy.registrar_mascota(_infoCliente, _infoMascota, _infoRegistro))



