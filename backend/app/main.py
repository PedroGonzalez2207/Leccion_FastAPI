from shlex import split
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, database, service

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Matricula CRUD FastAPI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_matricula_service(db: Session = Depends(database.get_db)):
    return service.MatriculaService(db)

@app.get("/api/matriculas", response_model=List[schemas.Matricula])
def read_matriculas(svc: service.MatriculaService = Depends(get_matricula_service)):
    return svc.get_all()

@app.get("/api/matriculas/{placa}", response_model=schemas.Matricula)
def read_matricula(placa: str, svc: service.MatriculaService = Depends(get_matricula_service)):
    db_matricula = svc.get_by_placa(placa)
    if db_matricula is None:
        raise HTTPException(status_code=404, detail="Matricula not found")
    return db_matricula

@app.post("/api/matriculas", response_model=schemas.Matricula, status_code=status.HTTP_201_CREATED)
def create_matricula(matricula: schemas.MatriculaCreate, svc: service.MatriculaService = Depends(get_matricula_service)):
    if len(matricula.placa) < 4 or matricula.placa[3] != "-":
        raise HTTPException(status_code=400, detail="La placa debe contener un guion (-) en la cuarta posición")
    try:
        return svc.create(matricula)
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))

@app.put("/api/matriculas/{placa}", response_model=schemas.Matricula)
def update_matricula(placa: str, matricula: schemas.MatriculaUpdate, svc: service.MatriculaService = Depends(get_matricula_service)):
    db_matricula = svc.update(placa, matricula)
    if db_matricula is None:
        raise HTTPException(status_code=404, detail="Matricula not found")
    return db_matricula

@app.delete("/api/matriculas/{placa}")
def delete_matricula(placa: str, svc: service.MatriculaService = Depends(get_matricula_service)):
    if not svc.delete(placa):
        raise HTTPException(status_code=404, detail="Matricula not found")
    return {"message": "Matricula deleted successfully"}