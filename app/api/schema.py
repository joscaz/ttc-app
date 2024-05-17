from app.base import BaseSchema
from app.api.model import Prueba, Version, Reporte, Elemento, Codigo
from marshmallow import fields

class PruebaSchema(BaseSchema):
    class Meta:
        model: Prueba
        include_fk = True

    nombre_prueba = fields.Str()

class VersionSchema(BaseSchema):
    class Meta:
        model: Version
        include_fk = True

class ReporteSchema(BaseSchema):
    class Meta:
        model: Reporte
        include_fk = True

class ElementoSchema(BaseSchema):
    class Meta:
        model: Elemento
        include_fk = True

class CodigoSchema(BaseSchema):
    class Meta:
        model: Codigo
        include_fk = True

def prueba_load_schema(many=False):
    return PruebaSchema(
            many=many)

def prueba_dump_schema(many=False,relationships = []):
    return PruebaSchema(
        many=many,
        relationships=relationships)