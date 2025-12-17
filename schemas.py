from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# --- SCHEMAS DE ENDEREÇO ---

class EnderecoBase(BaseModel):
    rua: str
    cidade: str
    estado: str

class EnderecoCreate(EnderecoBase):
    pass

class EnderecoResponse(EnderecoBase):
    id: int
    usuario_id: int

    class Config:
        from_attributes = True

# --- SCHEMAS DE USUÁRIO ---

class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    senha: str
    enderecos: List[EnderecoCreate] = []

class UsuarioResponse(UsuarioBase):
    id: int
    criado_em: datetime
    # 👇 AQUI ESTÁ O CAMPO QUE O SWAGGER MOSTROU QUE FALTAVA
    bio: Optional[str] = None
    enderecos: List[EnderecoResponse] = []

    class Config:
        from_attributes = True