# Selfee 



## Launch

Setup your env (or rename `.en.example` to `.env`)

run the apis
```
docker-compose --build up
```


## Usage
Local connect to the SecurePokeAPI api

```
curl 
```

Local connect to the PokemonAPI api

```
curl 
```



# Selfee Technical Test — Secure Pokémon API

This project implements two independent Django REST APIs using JWT authentication and Dockerized environments:

- **SecurePokeAPI**: Handles authentication, JWT token generation, and user-type (group) management.
- **PokemonAPI**: Proxies access to the public PokeAPI based on user type memberships.

---

## Requirements

- Docker
- Docker Compose

---

## Getting Started

### 1. Setup environment variables

Setup your `.env` or rename the provided example env file:

```bash
mv .env.example .env
```

Edit it as needed (JWT secret, debug, ports, etc).

### 2. Launch the APIs

From the root directory:

```bash
docker-compose up --build
```

This will start the following services:

| API           | URL                                                      | Description                   |
| ------------- | -------------------------------------------------------- | ----------------------------- |
| SecurePokeAPI | [http://localhost:8001/api/](http://localhost:8001/api/) | Auth and user-type management |
| PokemonAPI    | [http://localhost:8002/api/](http://localhost:8002/api/) | Filtered access to Pokémons   |

---

## Testing

You can run all the functional tests from `testeur/`.

```bash
cd testeur
poetry install
poetry run python src/test_runner.py
```

---

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

---

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


---

## Tech Stack

* Python 3.10+
* Django REST Framework
* SQLite (default dev DB)
* Docker / Docker Compose
* httpx (for testeur)

