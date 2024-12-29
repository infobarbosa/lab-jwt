# JSON Web Tokens (JWT)
Author: Prof. Barbosa<br>
Contact: infobarbosa@gmail.com<br>
Github: [infobarbosa](https://github.com/infobarbosa)

## Objetivo
O objetivo deste laboratório é fornecer uma introdução prática ao uso de JSON Web Tokens (JWT) para autenticação e autorização em aplicações web. Você aprenderá a configurar um ambiente de desenvolvimento na AWS utilizando o Cloud9, criar e manipular tokens JWT, e implementar mecanismos de segurança para proteger suas aplicações.

Ao final deste laboratório, você terá uma compreensão sólida sobre como os tokens JWT funcionam, como integrá-los em suas aplicações e como utilizar as melhores práticas de segurança para garantir a integridade e a confidencialidade dos dados transmitidos.

## Docker
Neste laboratório, utilizaremos o Docker para criar um ambiente isolado e consistente para o desenvolvimento e teste de aplicações que utilizam JSON Web Tokens (JWT). O Docker nos permite empacotar todas as dependências necessárias em contêineres, garantindo que o ambiente de desenvolvimento seja idêntico ao ambiente de produção. Isso facilita a configuração, a escalabilidade e a manutenção das aplicações, além de simplificar o processo de integração contínua e entrega contínua (CI/CD). Você aprenderá a criar contêineres Docker, configurar arquivos Dockerfile e docker-compose, e executar suas aplicações dentro desses contêineres.

## Ambiente 
Este laborarório pode ser executado em qualquer estação de trabalho.<br>
Recomendo, porém, a execução em Linux.<br>
Caso você não tenha um à sua disposição, é possível utilizar o [AWS Cloud9](https://aws.amazon.com/cloud9/). Siga essas [instruções](Cloud9/README.md).

## Setup
Para começar, faça o clone deste repositório:
```
git clone https://github.com/infobarbosa/lab-jwt.git

```

>### Atenção! 
> Os comandos desse tutorial presumem que você está no diretório raiz do projeto.

```
cd lab-jwt

```

## Buid da imagem
```sh
docker compose build

```

## Subindo o container
```sh
docker-compose up -d

```

## Rota pública
```sh
curl -X GET \
     http://localhost:5000

```
## Rota `login` (Obtendo o token)
```sh
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"username":"marcelo","password":"senha123"}' \
     http://localhost:5000/login

```

## Rota `protected`
```sh
curl -X GET \
     -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtYXJjZWxvIiwiZXhwIjoxNzM1NDE1NjMwfQ.yz50XQcKsiwr3-BYmqqzsJibPoV0_EMlmB3esi5gH4s" \
     http://localhost:5000/protected

```

# Scopes
Scopes são uma maneira de definir permissões específicas para um token JWT. Eles permitem que você controle o acesso a diferentes partes da sua aplicação, especificando quais ações o portador do token pode realizar. Scopes são geralmente representados como uma lista de strings no payload do token JWT.

### Conceito e Função
Scopes são usados para limitar o acesso a recursos específicos com base nas permissões atribuídas ao token. Por exemplo, você pode ter um token que permite apenas a leitura de dados, enquanto outro token permite tanto a leitura quanto a escrita. Isso é útil para implementar controle de acesso baseado em funções (RBAC) e garantir que os usuários só possam acessar os recursos que lhes são permitidos.

### Utilizando Scopes com JWT
Para utilizar scopes com JWT, você precisa incluir uma reivindicação (claim) chamada `scope` no payload do token. Aqui está um exemplo de como criar um token com scopes:

#### Exemplo de Payload com Scopes
```json
{
     "sub": "marcelo",
     "scope": "read write",
     "exp": 1735415630
}
```

#### Verificando Scopes no Servidor
No lado do servidor, você precisa verificar se o token possui os scopes necessários para acessar um recurso específico. Aqui está um exemplo em Python usando Flask e PyJWT:

```python
from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)
SECRET_KEY = 'your_secret_key'

def token_required(f):
     def decorator(*args, **kwargs):
          token = request.headers.get('Authorization').split()[1]
          try:
               data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
               request.scopes = data.get('scope', '').split()
          except Exception as e:
               return jsonify({"message": "Token inválido!"}), 403
          return f(*args, **kwargs)
     return decorator

def requires_scope(required_scope):
     def decorator(f):
          def wrapper(*args, **kwargs):
               if required_scope not in request.scopes:
                    return jsonify({"message": "Permission denied!"}), 403
               return f(*args, **kwargs)
          return wrapper
     return decorator

@app.route('/protected', methods=['GET'])
@token_required
@requires_scope('read')
def protected():
     return jsonify({"message": "Esta é uma rota protegida."})

if __name__ == '__main__':
          app.run(debug=True)
```

Neste exemplo, a rota `/protected` só pode ser acessada se o token JWT contiver o scope `read`.

### Conclusão
Scopes são uma ferramenta poderosa para gerenciar permissões em sua aplicação. Ao utilizar scopes com JWT, você pode implementar um controle de acesso granular e garantir que os usuários só possam realizar ações permitidas. Certifique-se de sempre validar os scopes no servidor para proteger seus recursos de acessos não autorizados.


## Parabéns!
Você concluiu com sucesso o laboratório de JSON Web Tokens (JWT)! Agora você possui as habilidades necessárias para implementar autenticação e autorização em suas aplicações web utilizando JWT. Continue praticando e explorando novas funcionalidades para aprimorar ainda mais seus conhecimentos.
