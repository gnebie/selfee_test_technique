import httpx
from pydentic import BaseModel 

class SecureApi:
    base = "http://localhost:8001/api"

    def login(self):
        return self.base + "/auth/login/"
    def add(self):
        return self.base + "/auth/group/fire/add/"
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
    token:str|None

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
assert httpx.post(secureapi.login(), json={"username": "unknown", "password": ash.password}).status_code == 400, "Wrong user login"
assert httpx.post(secureapi.login(), json={"username": ash.name, "password": "wrong"}).status_code == 400, "Wrong password login"
assert httpx.post(secureapi.login(), json={"username": ash.name, "password": ash.password}).status_code == 200, "login fail"


# Authentification
auth_user(ash)

# GROUP ADD
r = httpx.post(secureapi.add(), headers=ash.headers())
assert r.status_code in (200, 201), "Group add failed (fire)"

# Test Add group without token
r = httpx.post(secureapi.add())  # no headers
assert r.status_code == 401, "Group add without auth should be unauthorized"

# ME
r = httpx.get(secureapi.me(), headers=ash.headers())
assert r.status_code == 200, "Should get user info"
data = r.json()
assert ash.name == data["username"]
assert "fire" in data["groups"], "User should belong to 'fire' group"

# Test /me without token
r = httpx.get(secureapi.me())  # no headers
assert r.status_code == 401, "/me without auth should fail"

# POKEMON LIST
r = httpx.get(pokemomapi.catch_them_all(), headers=ash.headers())
assert r.status_code == 200, "User with fire group should access some pokemons"
pokemons = r.json()
assert isinstance(pokemons, list), "Expected a list of pokemons"
assert any("fire" in p["types"] for p in pokemons), "Should return at least one fire-type pokemon"

# Test call /pokemon/ with invalid token
bad_headers = {"Authorization": "Bearer invalidtoken"}
r = httpx.get(pokemomapi.catch_them_all(), headers=bad_headers)
assert r.status_code == 401, "Invalid token should be rejected"

# POKEMON DETAIL
TEST_POKEMON = "charmander"  # fire-type
r = httpx.get(pokemomapi.details(TEST_POKEMON), headers=ash.headers())
assert r.status_code == 200, f"Should access details of {TEST_POKEMON}"
pokemon_data = r.json()
assert "fire" in [t["type"]["name"] for t in pokemon_data["types"]], "Wrong type"

# Test Access a pokemon out of user's group
r = httpx.get(pokemomapi.details("squirtle"), headers=ash.headers())  # water-type
assert r.status_code == 403, "User shouldn't access squirtle (not in water group)"

# REMOVE GROUP
r = httpx.post(secureapi.remove("fire"), headers=ash.headers())
assert r.status_code in (200, 204), "Group remove failed"

# Test After removal, shouldn't access charmander anymore
r = httpx.get(pokemomapi.details("charmander"), headers=ash.headers())
assert r.status_code == 403, "Access to charmander should now be denied"

# CLEAN CONSOLE
print("✅ All tests passed with intentional failure cases verified.")
