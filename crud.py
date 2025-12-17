from sqlalchemy.orm import Session
from typing import Optional
import bcrypt
import google.generativeai as genai
import os
import models, schemas

# Configura a API do Google Gemini com a chave do .env
# Se não houver chave, a IA não vai funcionar, mas o sistema não vai quebrar (tratamos no try/except)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


# --- LEITURA (READ) ---

def get_usuario_por_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()


def get_usuarios(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        nome_filtro: Optional[str] = None,
        email_filtro: Optional[str] = None
):
    query = db.query(models.Usuario)

    if nome_filtro:
        query = query.filter(models.Usuario.nome.like(f"%{nome_filtro}%"))
    if email_filtro:
        query = query.filter(models.Usuario.email.like(f"%{email_filtro}%"))

    return query.offset(skip).limit(limit).all()


# --- CRIAÇÃO (CREATE) COM IA ---

def criar_usuario(db: Session, usuario: schemas.UsuarioCreate):
    # 1. Criptografia da Senha (Bcrypt)
    senha_bytes = usuario.senha.encode('utf-8')
    salt = bcrypt.gensalt()
    senha_hash_bytes = bcrypt.hashpw(senha_bytes, salt)
    senha_para_banco = senha_hash_bytes.decode('utf-8')

    # 2. Geração de Bio com IA (Google Gemini)
    bio_gerada = "Bio indisponível no momento."  # Valor padrão caso a IA falhe

    try:
        if os.getenv("GEMINI_API_KEY"):
            model = genai.GenerativeModel('gemini-2.5-proo')
            # Prompt pedindo algo criativo
            prompt = f"Escreva uma mini biografia profissional (máximo 1 frase), criativa e divertida para um perfil de usuário. O nome da pessoa é {usuario.nome}."

            response = model.generate_content(prompt)
            if response.text:
                bio_gerada = response.text
    except Exception as e:
        bio_gerada = "Bio indisponível (Erro na IA)."

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("❌ ERRO: Chave de API não encontrada no .env!")
        else:
            print(f"✅ Chave encontrada! Tentando gerar bio para {usuario.nome}...")
            try:
                # Configuração nova
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-flash-latest')  # Modelo mais rápido e atual

                prompt = f"Escreva uma mini biografia profissional (máximo 1 frase), criativa e divertida para {usuario.nome}."

                response = model.generate_content(prompt)

                if response.text:
                    bio_gerada = response.text
                    print(f"🎉 Bio gerada com sucesso: {bio_gerada}")
                else:
                    print("⚠️ A IA respondeu, mas veio vazio.")

            except Exception as e:
                print(f"❌ ERRO CRÍTICO NA IA: {e}")
                # Se der erro de cota ou modelo, a bio fica com a mensagem padrão

    # 3. Cria o Usuário no Banco
    db_usuario = models.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=senha_para_banco,
        bio=bio_gerada  # <--- Aqui entra o texto da IA
    )

    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)

    # 4. Cria os Endereços
    for endereco in usuario.enderecos:
        db_endereco = models.Endereco(**endereco.dict(), usuario_id=db_usuario.id)
        db.add(db_endereco)

    db.commit()
    db.refresh(db_usuario)
    return db_usuario


# --- ATUALIZAÇÃO (UPDATE) ---

def atualizar_usuario(db: Session, usuario_id: int, usuario_update: schemas.UsuarioCreate):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

    if db_usuario:
        db_usuario.nome = usuario_update.nome
        db_usuario.email = usuario_update.email

        if usuario_update.senha:
            senha_bytes = usuario_update.senha.encode('utf-8')
            salt = bcrypt.gensalt()
            db_usuario.senha_hash = bcrypt.hashpw(senha_bytes, salt).decode('utf-8')

        db.commit()
        db.refresh(db_usuario)

    return db_usuario


# --- EXCLUSÃO (DELETE) ---

def deletar_usuario(db: Session, usuario_id: int):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if usuario:
        db.delete(usuario)
        db.commit()
    return usuario