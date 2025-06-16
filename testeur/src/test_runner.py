import httpx
from pydantic import BaseModel, ValidationError

class SecureApi:
    base = "http://localhost:8001/api"

    def login(self):
        return self.base + "/login/"
    def add(self):
        return self.base + "/group/fire/add/"
    def remove(self, type_): 
        return f"{self.base}/group/{type_}/remove/"
    def me(self): 
        return self.base + "/user/me/"

class PokemonApi:
    base = "http://localhost:8002/api"

    def catch_them_all(self):
        return self.base + "/pokemon/"
    def details(self, name): 
        return f"{self.base}/pokemon/{name}/"

class MyUser(BaseModel):
    name:str
    password:str
    token:str|None = None

    def headers(self):
        return {"Authorization": f"Bearer {self.token}"}

secureapi = SecureApi()
pokemomapi = PokemonApi()

ash = MyUser(name="ash", password="pikachu")

def auth_user(user: MyUser):
    r = httpx.post(secureapi.login(), json={"username": user.name, "password": user.password})
    token = r.json()["access"]
    user.token = token
    return token


# Test user connexion
print("test wrong password")
assert httpx.post(secureapi.login(), json={"username": "unknown", "password": ash.password}).status_code == 401, "Wrong user login"
print("test wrong user name")
assert httpx.post(secureapi.login(), json={"username": ash.name, "password": "wrong"}).status_code == 401, "Wrong password login"
print("test good user/password")
assert httpx.post(secureapi.login(), json={"username": ash.name, "password": ash.password}).status_code == 200, "login fail"


# Authentification
auth_user(ash)

print("add croup fire to ash")
r = httpx.post(secureapi.add(), headers=ash.headers())
assert r.status_code in (200, 201), "Group add failed (fire)"

print("add croup fire without user")
r = httpx.post(secureapi.add())  # no headers
assert r.status_code == 401, "Group add without auth should be unauthorized"

r = httpx.get(secureapi.me(), headers=ash.headers())
print("get my user info")
assert r.status_code == 200, "Should get user info"
data = r.json()
assert ash.name == data["username"]
assert "fire" in data["groups"], "User should belong to 'fire' group"

print("test me without user")
r = httpx.get(secureapi.me())  # no headers
assert r.status_code == 401, "/me without auth should fail"

print("get ash pokemon list")
r = httpx.get(pokemomapi.catch_them_all(), headers=ash.headers())
assert r.status_code == 200, "User with fire group should access some pokemons"
pokemons = r.json()
assert isinstance(pokemons, list), "Expected a list of pokemons"

print("try to get no token pokemon list")
bad_headers = {"Authorization": "Bearer invalidtoken"}
r = httpx.get(pokemomapi.catch_them_all(), headers=bad_headers)
assert r.status_code == 401, "Invalid token should be rejected"

print("get one fire pokemen detail")
TEST_POKEMON = "charmander"  # fire-type
r = httpx.get(pokemomapi.details(TEST_POKEMON), headers=ash.headers())
assert r.status_code == 200, f"Should access details of {TEST_POKEMON}"
pokemon_data = r.json()
assert "fire" in [t["type"]["name"] for t in pokemon_data["types"]], "Wrong type"

TEST_POKEMON = "4"  # charmander ID
r = httpx.get(pokemomapi.details(TEST_POKEMON), headers=ash.headers())
assert r.status_code == 200, f"Should access details of {TEST_POKEMON}"
pokemon_data = r.json()
assert "fire" in [t["type"]["name"] for t in pokemon_data["types"]], "Wrong type"


print("get one fire pokemen detail without user")
r = httpx.get(pokemomapi.details("squirtle"), headers=ash.headers())  # water-type
assert r.status_code == 403, "User shouldn't access squirtle (not in water group)"

print("get remove ash from fire")
r = httpx.post(secureapi.remove("fire"), headers=ash.headers())
assert r.status_code in (200, 204), "Group remove failed"

print("try to get pokemon without ash")
r = httpx.get(pokemomapi.details("charmander"), headers=ash.headers())
assert r.status_code == 403, "Access to charmander should now be denied"

print("✅ All tests passed with intentional failure cases verified.")
