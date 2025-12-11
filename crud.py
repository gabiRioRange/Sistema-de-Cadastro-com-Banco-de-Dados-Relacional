from sqlalchemy.orm import Session
import models, schemas

def get_usuario_por_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

# VERSÃO MELHORADA: Com Filtros Avançados
def get_usuarios(db: Session, skip: int = 0, limit: int = 10, nome_filtro: str = None, email_filtro: str = None):
    query = db.query(models.Usuario)
    
    # Aplica filtros dinamicamente se forem passados
    if nome_filtro:
        # ilike busca independente de maiúscula/minúscula (se for Postgres). 
        # No SQLite, usamos like normal.
        query = query.filter(models.Usuario.nome.contains(nome_filtro))
    if email_filtro:
        query = query.filter(models.Usuario.email.contains(email_filtro))
        
    return query.offset(skip).limit(limit).all()

# NOVO: Função de Update (O "U" do CRUD)
def atualizar_usuario(db: Session, usuario_id: int, usuario_update: schemas.UsuarioCreate):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    
    if db_usuario:
        db_usuario.nome = usuario_update.nome
        db_usuario.email = usuario_update.email
        # Nota: Atualizar endereços é mais complexo, aqui focamos no usuário base
        db.commit()
        db.refresh(db_usuario)
        
    return db_usuario

def criar_usuario(db: Session, usuario: schemas.UsuarioCreate):
    # Cria o usuário
    db_usuario = models.Usuario(nome=usuario.nome, email=usuario.email)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)

    # Cria os endereços associados (Transação implícita)
    for endereco in usuario.enderecos:
        db_endereco = models.Endereco(**endereco.dict(), usuario_id=db_usuario.id)
        db.add(db_endereco)
    
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def deletar_usuario(db: Session, usuario_id: int):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if usuario:
        db.delete(usuario)
        db.commit()
    return usuario