
# Secure Poke API

## Launch 

Full local launch :

### Prepare the db
```bash
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
poetry run python manage.py create_users
```

### local Launch
```bash
poetry run python app/manage.py runserver 0.0.0.0:8001
```


### Lint & Security

```bash
poetry shell
black api
ruff check . --fix
bandit -r app/ -x app/tests
deactivate
```


### Test

```bash
pytest app/tests/
```

## Usage 

### Authenticate and get JWT token

```bash
curl -X POST http://localhost:8001/api/login/ -H "Content-Type: application/json" -d '{"username": "ash", "password": "pikachu"}'
```

Response:

```json
{
  "access": "<jwt_token>",
  "refresh": "<refresh_token>"
}
```

### Add user to a Pokémon type group

```bash
curl -X POST http://localhost:8001/api/group/fire/add/ -H "Authorization: Bearer <jwt_token>"
```

### Remove user from a type group

```bash
curl -X POST http://localhost:8001/api/group/fire/remove/ -H "Authorization: Bearer <jwt_token>"
```

### Get current user and groups

```bash
curl http://localhost:8001/api/user/me/ -H "Authorization: Bearer <jwt_token>"
```
