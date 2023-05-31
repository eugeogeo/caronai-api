# CaronaI


## Requisitos

- Python 3.x
- Django 4.x
- Django REST Framework
- Django REST Framework SimpleJwt

## Instalação

1. Clone o repositório em sua máquina local:

   `git clone https://github.com/eugeogeo/caronai-api.git`

2. Instale as dependências:

   `pip install -r requirements.txt`

3. Instale o Django REST Framework:

   `pip install djangorestframework`

4. Instale o Django REST Framework SimpleJWT:

   `pip install djangorestframework-simplejwt`

5. Configure o banco de dados:

   `python manage.py migrate`

6. Crie um superusuário:

   `python manage.py createsuperuser`

7. Execute o servidor:

   `python manage.py runserver`

8. Acesse a aplicação em seu navegador em http://localhost:8000/.


## Endpoints

Lista todos os usuários cadastrados: `api/token/`.

Permite visualizar um usuário :`api/users/`.

Permite listar as corridas : `api/rides/`.

Permite criar uma corrida : `api/rides/create/`.

Permite visualizar todas as corridas feitas do usuário: `api/ride-history/`.

Permite visualizar e excluir uma conta específica: `api/docs/`.


## Licença

Este projeto é licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE.md) para mais informações.
