from app.base import BaseSchema
from app.api.codigo.model import Codigo

class CodigoSchema(BaseSchema):
    class Meta:
        model = Codigo
        include_fk = True