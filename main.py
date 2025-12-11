from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
import models, schemas, crud, database
from typing import Optional

# Cria as tabelas automaticamente (em produção, usaríamos Alembic)
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Sistema de Cadastro Profissional")

# Middleware para Log de Acessos
@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    # Abre uma sessão dedicada para salvar o log
    db = database.SessionLocal()
    log = models.LogAcesso(metodo=request.method, rota=request.url.path)
    db.add(log)
    db.commit()
    db.close()
    return response

# --- ROTAS ---

@app.post("/usuarios/", response_model=schemas.UsuarioResponse, status_code=201)
def criar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_usuario_por_email(db, email=usuario.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    return crud.criar_usuario(db=db, usuario=usuario)

@app.get("/usuarios/", response_model=List[schemas.UsuarioResponse])
def listar_usuarios(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    usuarios = crud.get_usuarios(db, skip=skip, limit=limit)
    return usuarios

@app.get("/usuarios/", response_model=List[schemas.UsuarioResponse])
def listar_usuarios(
    skip: int = 0, 
    limit: int = 10, 
    nome: Optional[str] = None, 
    email: Optional[str] = None,
    db: Session = Depends(database.get_db)
):
    usuarios = crud.get_usuarios(db, skip=skip, limit=limit, nome_filtro=nome, email_filtro=email)
    return usuarios

@app.delete("/usuarios/{usuario_id}")
def deletar_usuario(usuario_id: int, db: Session = Depends(database.get_db)):
    db_user = crud.deletar_usuario(db, usuario_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"message": "Usuário deletado com sucesso"}

# ROTA NOVA: Update (PUT)
@app.put("/usuarios/{usuario_id}", response_model=schemas.UsuarioResponse)
def atualizar_usuario(usuario_id: int, usuario: schemas.UsuarioCreate, db: Session = Depends(database.get_db)):
    db_usuario = crud.atualizar_usuario(db, usuario_id, usuario)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_usuario