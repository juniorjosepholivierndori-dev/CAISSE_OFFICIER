from django.urls import path

from .views import (
    DashboardLoginView,
    inscription,
    inscription_reussie,
    profil_tresorier,
    profil_officier,
    officier_cotisations,
    officier_prets,
    officier_remboursements,
    officier_validation,
    profil_api,
    cotisations,
    pret,
    valider_pret,
    remboursements,
    historique,
    rechercher_mecano,
    deconnexion,
)

app_name = "dashboard"

urlpatterns = [

    path(
        "",
        DashboardLoginView.as_view(),
        name="home",
    ),

    path(
        "connexion/",
        DashboardLoginView.as_view(),
        name="login",
    ),

    path("inscription/", inscription, name="inscription"),
    path("inscription-reussie/", inscription_reussie, name="inscription-reussie"),

    path(
        "connextion/",
        DashboardLoginView.as_view(),
        name="connextion",
    ),

    path(
        "profil-tresorier/",
        profil_tresorier,
        name="profil-tresorier"
    ),

    path(
        "profil-officier/",
        profil_officier,
        name="profil-officier"
    ),

    path(
        "officier/cotisations/",
        officier_cotisations,
        name="officier-cotisations"
    ),

    path(
        "officier/prets/",
        officier_prets,
        name="officier-prets"
    ),

    path(
        "officier/remboursements/",
        officier_remboursements,
        name="officier-remboursements"
    ),

    path(
        "officier/validation/",
        officier_validation,
        name="officier-validation"
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
        "pret/<int:pret_id>/valider/",
        valider_pret,
        name="valider-pret"
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