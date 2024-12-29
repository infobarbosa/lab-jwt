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

# Scopes (lab02)
Scopes são uma forma de definir permissões específicas para um token JWT. Dessa forma, você controla o acesso a diferentes partes da aplicação, especificando quais ações o portador do token pode realizar. Scopes são geralmente representados como uma lista de strings no payload do token, por exemplo, ["read", "write"].


## Conceito e Função
Scopes são usados para limitar o acesso a recursos com base em permissões concedidas.
Exemplos:
- read: Permite apenas leitura de recursos.
- write: Permite criação, atualização ou remoção de recursos.
- admin: Permite acesso privilegiado a rotas administrativas.

#### Preparando o ambiente para Scopes
Este laboratório possui um arquivo específico, chamado main_scopes.py, que demonstra como utilizar JWT e scopes juntos. Para executá-lo:

Certifique-se de estar no diretório raiz do projeto (onde está o arquivo docker-compose.yml).
Caso deseje testar localmente (fora de containers), é possível instalar as dependências e rodar o main_scopes.py diretamente. Porém, recomenda-se o uso do Docker para manter o ambiente padronizado.
Construindo e subindo o container (usando main_scopes.py)

## Passo 1: Build da imagem
```sh
docker compose build

```

## Passo 2: Subindo o container
```sh
docker-compose up -d

```

Observação: Se você estiver utilizando o mesmo docker-compose.yml de exemplos anteriores, verifique se o CMD ou o Dockerfile foi ajustado para executar main_scopes.py ao invés de main.py. Caso contrário, você pode entrar no container e executar manualmente o main_scopes.py:

```sh
docker exec -it <nome_ou_id_do_container> python main_scopes.py

```

## Rotas e Testes com Scopes
1. Rota Pública
A rota raiz (/) não exige nenhum token:

```sh
curl -X GET http://localhost:5000

```
Deve retornar:

```json
{
  "message": "Bem-vindo à API de Autenticação com Scopes!"
}
```

2. Rota login (Obtendo o token com Scopes)
Existem dois usuários no exemplo do main_scopes.py:

- marcelo: "password": "senha123", "scopes": ["read", "write"]
- barbosa: "password": "abc123", "scopes": ["read"]

Exemplo de login com **marcelo**:

```sh
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"username":"marcelo","password":"senha123"}' \
     http://localhost:5000/login

```

Este comando retorna um token JWT que contém, no payload, um array de scopes, por exemplo: ["read","write"].

Exemplo de login com **barbosa**:

```sh
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"username":"barbosa","password":"abc123"}' \
     http://localhost:5000/login

```

3. Rota protected (Rota Protegida por Autenticação)
Qualquer usuário com token válido consegue acessar:

```sh
curl -X GET \
     -H "Authorization: Bearer <SEU_TOKEN_AQUI>" \
     http://localhost:5000/protected
Caso o token seja válido, a resposta será algo como:

```

```json
{
  "message": "Olá, marcelo, você acessou uma rota protegida!"
}
```
ou

```json
{
  "message": "Olá, barbosa, você acessou uma rota protegida!"
}
```
dependendo do usuário logado.

4. Rota admin (Exige Escopo write)
Para demonstrar a diferença de permissões, existe a rota `POST /admin`.<br>
Apenas quem tiver o escopo write poderá acessar com sucesso. <br>

Exemplo de cURL para essa rota:

```sh
curl -X POST \
     -H "Authorization: Bearer <TOKEN_DE_MARCELO>" \
     http://localhost:5000/admin

```

Se o token tiver o scope write, a resposta será:

```json
{
  "message": "Olá, marcelo, você tem permissão de escrita!"
}
```

Entretanto, se o usuário tiver somente read (caso do barbosa), a resposta será:

```json
{
  "error": "Acesso negado. Escopo insuficiente."
}
```

com código HTTP 403 (Forbidden).

## Conclusão
A introdução de scopes permite um controle fino de permissões, possibilitando autorizar ou restringir ações específicas dentro de sua aplicação. Esse modelo de segurança é muito útil em arquiteturas de micro serviços, APIs REST e em cenários em que você precisa garantir diferentes níveis de acesso para diferentes tipos de usuários.

Scopes flexíveis: Você pode adicionar quantos scopes desejar (por exemplo, delete, admin, finance etc.).
Validação: Sempre valide os scopes no lado do servidor (como mostramos no decorator require_scope).
Boas práticas: Mantenha seu token em um lugar seguro (por exemplo, Storage seguro no frontend, e nunca inclua tokens em URLs).
Desta forma, você consegue proteger rotas que exigem permissões específicas e manter o ambiente mais seguro e escalável.


## Parabéns!
Você concluiu com sucesso o laboratório de JSON Web Tokens (JWT)! Agora você possui as habilidades necessárias para implementar autenticação e autorização em suas aplicações web utilizando JWT. Continue praticando e explorando novas funcionalidades para aprimorar ainda mais seus conhecimentos.
