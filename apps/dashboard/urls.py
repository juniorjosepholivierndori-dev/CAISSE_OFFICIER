from django.urls import path

from .views import (
    profil_tresorier,
    profil_api,
    cotisations,
    pret,
    remboursements,
    historique,
    rechercher_mecano,
    deconnexion,
)

urlpatterns = [

    path(
        "profil-tresorier/",
        profil_tresorier,
        name="profil-tresorier"
    ),

    path(
        "api/profil/",
        profil_api,
        name="profil-api"
    ),

    path(
        "cotisations/",
        cotisations,
        name="cotisations"
    ),

    path(
        "pret/",
        pret,
        name="pret"
    ),

    path(
        "remboursements/",
        remboursements,
        name="remboursements"
    ),

    path(
        "historique/",
        historique,
        name="historique"
    ),

    path(
        "api/rechercher-mecano/",
        rechercher_mecano,
        name="rechercher-mecano"
    ),

    path(
        "deconnexion/",
        deconnexion,
        name="deconnexion"
    ),
]