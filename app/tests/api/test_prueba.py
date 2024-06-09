import pytest
from app import db
from app.api.prueba.model import Prueba
from app.api.prueba.schema import PruebaSchema
import datetime

def test_prueba_schema_load(client):
    prueba_data = {
        'id_prueba': 1,
        'nombre_prueba': 'prueba1',
        'fecha': '2025-01-01T00:00:00',
        'estado': False,
        'cambio_aceptado': True,
        'id_codigo': 1
    }

    schema = PruebaSchema()
    prueba = schema.load(prueba_data)
    assert prueba.id_prueba == prueba_data['id_prueba']
    assert prueba.nombre_prueba == prueba_data['nombre_prueba']
    assert prueba.fecha == datetime.fromisoformat(prueba_data['fecha'])
    assert prueba.estado == prueba_data['estado']
    assert prueba.cambio_aceptado == prueba_data['cambio_aceptado']
    assert prueba.id_codigo == prueba_data['id_codigo']

def test_prueba_schema_dump(client):
    prueba = Prueba(
        id_prueba=1,
        nombre_prueba='element1',
        fecha=datetime(2025, 1, 1),
        estado=False,
        cambio_aceptado=False,
        id_codigo=1
    )

    db.session.add(prueba)
    db.session.commit()

    schema = PruebaSchema()
    prueba_dict = schema.dump(prueba)

    assert prueba_dict['id_prueba'] == prueba.id_prueba
    assert prueba_dict['nombre_prueba'] == prueba.nombre_prueba
    assert prueba_dict['fecha'] == prueba.fecha.isoformat()
    assert prueba_dict['estado'] == prueba.estado
    assert prueba_dict['cambio_aceptado'] == prueba.cambio_aceptado
    assert prueba_dict['id_codigo'] == prueba.id_codigo