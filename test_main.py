from fastapi.testclient import TestClient
from main import app
import uuid

client = TestClient(app)

# Gera um email aleatório para não dar erro de duplicidade nos testes repetidos
email_teste = f"teste_{uuid.uuid4()}@exemplo.com"

def test_criar_usuario_com_sucesso():
    response = client.post(
        "/usuarios/",
        json={
            "nome": "Usuario Teste Robô",
            "email": email_teste,
            "senha": "senha_teste_123",
            "enderecos": [
                {
                    "rua": "Rua Virtual, 000",
                    "cidade": "Matrix",
                    "estado": "SP"
                }
            ]
        },
    )
    # Verifica se o código de resposta é 201 (Created)
    assert response.status_code == 201
    # Verifica se o nome voltou correto
    data = response.json()
    assert data["nome"] == "Usuario Teste Robô"
    assert "id" in data

def test_listar_usuarios():
    response = client.get("/usuarios/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_seguranca_email_duplicado():
    # Tenta criar o MESMO usuário do primeiro teste novamente
    response = client.post(
        "/usuarios/",
        json={
            "nome": "Usuario Clone",
            "email": email_teste, # Mesmo email
            "senha": "outra_senha",
            "enderecos": []
        },
    )
    # Tem que falhar! (Esperamos erro 400)
    assert response.status_code == 400