# Servidor RPC (Remote Procedure Call) con XML-RPC

import pymongo
from pymongo import MongoClient
from xmlrpc.server import SimpleXMLRPCServer
import datetime

import pprint

_hotelDB = 'hotel_mascotas'
_hotelCollections = ['Clientes', 'Mascotas', 'Habitaciones', 'Registros_Mascotas']


class HotelRPC:
    _metodos_rpc = ["registrar_mascota", "asignar_habitacion", "retirar_mascota",
                    "habitaciones_ocupadas", "mascotas_hospedadas", "total_visitas"]

    client = MongoClient('mongodb://localhost:27018/')

    def __init__(self, url):

        self._db = self.client[_hotelDB]

        self._server = SimpleXMLRPCServer(url, allow_none=True)

        for metodo in self._metodos_rpc:
            self._server.register_function(getattr(self, metodo))

    def es_habitacion_disponible(self, nro_habitacion):
        habitaciones_coll = self._db[_hotelCollections[2]]

        habitacion_document = habitaciones_coll.find_one({'nro_habitacion': nro_habitacion,
                                                          'estado': 'disponible'})
        if habitacion_document is None:
            return False
        return True

    def mostrar_habitaciones_libres(self):
        habitaciones_coll = self._db[_hotelCollections[2]]

        pprint.pprint("Habitaciones libres")
        habitaciones = habitaciones_coll.find({'estado': 'disponible'})

        contenido = []

        for habitacion in habitaciones:
            contenido.append({'nro_habitacion': habitacion['nro_habitacion'],
                              'tamanio': habitacion['tamanio'],
                              'precio': habitacion['precio']
                              })
        return contenido

    def registrar_mascota(self, kwargs_for_cliente={}, kwargs_for_mascota={}, kwargs_for_registro={}):

        clientes_coll = self._db[_hotelCollections[0]]
        mascotas_coll = self._db[_hotelCollections[1]]
        registros_coll = self._db[_hotelCollections[3]]

        cliente = dict(kwargs_for_cliente)
        mascota = dict(kwargs_for_mascota)
        registro = dict(kwargs_for_registro)

        cliente_document = clientes_coll.find_one({'cedula': cliente['cedula']})
        id_cliente = None

        """ Verificar si el cliente no esta en la coleccion """
        if cliente_document is None:
            id_cliente = str(clientes_coll.insert_one(cliente).inserted_id)
            pprint.pprint('_id de cliente instertado ' + id_cliente)
        else:
            pprint.pprint(cliente['nombre'] + ' ya esta registrado')
            id_cliente = str(cliente_document['_id'])

        mascota_document = mascotas_coll.find_one({'cedula_cliente': cliente['cedula'], 'nombre': mascota['nombre']})
        id_mascota = None

        """ Verificar si la mascota no esta en la coleccion """
        if mascota_document is None:
            mascota['cedula_cliente'] = cliente['cedula']
            id_mascota = str(mascotas_coll.insert_one(mascota).inserted_id)
            pprint.pprint('_id de mascota instertado ' + id_mascota)
        else:
            pprint.pprint(mascota['nombre'] + ' ya existe')
            id_mascota = str(mascota_document['_id'])

        registro_document = registros_coll.find_one({'cedula_cliente': cliente['cedula'],
                                                     'id_mascota': id_mascota,
                                                     'estado': 'alojado'})
        id_registro = None

        """ Verificar si mascota no esta alojada actualmente"""
        if registro_document is None:
            now = datetime.datetime.now()
            fecha_entrada = now.strftime('%d/%m/%Y')
            hora_entrada = now.strftime('%H:%M:%S')

            registro['cedula_cliente'] = cliente['cedula']
            registro['id_mascota'] = str(id_mascota)
            registro['nombre_mascota'] = mascota['nombre']
            registro['fecha_entrada'] = fecha_entrada
            registro['hora_entrada'] = hora_entrada
            registro['estado'] = 'alojado'

            id_registro = str(registros_coll.insert_one(registro).inserted_id)
            pprint.pprint('_id de Objeto registro insertado ' + id_registro)

        else:
            pprint.pprint(mascota['nombre'] + ' ya esta registrado')
            return False

        return True

    def asignar_habitacion(self, cedula_cliente, nombre_mascota, nro_habitacion=0):

        if not self.es_habitacion_disponible(nro_habitacion) or nro_habitacion < 1:
            return False

        mascotas_coll = self._db[_hotelCollections[1]]

        mascota_document = mascotas_coll.find_one(
            {'cedula_cliente': cedula_cliente,
             'nombre': nombre_mascota}
        )

        id_mascota = None

        """ Verificar si mascota esta en la coleccion """
        if mascota_document:
            id_mascota = str(mascota_document['_id'])
        else:
            return False

        registros_coll = self._db[_hotelCollections[3]]

        registro_document = registros_coll.find_one_and_update(
            {'cedula_cliente': cedula_cliente, 'id_mascota': id_mascota, 'estado': 'alojado'},
            {'$set': {'nro_habitacion': nro_habitacion}})

        """Revisar si la mascota tiene un registro activo"""
        if not registro_document:
            return False

        habitaciones_coll = self._db[_hotelCollections[2]]

        """Cambia el estado de la habitacion"""
        habitaciones_coll.find_one_and_update(
            {'nro_habitacion': nro_habitacion},
            {'$set': {'estado': 'ocupada'}},
            upsert=True)

        return True

    def retirar_mascota(self, cedula_cliente='', nombre_mascota=''):
        mascotas_coll = self._db[_hotelCollections[1]]

        mascota_document = mascotas_coll.find_one({'cedula_cliente': cedula_cliente,
                                                   'nombre': nombre_mascota})
        id_mascota = None

        """ Verificar si mascota esta en la coleccion """
        if mascota_document:
            id_mascota = str(mascota_document['_id'])
        else:
            return False

        registros_coll = self._db[_hotelCollections[3]]

        """ Modificar el estado del ultimo registro """
        registro_document = registros_coll.find_one_and_update(
            {'cedula_cliente': cedula_cliente, 'id_mascota': id_mascota, 'estado': 'alojado'},
            {'$set': {'estado': 'retirado'}})

        nro_habitacion = None

        if (registro_document):
            nro_habitacion = registro_document['nro_habitacion']
        else:
            return False

        """Liberar habitacion"""
        habitaciones_coll = self._db[_hotelCollections[2]]

        habitaciones_coll.find_one_and_update(
            {'nro_habitacion': nro_habitacion},
            {'$set': {'estado': 'disponible'}})

        return True

    def habitaciones_ocupadas(self):
        habitaciones_coll = self._db[_hotelCollections[2]]

        return habitaciones_coll.count_documents({'estado': 'ocupada'})

    def mascotas_hospedadas(self):
        registros_coll = self._db[_hotelCollections[3]]

        registros = registros_coll.find({'estado': 'alojado'})

        contenido = []

        mascotas_coll = self._db[_hotelCollections[1]]

        for registro in registros:
            contenido.append({'nombre_mascota': registro['nombre_mascota'],
                              'cedula_cliente': registro['cedula_cliente'],
                              'nro_habitacion': registro['nro_habitacion']})

        return contenido

    def total_visitas(self, nombre_mascota='', cedula_cliente=''):
        mascotas_coll = self._db[_hotelCollections[1]]

        mascota_document = mascotas_coll.find_one({'cedula_cliente': cedula_cliente,
                                                   'nombre': nombre_mascota})
        id_mascota = None

        """ Verificar si mascota esta en la coleccion """
        if mascota_document:
            id_mascota = str(mascota_document['_id'])
        else:
            return False

        registros_coll = self._db[_hotelCollections[3]]

        return registros_coll.count_documents({'id_mascota': id_mascota})

    def iniciar_servidor(self):
        self._server.serve_forever()


if __name__ == '__main__':
    rpc = HotelRPC(('localhost', 8000))
    print("Se ha iniciado el servidor RPC.")
    rpc.iniciar_servidor()
