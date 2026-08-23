from django.urls import path

from .views import profil_tresorier


urlpatterns = [
    path("profil-tresorier/", profil_tresorier, name="profil-tresorier"),
]