from app import db
from app.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, Text

class Codigo(Base):
    __tablename__ = 'codigo'

    id_codigo: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre_archivo: Mapped[str] = mapped_column(String(100), nullable=False)
    contenido: Mapped[str] = mapped_column(Text, nullable=False)
    fecha_subida: Mapped[DateTime] = mapped_column(DateTime, default=db.func.current_timestamp())