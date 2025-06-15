import httpx
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.shortcuts import render

SECURE_API_BASE = settings.SECURE_API_URL
POKEAPI_BASE = settings.POKEAPI_BASE

def get_user_groups(request):
    token = request.headers.get("Authorization")
    if not token:
        return []

    r = httpx.get(f"{SECURE_API_BASE}/user/me/", headers={"Authorization": token})
    if r.status_code != 200:
        return []
    return r.json().get("groups", [])


class PokemonListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        groups = get_user_groups(request)
        if not groups:
            return Response({"detail": "No valid group"}, status=403)

        resp = httpx.get(f"{POKEAPI_BASE}/type")
        all_type = resp.json()["results"]
        user_types = []
        for type in all_type:
            if type["name"] in groups:
                user_types.append(type["url"])
        user_pokemons = set()
        for type in list(set(user_types)):
            resp = httpx.get(f"{POKEAPI_BASE}/pokemon?limit=1000")
            types = resp.json()["results"]
            for pokemon in types.get("pokemon", []):
                user_pokemons.add(pokemon.get("url"))
        list_pokemon = list(user_pokemons)
        list_pokemon.sort()
        return Response(list_pokemon)


class PokemonDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, name_or_id):
        groups = get_user_groups(request)
        if not groups:
            return Response({"detail": "No valid group"}, status=403)

        r = httpx.get(f"{POKEAPI_BASE}/pokemon/{name_or_id}")
        if r.status_code != 200:
            return Response({"detail": "Pokemon not found"}, status=r.status_code)

        poke = r.json()
        types = [t["type"]["name"] for t in poke["types"]]

        if not any(t in groups for t in types):
            return Response({"detail": "Access denied"}, status=403)

        return Response(poke)
