from app.base import BaseSchema
from app.api.prueba.model import Prueba
from marshmallow import fields

class PruebaSchema(BaseSchema):
    class Meta:
        model = Prueba
        include_fk = True

    nombre_prueba = fields.Str()

def prueba_load_schema(many=False):
    return PruebaSchema(
            many=many)

def prueba_dump_schema(many=False,relationships = []):
    return PruebaSchema(
        many=many,
        relationships=relationships)