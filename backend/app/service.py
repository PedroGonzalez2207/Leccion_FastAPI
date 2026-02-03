from .repository import MatriculaRepository
from . import models, schemas

class MatriculaService:
    def __init__(self, db):
        self.repo = MatriculaRepository(db)

    def get_all(self):
        return self.repo.find_all()

    def get_by_placa(self, placa: str):
        return self.repo.find_by_placa(placa)

    def create(self, matricula_data: schemas.MatriculaCreate):
        matricula = models.Matricula(**matricula_data.model_dump())
        return self.repo.save(matricula)

    def update(self, placa: str, matricula_data: schemas.MatriculaUpdate):
        db_matricula = self.repo.find_by_placa(placa)
        if not db_matricula:
            return None

        update_data = matricula_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_matricula, key, value)

        return self.repo.save(db_matricula)

    def delete(self, placa: str):
        db_matricula = self.repo.find_by_placa(placa)
        if db_matricula:
            self.repo.delete(db_matricula)
            return True
        return False