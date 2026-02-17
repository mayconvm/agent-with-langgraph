# Use a imagem Alpine do Python por ser uma das menores imagens oficiais disponíveis.
FROM python:3.12-alpine

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala o uv para gerenciamento rápido de dependências e curl para healthchecks
COPY pyproject.toml uv.lock ./
RUN apk add --no-cache curl && \
    pip install --no-cache-dir uv && \
    uv pip install --no-cache-dir --system .

# Copia o código da aplicação
COPY . .

# Comando para executar a aplicação
CMD ["python", "main.py"]
