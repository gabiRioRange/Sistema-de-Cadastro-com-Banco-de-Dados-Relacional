import streamlit as st
import requests
import os

# Configuração da Página
st.set_page_config(page_title="Sistema de Cadastro AI", layout="wide")

# URL da API (Como vamos rodar via Docker, usamos o nome do container 'app')
# Se fosse rodar localmente sem docker, seria 'http://127.0.0.1:8000'
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.title("🤖 Sistema de Cadastro Inteligente")
st.markdown("---")

# --- BARRA LATERAL (CADASTRO) ---
with st.sidebar:
    st.header("Novo Usuário")
    nome = st.text_input("Nome Completo")
    email = st.text_input("E-mail")
    senha = st.text_input("Senha", type="password")

    st.subheader("Endereço")
    rua = st.text_input("Rua e Número")
    cidade = st.text_input("Cidade")
    estado = st.text_input("Estado (Sigla)", max_chars=2)

    if st.button("Cadastrar Usuário"):
        if not nome or not email or not senha:
            st.error("Preencha os campos obrigatórios!")
        else:
            payload = {
                "nome": nome,
                "email": email,
                "senha": senha,
                "enderecos": [
                    {
                        "rua": rua,
                        "cidade": cidade,
                        "estado": estado
                    }
                ]
            }
            try:
                response = requests.post(f"{API_URL}/usuarios/", json=payload)
                if response.status_code == 201:
                    st.success("Usuário criado com sucesso!")
                    # Mostra a Bio gerada na hora
                    dados = response.json()
                    st.info(f"✨ Bio Gerada pela IA: {dados.get('bio')}")
                else:
                    st.error(f"Erro: {response.text}")
            except Exception as e:
                st.error(f"Erro de conexão com a API: {e}")

# --- ÁREA PRINCIPAL (LISTAGEM) ---
st.subheader("📋 Usuários Cadastrados")

if st.button("Atualizar Lista"):
    try:
        response = requests.get(f"{API_URL}/usuarios/")
        if response.status_code == 200:
            usuarios = response.json()

            if not usuarios:
                st.warning("Nenhum usuário encontrado.")
            else:
                # Cria cartões para cada usuário
                for user in usuarios:
                    with st.container():
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            st.markdown(f"### 👤 {user['nome']}")
                            st.caption(user['email'])
                            st.text(f"ID: {user['id']}")
                        with col2:
                            if user.get('bio'):
                                st.info(f"🤖 **IA Bio:** {user['bio']}")
                            else:
                                st.warning("Bio indisponível")

                            # Mostra endereços
                            enderecos_texto = ", ".join(
                                [f"{end['rua']} ({end['cidade']}/{end['estado']})" for end in user['enderecos']])
                            st.text(f"🏠 {enderecos_texto}")
                        st.markdown("---")
        else:
            st.error("Erro ao buscar usuários.")
    except Exception as e:
        st.error("Não foi possível conectar ao Backend. O Docker está rodando?")