from django.utils import timezone

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Cotisation, Pret, Remboursement
from apps.referentiels.models import Adherent
from apps.audit.models import Audit


# =========================================================
# COTISATIONS
# =========================================================

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def liste_cotisations(request):

    # -----------------------------------------------------
    # GET : afficher toutes les cotisations
    # -----------------------------------------------------

    if request.method == "GET":

        cotisations = Cotisation.objects.select_related(
            "payeur"
        ).all().order_by("-date_paiement")

        data = []

        for cotisation in cotisations:

            data.append({
                "id": cotisation.id,
                "montant": str(cotisation.montant),
                "date_paiement": cotisation.date_paiement,
                "mois_concerne": cotisation.mois_concerne,
                "mode_paiement": cotisation.mode_paiement,
                "payeur": (
                    cotisation.payeur.username
                    if cotisation.payeur
                    else None
                ),
            })

        return Response(data)

    # -----------------------------------------------------
    # POST : enregistrer une cotisation
    # -----------------------------------------------------

    if request.user.role != request.user.Role.TRESORIER:

        return Response(
            {
                "detail": "Accès réservé au trésorier."
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    montant = request.data.get("montant")
    mois_concerne = request.data.get("mois_concerne")
    mode_paiement = request.data.get("mode_paiement")

    # Vérification des champs
    if not montant or not mois_concerne or not mode_paiement:

        return Response(
            {
                "detail": (
                    "Les champs montant, mois_concerne "
                    "et mode_paiement sont obligatoires."
                )
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # -----------------------------------------------------
    # CRÉATION
    # -----------------------------------------------------

    cotisation = Cotisation.objects.create(
        montant=montant,
        mois_concerne=mois_concerne,
        mode_paiement=mode_paiement,
        payeur=request.user,
    )

    # -----------------------------------------------------
    # AUDIT
    # -----------------------------------------------------

    Audit.objects.create(
        id_user=request.user,
        operation_effectuee="CREATION",
        type_modification="Enregistrement d'une cotisation",
        donnees_avant=None,
        donnees_apres={
            "id": cotisation.id,
            "montant": str(cotisation.montant),
            "mois_concerne": str(cotisation.mois_concerne),
            "mode_paiement": cotisation.mode_paiement,
        },
        nom_table="Cotisation"
    )

    return Response(
        {
            "message": "Cotisation enregistrée avec succès.",
            "id": cotisation.id,
            "montant": str(cotisation.montant),
            "date_paiement": cotisation.date_paiement,
            "mois_concerne": cotisation.mois_concerne,
            "mode_paiement": cotisation.mode_paiement,
            "payeur": request.user.username,
        },
        status=status.HTTP_201_CREATED,
    )


# =========================================================
# PRÊTS
# =========================================================

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def liste_prets(request):

    # -----------------------------------------------------
    # GET : afficher tous les prêts
    # -----------------------------------------------------

    if request.method == "GET":

        prets = Pret.objects.select_related(
            "adherent",
            "valide_par"
        ).all().order_by("-date_pret")

        data = []

        for pret in prets:

            data.append({
                "id": pret.id,
                "mecano": pret.adherent.mecano,
                "nom": pret.adherent.nom,
                "prenom": pret.adherent.prenom,
                "montant": str(pret.montant),
                "date_pret": pret.date_pret,
                "motif": pret.motif,
                "duree_remboursement": pret.duree_remboursement,
                "etat": pret.etat,
                "valide_par": (
                    pret.valide_par.get_full_name()
                    if pret.valide_par
                    else None
                ),
                "date_validation": pret.date_validation,
            })

        return Response(data)

    # -----------------------------------------------------
    # POST : enregistrer un prêt
    # -----------------------------------------------------

    if request.user.role != request.user.Role.TRESORIER:

        return Response(
            {
                "detail": "Accès réservé au trésorier."
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    mecano = request.data.get("mecano")
    montant = request.data.get("montant")
    date_pret = request.data.get("date_pret")
    motif = request.data.get("motif")
    duree_remboursement = request.data.get(
        "duree_remboursement"
    )

    # Vérification des champs obligatoires
    if (
        not mecano
        or not montant
        or not date_pret
        or not duree_remboursement
    ):

        return Response(
            {
                "detail": (
                    "Les champs mécano, montant, date du prêt "
                    "et durée de remboursement sont obligatoires."
                )
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # -----------------------------------------------------
    # RECHERCHE DE L'ADHÉRENT
    # -----------------------------------------------------

    try:

        adherent = Adherent.objects.get(
            mecano=mecano
        )

    except Adherent.DoesNotExist:

        return Response(
            {
                "detail": (
                    "Aucun adhérent trouvé avec "
                    "ce numéro mécano."
                )
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    # -----------------------------------------------------
    # VÉRIFIER PRÊT ACTIF
    # -----------------------------------------------------

    pret_actif = Pret.objects.filter(
        adherent=adherent,
        etat=Pret.Etat.ACTIF
    ).exists()

    if pret_actif:

        return Response(
            {
                "detail": (
                    "Cet adhérent possède déjà "
                    "un prêt actif."
                )
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # -----------------------------------------------------
    # CRÉATION DU PRÊT
    # -----------------------------------------------------

    pret = Pret.objects.create(
        adherent=adherent,
        montant=montant,
        date_pret=date_pret,
        motif=motif or "",
        duree_remboursement=duree_remboursement,
        etat=Pret.Etat.EN_ATTENTE,
    )

    # -----------------------------------------------------
    # AUDIT
    # -----------------------------------------------------

    Audit.objects.create(
        id_user=request.user,
        operation_effectuee="CREATION",
        type_modification="Enregistrement d'un prêt",
        donnees_avant=None,
        donnees_apres={
            "id": pret.id,
            "mecano": adherent.mecano,
            "nom": adherent.nom,
            "prenom": adherent.prenom,
            "montant": str(pret.montant),
            "date_pret": str(pret.date_pret),
            "motif": pret.motif,
            "duree_remboursement": pret.duree_remboursement,
            "etat": pret.etat,
        },
        nom_table="Pret"
    )

    return Response(
        {
            "message": "Prêt enregistré avec succès.",
            "id": pret.id,
            "mecano": adherent.mecano,
            "nom": adherent.nom,
            "prenom": adherent.prenom,
            "montant": str(pret.montant),
            "date_pret": pret.date_pret,
            "motif": pret.motif,
            "duree_remboursement": pret.duree_remboursement,
            "etat": pret.etat,
        },
        status=status.HTTP_201_CREATED,
    )


# =========================================================
# VALIDER UN PRÊT
# =========================================================

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def valider_pret(request, pret_id):

    # Seul l'administrateur peut valider
    if request.user.role != request.user.Role.ADMIN:

        return Response(
            {
                "detail": (
                    "Seul l'administrateur peut "
                    "valider un prêt."
                )
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    try:

        pret = Pret.objects.select_related(
            "adherent"
        ).get(id=pret_id)

    except Pret.DoesNotExist:

        return Response(
            {
                "detail": "Prêt introuvable."
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    if pret.etat != Pret.Etat.EN_ATTENTE:

        return Response(
            {
                "detail": "Ce prêt a déjà été traité."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    ancien_etat = pret.etat

    pret.etat = Pret.Etat.ACTIF
    pret.valide_par = request.user
    pret.date_validation = timezone.now()

    pret.save(
        update_fields=[
            "etat",
            "valide_par",
            "date_validation",
        ]
    )

    # -----------------------------------------------------
    # AUDIT
    # -----------------------------------------------------

    Audit.objects.create(
        id_user=request.user,
        operation_effectuee="VALIDATION",
        type_modification="Validation d'un prêt",
        donnees_avant={
            "etat": ancien_etat,
        },
        donnees_apres={
            "mecano": pret.adherent.mecano,
            "nom": pret.adherent.nom,
            "prenom": pret.adherent.prenom,
            "montant": str(pret.montant),
            "etat": pret.etat,
            "valide_par": request.user.get_full_name(),
            "date_validation": str(
                pret.date_validation
            ),
        },
        nom_table="Pret"
    )

    return Response(
        {
            "message": "Prêt validé avec succès.",
            "id": pret.id,
            "mecano": pret.adherent.mecano,
            "nom": pret.adherent.nom,
            "prenom": pret.adherent.prenom,
            "montant": str(pret.montant),
            "etat": pret.etat,
            "valide_par": request.user.get_full_name(),
            "date_validation": pret.date_validation,
        },
        status=status.HTTP_200_OK,
    )


# =========================================================
# REFUSER UN PRÊT
# =========================================================

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def refuser_pret(request, pret_id):

    # Seul l'administrateur peut refuser
    if request.user.role != request.user.Role.ADMIN:

        return Response(
            {
                "detail": (
                    "Seul l'administrateur peut "
                    "refuser un prêt."
                )
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    try:

        pret = Pret.objects.select_related(
            "adherent"
        ).get(id=pret_id)

    except Pret.DoesNotExist:

        return Response(
            {
                "detail": "Prêt introuvable."
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    if pret.etat != Pret.Etat.EN_ATTENTE:

        return Response(
            {
                "detail": "Ce prêt a déjà été traité."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    ancien_etat = pret.etat

    pret.etat = Pret.Etat.REFUSE
    pret.valide_par = request.user
    pret.date_validation = timezone.now()

    pret.save(
        update_fields=[
            "etat",
            "valide_par",
            "date_validation",
        ]
    )

    # -----------------------------------------------------
    # AUDIT
    # -----------------------------------------------------

    Audit.objects.create(
        id_user=request.user,
        operation_effectuee="REFUS",
        type_modification="Refus d'un prêt",
        donnees_avant={
            "etat": ancien_etat,
        },
        donnees_apres={
            "mecano": pret.adherent.mecano,
            "nom": pret.adherent.nom,
            "prenom": pret.adherent.prenom,
            "montant": str(pret.montant),
            "etat": pret.etat,
            "valide_par": request.user.get_full_name(),
            "date_validation": str(
                pret.date_validation
            ),
        },
        nom_table="Pret"
    )

    return Response(
        {
            "message": "Prêt refusé.",
            "id": pret.id,
            "mecano": pret.adherent.mecano,
            "nom": pret.adherent.nom,
            "prenom": pret.adherent.prenom,
            "montant": str(pret.montant),
            "etat": pret.etat,
            "valide_par": request.user.get_full_name(),
            "date_validation": pret.date_validation,
        },
        status=status.HTTP_200_OK,
    )


# =========================================================
# MODIFIER UNE COTISATION
# =========================================================

@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def modifier_cotisation(request, cotisation_id):

    # Seul le trésorier peut modifier
    if request.user.role != request.user.Role.TRESORIER:

        return Response(
            {
                "detail": "Accès réservé au trésorier."
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    try:

        cotisation = Cotisation.objects.get(
            id=cotisation_id
        )

    except Cotisation.DoesNotExist:

        return Response(
            {
                "detail": "Cotisation introuvable."
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    # -----------------------------------------------------
    # DONNÉES AVANT
    # -----------------------------------------------------

    donnees_avant = {
        "id": cotisation.id,
        "montant": str(cotisation.montant),
        "mois_concerne": str(cotisation.mois_concerne),
        "mode_paiement": cotisation.mode_paiement,
    }

    # -----------------------------------------------------
    # NOUVELLES DONNÉES
    # -----------------------------------------------------

    montant = request.data.get(
        "montant",
        cotisation.montant
    )

    mois_concerne = request.data.get(
        "mois_concerne",
        cotisation.mois_concerne
    )

    mode_paiement = request.data.get(
        "mode_paiement",
        cotisation.mode_paiement
    )

    # -----------------------------------------------------
    # MODIFICATION
    # -----------------------------------------------------

    cotisation.montant = montant
    cotisation.mois_concerne = mois_concerne
    cotisation.mode_paiement = mode_paiement

    cotisation.save()

    # -----------------------------------------------------
    # DONNÉES APRÈS
    # -----------------------------------------------------

    donnees_apres = {
        "id": cotisation.id,
        "montant": str(cotisation.montant),
        "mois_concerne": str(cotisation.mois_concerne),
        "mode_paiement": cotisation.mode_paiement,
    }

    # -----------------------------------------------------
    # AUDIT
    # -----------------------------------------------------

    Audit.objects.create(
        id_user=request.user,
        operation_effectuee="MODIFICATION",
        type_modification="Modification d'une cotisation",
        donnees_avant=donnees_avant,
        donnees_apres=donnees_apres,
        nom_table="Cotisation"
    )

    return Response(
        {
            "message": "Cotisation modifiée avec succès.",
            "id": cotisation.id,
            "montant": str(cotisation.montant),
            "mois_concerne": cotisation.mois_concerne,
            "mode_paiement": cotisation.mode_paiement,
        },
        status=status.HTTP_200_OK,
    )


# =========================================================
# SUPPRIMER UNE COTISATION
# =========================================================

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def supprimer_cotisation(request, cotisation_id):

    # Seul le trésorier peut supprimer
    if request.user.role != request.user.Role.TRESORIER:

        return Response(
            {
                "detail": "Accès réservé au trésorier."
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    try:

        cotisation = Cotisation.objects.get(
            id=cotisation_id
        )

    except Cotisation.DoesNotExist:

        return Response(
            {
                "detail": "Cotisation introuvable."
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    # -----------------------------------------------------
    # DONNÉES AVANT SUPPRESSION
    # -----------------------------------------------------

    donnees_avant = {
        "id": cotisation.id,
        "montant": str(cotisation.montant),
        "mois_concerne": str(cotisation.mois_concerne),
        "mode_paiement": cotisation.mode_paiement,
        "payeur": (
            cotisation.payeur.username
            if cotisation.payeur
            else None
        ),
    }

    # -----------------------------------------------------
    # SUPPRESSION
    # -----------------------------------------------------

    cotisation.delete()

    # -----------------------------------------------------
    # AUDIT
    # -----------------------------------------------------

    Audit.objects.create(
        id_user=request.user,
        operation_effectuee="SUPPRESSION",
        type_modification="Suppression d'une cotisation",
        donnees_avant=donnees_avant,
        donnees_apres=None,
        nom_table="Cotisation"
    )

    return Response(
        {
            "message": "Cotisation supprimée avec succès."
        },
        status=status.HTTP_200_OK,
    )


# =========================================================
# MODIFIER UN PRÊT
# =========================================================

@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def modifier_pret(request, pret_id):

    # Seul le trésorier peut modifier
    if request.user.role != request.user.Role.TRESORIER:

        return Response(
            {
                "detail": "Accès réservé au trésorier."
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    try:

        pret = Pret.objects.select_related(
            "adherent"
        ).get(id=pret_id)

    except Pret.DoesNotExist:

        return Response(
            {
                "detail": "Prêt introuvable."
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    # -----------------------------------------------------
    # DONNÉES AVANT
    # -----------------------------------------------------

    donnees_avant = {
        "id": pret.id,
        "mecano": pret.adherent.mecano,
        "montant": str(pret.montant),
        "date_pret": str(pret.date_pret),
        "motif": pret.motif,
        "duree_remboursement": pret.duree_remboursement,
        "etat": pret.etat,
    }

    # -----------------------------------------------------
    # NOUVELLES DONNÉES
    # -----------------------------------------------------

    montant = request.data.get(
        "montant",
        pret.montant
    )

    date_pret = request.data.get(
        "date_pret",
        pret.date_pret
    )

    motif = request.data.get(
        "motif",
        pret.motif
    )

    duree_remboursement = request.data.get(
        "duree_remboursement",
        pret.duree_remboursement
    )

    # -----------------------------------------------------
    # MODIFICATION
    # -----------------------------------------------------

    pret.montant = montant
    pret.date_pret = date_pret
    pret.motif = motif
    pret.duree_remboursement = duree_remboursement

    pret.save()

    # -----------------------------------------------------
    # DONNÉES APRÈS
    # -----------------------------------------------------

    donnees_apres = {
        "id": pret.id,
        "mecano": pret.adherent.mecano,
        "montant": str(pret.montant),
        "date_pret": str(pret.date_pret),
        "motif": pret.motif,
        "duree_remboursement": pret.duree_remboursement,
        "etat": pret.etat,
    }

    # -----------------------------------------------------
    # AUDIT
    # -----------------------------------------------------

    Audit.objects.create(
        id_user=request.user,
        operation_effectuee="MODIFICATION",
        type_modification="Modification d'un prêt",
        donnees_avant=donnees_avant,
        donnees_apres=donnees_apres,
        nom_table="Pret"
    )

    return Response(
        {
            "message": "Prêt modifié avec succès.",
            "id": pret.id,
            "montant": str(pret.montant),
            "date_pret": pret.date_pret,
            "motif": pret.motif,
            "duree_remboursement": pret.duree_remboursement,
            "etat": pret.etat,
        },
        status=status.HTTP_200_OK,
    )


# =========================================================
# SUPPRIMER UN PRÊT
# =========================================================

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def supprimer_pret(request, pret_id):

    # Seul le trésorier peut supprimer
    if request.user.role != request.user.Role.TRESORIER:

        return Response(
            {
                "detail": "Accès réservé au trésorier."
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    try:

        pret = Pret.objects.select_related(
            "adherent"
        ).get(id=pret_id)

    except Pret.DoesNotExist:

        return Response(
            {
                "detail": "Prêt introuvable."
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    # -----------------------------------------------------
    # DONNÉES AVANT SUPPRESSION
    # -----------------------------------------------------

    donnees_avant = {
        "id": pret.id,
        "mecano": pret.adherent.mecano,
        "nom": pret.adherent.nom,
        "prenom": pret.adherent.prenom,
        "montant": str(pret.montant),
        "date_pret": str(pret.date_pret),
        "motif": pret.motif,
        "duree_remboursement": pret.duree_remboursement,
        "etat": pret.etat,
    }

    # -----------------------------------------------------
    # SUPPRESSION
    # -----------------------------------------------------

    pret.delete()

    # -----------------------------------------------------
    # AUDIT
    # -----------------------------------------------------

    Audit.objects.create(
        id_user=request.user,
        operation_effectuee="SUPPRESSION",
        type_modification="Suppression d'un prêt",
        donnees_avant=donnees_avant,
        donnees_apres=None,
        nom_table="Pret"
    )

    return Response(
        {
            "message": "Prêt supprimé avec succès."
        },
        status=status.HTTP_200_OK,
    )


# =========================================================
# MODIFIER UN REMBOURSEMENT
# =========================================================

@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def modifier_remboursement(request, remboursement_id):

    # Seul le trésorier peut modifier
    if request.user.role != request.user.Role.TRESORIER:

        return Response(
            {
                "detail": "Accès réservé au trésorier."
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    try:

        remboursement = Remboursement.objects.select_related(
            "pret",
            "pret__adherent"
        ).get(id=remboursement_id)

    except Remboursement.DoesNotExist:

        return Response(
            {
                "detail": "Remboursement introuvable."
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    # -----------------------------------------------------
    # DONNÉES AVANT
    # -----------------------------------------------------

    donnees_avant = {
        "id": remboursement.id,
        "montant": str(remboursement.montant),
        "date_remboursement": str(
            remboursement.date_remboursement
        ),
        "mode_paiement": remboursement.mode_paiement,
        "observation": remboursement.observation,
    }

    # -----------------------------------------------------
    # NOUVELLES DONNÉES
    # -----------------------------------------------------

    montant = request.data.get(
        "montant",
        remboursement.montant
    )

    mode_paiement = request.data.get(
        "mode_paiement",
        remboursement.mode_paiement
    )

    observation = request.data.get(
        "observation",
        remboursement.observation
    )

    # -----------------------------------------------------
    # MODIFICATION
    # -----------------------------------------------------

    remboursement.montant = montant
    remboursement.mode_paiement = mode_paiement
    remboursement.observation = observation

    remboursement.save()

    # -----------------------------------------------------
    # DONNÉES APRÈS
    # -----------------------------------------------------

    donnees_apres = {
        "id": remboursement.id,
        "montant": str(remboursement.montant),
        "date_remboursement": str(
            remboursement.date_remboursement
        ),
        "mode_paiement": remboursement.mode_paiement,
        "observation": remboursement.observation,
    }

    # -----------------------------------------------------
    # AUDIT
    # -----------------------------------------------------

    Audit.objects.create(
        id_user=request.user,
        operation_effectuee="MODIFICATION",
        type_modification="Modification d'un remboursement",
        donnees_avant=donnees_avant,
        donnees_apres=donnees_apres,
        nom_table="Remboursement"
    )

    return Response(
        {
            "message": "Remboursement modifié avec succès.",
            "id": remboursement.id,
            "montant": str(remboursement.montant),
            "date_remboursement": (
                remboursement.date_remboursement
            ),
            "mode_paiement": (
                remboursement.mode_paiement
            ),
            "observation": remboursement.observation,
        },
        status=status.HTTP_200_OK,
    )


# =========================================================
# SUPPRIMER UN REMBOURSEMENT
# =========================================================

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def supprimer_remboursement(request, remboursement_id):

    # Seul le trésorier peut supprimer
    if request.user.role != request.user.Role.TRESORIER:

        return Response(
            {
                "detail": "Accès réservé au trésorier."
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    try:

        remboursement = Remboursement.objects.select_related(
            "pret",
            "pret__adherent"
        ).get(id=remboursement_id)

    except Remboursement.DoesNotExist:

        return Response(
            {
                "detail": "Remboursement introuvable."
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    # -----------------------------------------------------
    # DONNÉES AVANT SUPPRESSION
    # -----------------------------------------------------

    donnees_avant = {
        "id": remboursement.id,
        "montant": str(remboursement.montant),
        "date_remboursement": str(
            remboursement.date_remboursement
        ),
        "mode_paiement": remboursement.mode_paiement,
        "observation": remboursement.observation,
        "pret_id": remboursement.pret.id,
    }

    # -----------------------------------------------------
    # SUPPRESSION
    # -----------------------------------------------------

    remboursement.delete()

    # -----------------------------------------------------
    # AUDIT
    # -----------------------------------------------------

    Audit.objects.create(
        id_user=request.user,
        operation_effectuee="SUPPRESSION",
        type_modification="Suppression d'un remboursement",
        donnees_avant=donnees_avant,
        donnees_apres=None,
        nom_table="Remboursement"
    )

    return Response(
        {
            "message": "Remboursement supprimé avec succès."
        },
        status=status.HTTP_200_OK,
    )