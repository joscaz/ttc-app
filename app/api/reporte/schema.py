from app.base import BaseSchema
from app.api.reporte.model import Reporte
from marshmallow import fields

class ReporteSchema(BaseSchema):
    class Meta:
        model = Reporte
        include_fk = True
