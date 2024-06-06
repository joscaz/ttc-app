from app.base import BaseSchema
from app.api.version.model import Version

class VersionSchema(BaseSchema):
    class Meta:
        model = Version
        include_fk = True