

# Pokemon API

## Launch 

### local Launch
```bash
poetry run python app/manage.py runserver 0.0.0.0:8001
```

### Lint

```bash
poetry shell
black api
ruff check . --fix
bandit -r app/
deactivate
```

## Access Pokémons

### Get all accessible Pokémons

```bash
curl http://localhost:8002/api/pokemon/ -H "Authorization: Bearer <jwt_token>"
```

Returns only the Pokémons with types matching your groups.

### Get details of a Pokémon (by name or ID)

```bash
curl http://localhost:8002/api/pokemon/bulbasaur/ -H "Authorization: Bearer <jwt_token>"
```
