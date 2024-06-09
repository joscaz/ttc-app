import pytest
from app import db
from app.api.codigo.model import Codigo
from app.api.codigo.schema import CodigoSchema
import datetime

def test_codigo_schema_load(client):
    codigo_data = {
        'id_codigo': 2,
        'nombre_archivo': 'prueba_pytest.html',
        'contenido': 'xxx x xxx x xx xxxxx x x x x x ',
        'fecha_subida': '2025-01-01T00:00:00'
    }

    schema = CodigoSchema()
    codigo = schema.load(codigo_data)
    assert codigo.id_codigo == codigo_data['id_codigo']
    assert codigo.nombre_archivo == codigo_data['nombre_archivo']
    assert codigo.contenido == codigo_data['contenido']
    assert codigo.fecha_subida == datetime.fromisoformat(codigo_data['fecha_subida'])

def test_codigo_schema_dump(client):
    codigo = Codigo(
        id_codigo=2,
        nombre_archivo='prueb_pytest.html',
        contenido='xxx x xxx x xx xxxxx x x x x x ',
        fecha_subida=datetime(2025, 1, 1)
    )

    db.session.add(codigo)
    db.session.commit()

    schema = CodigoSchema()
    codigo_dict = schema.dump(codigo)

    assert codigo_dict['id_codigo'] == codigo.id_codigo
    assert codigo_dict['nombre_archivo'] == codigo.nombre_archivo
    assert codigo_dict['contenido'] == codigo.contenido
    assert codigo_dict['fecha_subida'] == codigo.fecha_subida.isoformat()