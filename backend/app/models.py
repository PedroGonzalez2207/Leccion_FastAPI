from sqlalchemy import Column, String, Integer, Float
from .database import Base

class Persona(Base):
    __tablename__ = "Matricula"

    placa = Column(String, primary_key=True, index=True)
    propietario = Column(String, nullable=False)
    marca = Column(String, nullable=False)
    fabricacion = Column(Integer, nullable=False)
    valor_comercial = Column(Float, nullable=False)
    impuesto = Column(Float, nullable=False)
    codigo_revision = Column(String, nullable=False)