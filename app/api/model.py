from app import db
from app.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey, Text

class Prueba(Base):
    __tablename__ = 'prueba'
    
    id_prueba: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre_prueba: Mapped[str] = mapped_column(String(100), nullable=False)
    fecha: Mapped[DateTime] = mapped_column(DateTime, default=db.func.current_timestamp())
    estado: Mapped[bool] = mapped_column(Boolean, nullable=False)
    cambio_aceptado: Mapped[bool] = mapped_column(Boolean, nullable=False)

class Version(Base):
    __tablename__ = 'version'
    
    id_version: Mapped[int] = mapped_column(Integer, primary_key=True)
    numero_version: Mapped[str] = mapped_column(String(50), nullable=False)
    github_url: Mapped[str] = mapped_column(String(200), nullable=False)

class Reporte(Base):
    __tablename__ = 'reporte'
    
    id_reporte: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha: Mapped[DateTime] = mapped_column(DateTime, default=db.func.current_timestamp())
    contenido: Mapped[str] = mapped_column(Text, nullable=False)
    id_prueba: Mapped[int] = mapped_column(Integer, ForeignKey('prueba.id_prueba'))

class Elemento(Base):
    __tablename__ = 'elemento'
    
    id_elemento: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    localizador: Mapped[str] = mapped_column(String(200), nullable=False)
    estado: Mapped[bool] = mapped_column(Boolean, nullable=False)
    id_prueba: Mapped[int] = mapped_column(Integer, ForeignKey('prueba.id_prueba'))
