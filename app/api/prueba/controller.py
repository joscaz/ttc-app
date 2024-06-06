from app import db
from app.api.prueba.model import Prueba
from app.api.prueba.schema import (PruebaSchema)

def getPruebas():
    pruebas = Prueba.query.all()
    prueba_schema = PruebaSchema(many=True)
    all_pruebas = prueba_schema.dump(pruebas)
    count = Prueba.query.count()
    return count, all_pruebas
    
def getPruebaById(id):
    prueba = Prueba.query.filter_by(id_prueba=id).first()
    prueba_schema = PruebaSchema()
    prueba_dumped = prueba_schema.dump(prueba)
    return prueba_dumped

def editPruebaById(id, data):
    Prueba.query.filter_by(id_prueba=id).update(data)
    db.session.commit()
    return Prueba.query.filter_by(id_prueba=id).first()

def deletePrueba(prueba):
    prueba.delete()
    db.session.commit()