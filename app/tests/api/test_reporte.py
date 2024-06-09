import pytest
from app import db
from app.api.reporte.model import Reporte
from app.api.reporte.schema import ReporteSchema
import datetime

def test_reporte_schema_load(client):
    reporte_data = {
        'id_reporte': 1,
        'fecha': '2025-01-01T00:00:00',
        'contenido': False,
        'id_pruebas': [1,2,3],
        'id_codigo': 1
    }

    schema = ReporteSchema()
    reporte = schema.load(reporte_data)
    assert reporte.id_reporte == reporte_data['id_reporte']
    assert reporte.fecha == datetime.fromisoformat(reporte_data['fecha'])
    assert reporte.contenido == reporte_data['contenido']
    assert reporte.id_pruebas == reporte_data['id_pruebas']
    assert reporte.id_codigo == reporte_data['id_codigo']

def test_reporte_schema_dump(client):
    reporte = Reporte(
        id_reporte=1,
        fecha=datetime(2025, 1, 1),
        contenido=False,
        id_pruebas=False,
        id_codigo=1
    )

    db.session.add(reporte)
    db.session.commit()

    schema = ReporteSchema()
    reporte_dict = schema.dump(reporte)

    assert reporte_dict['id_reporte'] == reporte.id_reporte
    assert reporte_dict['fecha'] == reporte.fecha.isoformat()
    assert reporte_dict['contenido'] == reporte.contenido
    assert reporte_dict['id_pruebas'] == reporte.id_pruebas
    assert reporte_dict['id_codigo'] == reporte.id_codigo