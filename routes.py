from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from app import schemas, models
from app.database import SessionLocal, engine
from sqlalchemy.exc import IntegrityError
from fastapi_pagination import Page, paginate

router = APIRouter()

# Endpoint para criar um novo atleta
@router.post("/atletas/", response_model=schemas.Atleta)
async def create_atleta(atleta: schemas.AtletaCreate, db: Session = Depends(SessionLocal)):
    db_atleta = models.Atleta(**atleta.dict())
    try:
        db.add(db_atleta)
        db.commit()
        db.refresh(db_atleta)
        return db_atleta
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=303, detail=f"Já existe um atleta cadastrado com o cpf: {atleta.cpf}")
    finally:
        db.close()

# Endpoint para obter todos os atletas com paginação
@router.get("/atletas/", response_model=Page[schemas.Atleta])
async def read_atletas(nome: str = None, cpf: str = None, limit: int = Query(default=10, description="Número de itens por página"),
                       offset: int = Query(default=0, description="Índice do primeiro item"), db: Session = Depends(SessionLocal)):
    atletas_query = db.query(models.Atleta)
    
    # Aplica os filtros com base nos parâmetros de consulta
    if nome:
        atletas_query = atletas_query.filter(models.Atleta.nome == nome)
    if cpf:
        atletas_query = atletas_query.filter(models.Atleta.cpf == cpf)
    
    # Realiza a paginação dos resultados
    atletas = paginate(atletas_query, limit=limit, offset=offset)
    
    return atletas
