# app/main.py

import os
import datetime
from flask import Flask, request, jsonify
import jwt
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis do .env

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'sua_chave_secreta')

# Simulação de base de dados de usuários
USERS_DB = {
    "marcelo": "senha123",
    "barbosa": "abc123"
}

# Rota pública de teste
@app.route('/')
def home():
    return jsonify({"message": "Bem-vindo à API de Autenticação!"}), 200

# Rota para fazer login e obter JWT
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Usuário e senha são obrigatórios"}), 400

    # Verifica credenciais
    user_password = USERS_DB.get(username)
    if user_password and user_password == password:
        # Gera token com prazo de expiração
        token = jwt.encode(
            {
                "sub": username,
                "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=1)
            },
            app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        return jsonify({"token": token}), 200
    else:
        return jsonify({"error": "Credenciais inválidas"}), 401

# Middleware simples para verificar o token
def token_required(f):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"error": "Token não fornecido"}), 401

        token = auth_header.split(" ")[1] if len(auth_header.split(" ")) == 2 else None
        if not token:
            return jsonify({"error": "Formato de token inválido"}), 401

        try:
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            request.user = decoded_token['sub']
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401

        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# Rota protegida
@app.route('/protected', methods=['GET'])
@token_required
def protected():
    return jsonify({"message": f"Olá, {request.user}, você acessou uma rota protegida!"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
