# Imagem base do Python
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de requirements
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante da aplicação
COPY . /app

# Define a variável de ambiente para não gerar pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Expõe a porta 5000 para acesso externo
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "main.py"]
