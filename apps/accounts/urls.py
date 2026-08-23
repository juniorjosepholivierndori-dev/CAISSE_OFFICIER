from django.urls import path
from . import views


urlpatterns = [

    path(
        "inscription/",
        views.inscription,
        name="inscription"
    ),

    path(
        "connexion/",
        views.connexion,
        name="connexion"
    ),

    path(
        "inscription-reussie/",
        views.inscription_reussie,
        name="inscription_reussie"
    ),

]