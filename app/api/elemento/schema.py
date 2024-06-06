from app.base import BaseSchema
from app.api.elemento.model import Elemento

class ElementoSchema(BaseSchema):
    class Meta:
        model = Elemento
        include_fk = True