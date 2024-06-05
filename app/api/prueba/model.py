from app import db
from app.base import Base
from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class Prueba(Base):
    __tablename__ = 'prueba'
    
    id_prueba: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre_prueba: Mapped[str] = mapped_column(String(100), nullable=False)
    fecha: Mapped[DateTime] = mapped_column(DateTime, default=db.func.current_timestamp())
    estado: Mapped[bool] = mapped_column(Boolean, nullable=False)
    cambio_aceptado: Mapped[bool] = mapped_column(Boolean, nullable=False)
    id_codigo: Mapped[int] = mapped_column(Integer, ForeignKey('codigo.id_codigo'), nullable=True)