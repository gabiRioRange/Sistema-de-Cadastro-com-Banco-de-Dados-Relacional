# 1. Usa uma imagem oficial do Python leve
FROM python:3.12-slim

# 2. Define o diretório de trabalho dentro do container
WORKDIR /app

# 3. Impede que o Python crie arquivos .pyc e força o log a aparecer no terminal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. Instala dependências do sistema necessárias para compilar algumas libs
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 5. Copia o arquivo de requisitos e instala as libs Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 6. Copia todo o código do projeto para dentro do container
COPY . .

# 7. Expõe a porta 8000 (onde o FastAPI roda)
EXPOSE 8000

# 8. Comando para rodar o servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]