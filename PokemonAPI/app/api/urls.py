from django.urls import path
from . import views

urlpatterns = [
    path("api/pokemon/", views.PokemonListView.as_view(), name="pokemons"),
    path(
        "api/pokemon/<str:type>/",
        views.PokemonDetailView.as_view(),
        name="pokemon-name",
    ),
]

