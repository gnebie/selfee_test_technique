from django.urls import path
from . import views

urlpatterns = [
    path("pokemon/", views.PokemonListView.as_view(), name="pokemons"),
    path(
        "pokemon/<str:name>/",
        views.PokemonDetailView.as_view(),
        name="pokemon-name",
    ),
]

