from app import db, ma
from marshmallow import fields
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID, uuid4
from datetime import datetime

class BaseSchema(ma.SQLAlchemyAutoSchema):
  def __init__(self, *args, **kwargs):
    declared_fields = self._declared_fields
    no_nested_fields = {k: v for k, v in declared_fields.items() if not isinstance(v, fields.Nested)}
    no_nested_fields.keys()

    if 'relationships' in kwargs:
      if kwargs['relationships']:
        kwargs["only"] = tuple(set(no_nested_fields.keys()).union(set(kwargs['relationships'])))
      else:
        kwargs["only"] = tuple(set(no_nested_fields.keys()))
      del kwargs["relationships"]

    super().__init__(*args, **kwargs)

class Base(db.Model):
  __abstract__ = True

#   id: Mapped[UUID]             = mapped_column(primary_key=True, default=uuid4)
  created_at: Mapped[datetime] = mapped_column(default=db.func.current_timestamp())
  updated_at: Mapped[datetime] = mapped_column(default=db.func.current_timestamp(),
                                               onupdate=db.func.current_timestamp())
#   deleted_at: Mapped[datetime] = mapped_column(default=None, nullable=True)