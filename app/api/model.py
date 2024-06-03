from app import db
from app.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.dialects.postgresql import ARRAY

class Prueba(Base):
    __tablename__ = 'prueba'
    
    id_prueba: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre_prueba: Mapped[str] = mapped_column(String(100), nullable=False)
    fecha: Mapped[DateTime] = mapped_column(DateTime, default=db.func.current_timestamp())
    estado: Mapped[bool] = mapped_column(Boolean, nullable=False)
    cambio_aceptado: Mapped[bool] = mapped_column(Boolean, nullable=False)
    id_codigo: Mapped[int] = mapped_column(Integer, ForeignKey('codigo.id_codigo'), nullable=True)

class Version(Base):
    __tablename__ = 'version'
    
    id_version: Mapped[int] = mapped_column(Integer, primary_key=True)
    numero_version: Mapped[str] = mapped_column(String(50), nullable=False)
    github_url: Mapped[str] = mapped_column(String(200), nullable=True)

class Reporte(Base):
    __tablename__ = 'reporte'
    
    id_reporte: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha: Mapped[DateTime] = mapped_column(DateTime, default=db.func.current_timestamp())
    contenido: Mapped[str] = mapped_column(Text, nullable=False)
    id_pruebas: Mapped[ARRAY] = mapped_column(ARRAY(Integer), nullable=True)
    id_codigo: Mapped[int] = mapped_column(Integer, ForeignKey('codigo.id_codigo'))  # Asegúrate de que este campo esté definido

class Elemento(Base):
    __tablename__ = 'elemento'
    
    id_elemento: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    localizador: Mapped[str] = mapped_column(String(200), nullable=False)
    estado: Mapped[bool] = mapped_column(Boolean, nullable=False)

class Codigo(Base):
    __tablename__ = 'codigo'

    id_codigo: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre_archivo: Mapped[str] = mapped_column(String(100), nullable=False)
    contenido: Mapped[str] = mapped_column(Text, nullable=False)
    fecha_subida: Mapped[DateTime] = mapped_column(DateTime, default=db.func.current_timestamp())