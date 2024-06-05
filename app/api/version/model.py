from app import db
from app.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

class Version(Base):
    __tablename__ = 'version'
    
    id_version: Mapped[int] = mapped_column(Integer, primary_key=True)
    numero_version: Mapped[str] = mapped_column(String(50), nullable=False)
    github_url: Mapped[str] = mapped_column(String(200), nullable=True)
