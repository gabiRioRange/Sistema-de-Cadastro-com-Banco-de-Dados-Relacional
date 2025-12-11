from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# Schemas para Endereço
class EnderecoBase(BaseModel):
    rua: str
    cidade: str
    estado: str

class EnderecoCreate(EnderecoBase):
    pass

class EnderecoResponse(EnderecoBase):
    id: int
    class Config:
        from_attributes = True

# Schemas para Usuário
class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    enderecos: List[EnderecoCreate] = []

class UsuarioResponse(UsuarioBase):
    id: int
    criado_em: datetime
    enderecos: List[EnderecoResponse] = []

    class Config:
        from_attributes = True