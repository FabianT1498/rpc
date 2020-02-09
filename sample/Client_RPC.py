#Cliente RPC (Remote Procedure Call) con XML-RPC

from xmlrpc.client import ServerProxy

proxy = ServerProxy('http://localhost:8000/', allow_none = True)

_infoRegistro = {}
_infoCliente = {'cedula': '40','nombre': 'Luis'}

_infoMascota = {'nombre': 'Mia'}


#_infoRegistro[tipo_habitacion, nro_piso, nro_habitacion, fecha_entrada, hora_entrada, fecha_salida, hora_salida]
#_infoCliente[cedula, nombre, apellido, nacionalidad, edad, nro_tlfn, direccion, nro_contacto, zona_origen]
#_infoMascota[nombre, edad, raza, esterilizado, [vacunas], descripcion]


#proxy.registrar_mascota(_infoCliente, _infoMascota, _infoRegistro)
proxy.mostrar_registros()


