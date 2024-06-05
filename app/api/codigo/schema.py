from app.base import BaseSchema
from app.api.codigo.model import Codigo
from marshmallow import fields

class CodigoSchema(BaseSchema):
    class Meta:
        model = Codigo
        include_fk = True