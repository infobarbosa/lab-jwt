# lab-jwt

```sh
python3 -m venv venv
source venv/bin/activate  

```

```sh
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"username":"marcelo","password":"senha123"}' \
     http://localhost:5000/login

```

```sh
curl -X GET \
     -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtYXJjZWxvIiwiZXhwIjoxNzM1NDEzODIwfQ.vYNlG3bjRh7huHH_OxgG6san3mYgOGObYP6URei1Frc" \
     http://localhost:5000/protected

```