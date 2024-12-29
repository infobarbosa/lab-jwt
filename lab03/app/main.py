from flask import Flask, request, jsonify
import os
import requests
from jose import jwt, JWTError  # python-jose

app = Flask(__name__)

# Configurações obtidas via env
KEYCLOAK_ISSUER_URL = os.getenv("KEYCLOAK_ISSUER_URL")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID")

@app.route('/')
def public_route():
    return jsonify({"message": "Rota pública - Keycloak lab03"}), 200

def token_required(f):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization', None)
        if not auth_header:
            return jsonify({"error": "Token não fornecido"}), 401
        
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({"error": "Formato de token inválido"}), 401
        
        token = parts[1]
        
        # Aqui validamos o token consultando a JWKS do Keycloak ou introspect endpoint
        # Exemplo (via JWKS):
        try:
            # Descobrir a JWKS
            jwks_uri = f"{KEYCLOAK_ISSUER_URL}/protocol/openid-connect/certs"
            jwks_keys = requests.get(jwks_uri).json()['keys']
            
            # Decodificar usando python-jose
            decoded_token = jwt.decode(
                token,
                jwks_keys,  # pular detalhes de matching de kid
                algorithms=["RS256"],
                audience=KEYCLOAK_CLIENT_ID,
                options={"verify_aud": True, "verify_iss": False}  # etc.
            )
            
            request.user = decoded_token["preferred_username"]
        except JWTError:
            return jsonify({"error": "Token inválido ou expirado"}), 401
        
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route('/protected')
@token_required
def protected_route():
    return jsonify({"message": f"Olá, {request.user}, rota protegida!"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
