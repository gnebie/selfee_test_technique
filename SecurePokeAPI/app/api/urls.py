from django.urls import path
from . import views

urlpatterns = [
    path("user/me/", views.MeView.as_view(), name="me"),
    path(
        "group/<str:type>/add/",
        views.AddUserToTypeGroupView.as_view(),
        name="group-add",
    ),
    path(
        "group/<str:type>/remove/",
        views.RemoveUserFromTypeGroupView.as_view(),
        name="group-remove",
    ),
]
