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


## Parabéns!
Você concluiu com sucesso o laboratório de JSON Web Tokens (JWT)! Agora você possui as habilidades necessárias para implementar autenticação e autorização em suas aplicações web utilizando JWT. Continue praticando e explorando novas funcionalidades para aprimorar ainda mais seus conhecimentos.
