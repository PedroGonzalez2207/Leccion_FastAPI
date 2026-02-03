from sqlalchemy.orm import Session
from . import models

class MatriculaRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_all(self):
        return self.db.query(models.Matricula).all()

    def find_by_placa(self, placa: str):
        return self.db.query(models.Matricula).filter(models.Matricula.placa == placa).first()

    def save(self, matricula: models.Matricula):
        self.db.add(matricula)
        self.db.commit()
        self.db.refresh(matricula)
        return matricula

    def delete(self, matricula: models.Matricula):
        self.db.delete(matricula)
        self.db.commit()