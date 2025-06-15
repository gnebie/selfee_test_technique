import httpx

class SecureApi:
    base = "http://localhost:8000/api"

    def login(self):
        return self.base + "/auth/login/"
    def add(self):
        return self.base + "/auth/group/fire/add/"

class PokemonApi:
    base = "http://localhost:8000/api"

    def catch_them_all(self):
        return self.base + "/pokemon/"




secureapi = SecureApi()
pokemomapi = PokemonApi()

r = httpx.post(secureapi.login(), json={"username": "ash", "password": "pikachu"})
token = r.json()["access"]

headers = {"Authorization": f"Bearer {token}"}


httpx.post(secureapi.add(), headers=headers)

pokemons = httpx.get(pokemomapi.catch_them_all(), headers=headers)
print(pokemons.json())
res = pokemons.json()

assert res == ""