import pytest
from app import db
from app.api.elemento.model import Elemento
from app.api.elemento.schema import ElementoSchema

def test_elemento_schema_load(client):
    elemento_data = {
        'id_elemento': 1,
        'nombre': 'element1',
        'localizador': 'div//p',
        'estado': False
    }

    schema = ElementoSchema()
    elemento = schema.load(elemento_data)
    assert elemento.id_elemento == elemento_data['id_elemento']
    assert elemento.nombre == elemento_data['nombre']
    assert elemento.localizador == elemento_data['localizador']
    assert elemento.estado == elemento_data['estado']

def test_elemento_schema_dump(client):
    elemento = Elemento(
        id_elemento=1,
        nombre='element1',
        localizador='div//p',
        estado=False
    )

    db.session.add(elemento)
    db.session.commit()

    schema = ElementoSchema()
    elemento_dict = schema.dump(elemento)

    assert elemento_dict['id_elemento'] == elemento.id_elemento
    assert elemento_dict['nombre'] == elemento.nombre
    assert elemento_dict['localizador'] == elemento.localizador
    assert elemento_dict['estado'] == elemento.estado