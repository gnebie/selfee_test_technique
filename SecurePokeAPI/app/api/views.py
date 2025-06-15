from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import httpx

from django.conf import settings

POKEAPI_TYPES_URL = settings.POKEAPI_TYPES_URL


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(
            {"username": user.username, "groups": [g.name for g in user.groups.all()]}
        )


def type_exists_in_pokeapi(type_name: str) -> bool:
    try:
        r = httpx.get(POKEAPI_TYPES_URL)
        r.raise_for_status()
        data = r.json()
        return any(t["name"] == type_name for t in data["results"])
    except Exception:
        return False


class AddUserToTypeGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, type):
        if not type_exists_in_pokeapi(type):
            return Response(
                {"detail": f"Type '{type}' is invalid."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        group, _ = Group.objects.get_or_create(name=type)
        request.user.groups.add(group)
        return Response(
            {"detail": f"User added to group '{type}'."}, status=status.HTTP_200_OK
        )


class RemoveUserFromTypeGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, type):
        try:
            group = Group.objects.get(name=type)
        except Group.DoesNotExist:
            return Response(
                {"detail": f"Group '{type}' does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        request.user.groups.remove(group)
        return Response(
            {"detail": f"User removed from group '{type}'."}, status=status.HTTP_200_OK
        )
