from django.urls import path

from .views import member_login

app_name = "accounts"

urlpatterns = [
    path("connexion/", member_login, name="login"),
]
