import os
import datetime
from flask import Flask, request, jsonify
import jwt
from dotenv import load_dotenv
from functools import wraps  # para criar decorators

load_dotenv()  # Carrega variáveis do .env

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'sua_chave_secreta')

# Simulação de base de dados de usuários com scopes
USERS_DB = {
    "marcelo": {
        "password": "senha123",
        "scopes": ["read", "write"]  # Exemplo: Marcelo pode ler e escrever
    },
    "barbosa": {
        "password": "abc123",
        "scopes": ["read"]  # Barbosa só pode ler
    }
}

# Rota pública de teste
@app.route('/')
def home():
    return jsonify({"message": "Bem-vindo à API de Autenticação com Scopes!"}), 200

# Rota para fazer login e obter JWT
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Usuário e senha são obrigatórios"}), 400

    # Verifica credenciais
    user_info = USERS_DB.get(username)
    if user_info and user_info["password"] == password:
        # Gera token com prazo de expiração e inclui scopes
        token = jwt.encode(
            {
                "sub": username,
                "scopes": user_info["scopes"],
                "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=1)
            },
            app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        return jsonify({"token": token}), 200
    else:
        return jsonify({"error": "Credenciais inválidas"}), 401

# Decorator para validar token
def token_required(f):
    @wraps(f)
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
            request.scopes = decoded_token.get('scopes', [])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401

        return f(*args, **kwargs)
    return wrapper

# Decorator para verificar se o usuário possui um scope específico
def require_scope(required_scope):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if required_scope not in request.scopes:
                return jsonify({"error": "Acesso negado. Escopo insuficiente."}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator

# Rota protegida que só requer login (qualquer scope)
@app.route('/protected', methods=['GET'])
@token_required
def protected():
    return jsonify({"message": f"Olá, {request.user}, você acessou uma rota protegida!"}), 200

# Rota que requer escopo específico ("write")
@app.route('/admin', methods=['POST'])
@token_required
@require_scope('write')
def admin_action():
    # Este endpoint está limitado a quem possui o scope 'write'
    return jsonify({"message": f"Olá, {request.user}, você tem permissão de escrita!"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
