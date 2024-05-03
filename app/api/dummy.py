from app import db
from app.api.model import Prueba

def create_dummy_pruebas():
    pruebas = [
        Prueba(nombre_prueba="Prueba 1", estado=True, cambio_aceptado=False),
        Prueba(nombre_prueba="Prueba 2", estado=True, cambio_aceptado=False),
        Prueba(nombre_prueba="Prueba 3", estado=False, cambio_aceptado=True),
        Prueba(nombre_prueba="Prueba 4", estado=False, cambio_aceptado=True)
    ]
    db.session.bulk_save_objects(pruebas)
    db.session.commit()

