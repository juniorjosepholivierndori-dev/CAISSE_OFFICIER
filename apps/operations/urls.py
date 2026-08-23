from django.urls import path

from .views import (
    liste_cotisations,
    liste_prets,
    valider_pret,
    refuser_pret,
    modifier_cotisation,
    supprimer_cotisation,
    modifier_pret,
    supprimer_pret,
    modifier_remboursement,
    supprimer_remboursement,
)

urlpatterns = [

    # =====================================================
    # COTISATIONS
    # =====================================================

    path(
        "cotisations/",
        liste_cotisations,
        name="liste-cotisations"
    ),

    path(
        "cotisations/<int:cotisation_id>/modifier/",
        modifier_cotisation,
        name="modifier-cotisation"
    ),

    path(
        "cotisations/<int:cotisation_id>/supprimer/",
        supprimer_cotisation,
        name="supprimer-cotisation"
    ),


    # =====================================================
    # PRÊTS
    # =====================================================

    path(
        "prets/",
        liste_prets,
        name="liste-prets"
    ),

    path(
        "prets/<int:pret_id>/modifier/",
        modifier_pret,
        name="modifier-pret"
    ),

    path(
        "prets/<int:pret_id>/supprimer/",
        supprimer_pret,
        name="supprimer-pret"
    ),

    path(
        "prets/<int:pret_id>/valider/",
        valider_pret,
        name="valider-pret"
    ),

    path(
        "prets/<int:pret_id>/refuser/",
        refuser_pret,
        name="refuser-pret"
    ),
    # =====================================================
    # REMBOURSEMENTS
    # =====================================================

    path(
        "remboursements/<int:remboursement_id>/modifier/",
        modifier_remboursement,
        name="modifier-remboursement"
    ),

    path(
        "remboursements/<int:remboursement_id>/supprimer/",
        supprimer_remboursement,
        name="supprimer-remboursement"
    ),
]