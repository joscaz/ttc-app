from app import db
from app.base import Base
from sqlalchemy import Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY

class Reporte(Base):
    __tablename__ = 'reporte'
    
    id_reporte: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha: Mapped[DateTime] = mapped_column(DateTime, default=db.func.current_timestamp())
    contenido: Mapped[str] = mapped_column(Text, nullable=False)
    id_pruebas: Mapped[ARRAY] = mapped_column(ARRAY(Integer), nullable=True)
    id_codigo: Mapped[int] = mapped_column(Integer, ForeignKey('codigo.id_codigo'))  # Asegúrate de que este campo esté definido
