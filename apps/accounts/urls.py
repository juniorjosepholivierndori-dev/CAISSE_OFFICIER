from django.urls import path

from .views import (
    profil_tresorier,
    profile_admin,
    utilisateurs,
    cotisations_admin,
    prets_admin,
    remboursements_admin,
    validation_admin,
    parametres_admin,
    deconnexion_admin,
)

app_name = "accounts"

urlpatterns = [
    path("profil-tresorier/", profil_tresorier, name="api-profil-tresorier"),
    path("profile-admin/", profile_admin, name="profile-admin"),
    path("utilisateurs/", utilisateurs, name="utilisateurs"),
    path("cotisations/", cotisations_admin, name="cotisations-admin"),
    path("prets/", prets_admin, name="prets-admin"),
    path("remboursements/", remboursements_admin, name="remboursements-admin"),
    path("validation/", validation_admin, name="validation-admin"),
    path("parametres/", parametres_admin, name="parametres-admin"),
    path("deconnexion/", deconnexion_admin, name="deconnexion-admin"),
]