from app import db
from app.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean

class Elemento(Base):
    __tablename__ = 'elemento'
    
    id_elemento: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    localizador: Mapped[str] = mapped_column(String(200), nullable=False)
    estado: Mapped[bool] = mapped_column(Boolean, nullable=False)