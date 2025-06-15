import httpx
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
import logging

logger = logging.getLogger(__name__)
SECURE_API_BASE = settings.SECURE_API_URL
POKEAPI_BASE = settings.POKEAPI_BASE


def get_user_groups(request):
    token = request.headers.get("Authorization")
    if not token:
        return []

    r = httpx.get(f"{SECURE_API_BASE}/user/me/", headers={"Authorization": token})

    if r.status_code != 200:
        return [], r.status_code
    return r.json().get("groups", []), r.status_code


class PokemonListView(APIView):
    def get(self, request):
        groups, status = get_user_groups(request)
        if not groups:
            if status == 401:
                return Response({"detail": "user not found"}, status=401)
            logger.warning("no group found for user ")
            return Response({"detail": "No valid group"}, status=403)

        resp = httpx.get(f"{POKEAPI_BASE}/type")
        all_type = resp.json()["results"]
        user_types = []
        for type in all_type:
            if type["name"] in groups:
                user_types.append(type["url"])
        user_pokemons = set()
        for type_url in list(set(user_types)):
            resp = httpx.get(type_url)
            types = resp.json()
            for pokemon in types.get("pokemon", []):
                user_pokemons.add(pokemon.get("pokemon", {}).get("name"))
        list_pokemon = list(user_pokemons)
        list_pokemon.sort()
        return Response(list_pokemon)


class PokemonDetailView(APIView):
    def get(self, request, name):
        groups, status = get_user_groups(request)
        if not groups:
            if status == 401:
                return Response({"detail": "user not found"}, status=401)
            logger.warning("no group found for user ")
            return Response({"detail": "No valid group"}, status=403)

        r = httpx.get(f"{POKEAPI_BASE}/pokemon/{name}")
        if r.status_code != 200:
            return Response({"detail": "Pokemon not found"}, status=r.status_code)

        poke = r.json()
        types = [t["type"]["name"] for t in poke["types"]]

        if not any(t in groups for t in types):
            return Response({"detail": "Access denied"}, status=403)

        return Response(poke)
