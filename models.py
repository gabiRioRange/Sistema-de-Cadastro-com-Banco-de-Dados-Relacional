from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    senha_hash = Column(String)
    bio = Column(String, nullable=True)
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    criado_em = Column(DateTime, default=datetime.utcnow)

    # Relacionamento com Endereços
    enderecos = relationship("Endereco", back_populates="dono", cascade="all, delete-orphan")

class Endereco(Base):
    __tablename__ = "enderecos"

    id = Column(Integer, primary_key=True, index=True)
    rua = Column(String)
    cidade = Column(String)
    estado = Column(String)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    # Relacionamento Reverso
    dono = relationship("Usuario", back_populates="enderecos")

class LogAcesso(Base):
    __tablename__ = "logs_acesso"

    id = Column(Integer, primary_key=True, index=True)
    metodo = Column(String)
    rota = Column(String)
    data_hora = Column(DateTime, default=datetime.utcnow)