from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

from apps.operations.models import Cotisation, Pret, Remboursement
from apps.referentiels.models import Adherent
from apps.audit.models import Audit


class DashboardLoginView(LoginView):
    template_name = "dashboard/login.html"
    redirect_authenticated_user = True


# =========================================================
# PROFIL TRÉSORIER
# =========================================================

@login_required
def profil_tresorier(request):

    # -----------------------------------------------------
    # ACTIVITÉS RÉCENTES DU TRÉSORIER CONNECTÉ
    # -----------------------------------------------------

    if request.user.is_authenticated:
        activites = Audit.objects.filter(
            id_user=request.user
        ).order_by("-date_heure")[:10]

    else:
        activites = Audit.objects.none()

    # -----------------------------------------------------
    # RÉSUMÉ DES OPÉRATIONS
    # -----------------------------------------------------

    # Nombre total de cotisations enregistrées
    nombre_cotisations = Cotisation.objects.count()

    # Nombre total de prêts enregistrés
    nombre_prets = Pret.objects.count()

    # Nombre total de remboursements enregistrés
    nombre_remboursements = Remboursement.objects.count()

    # -----------------------------------------------------
    # AFFICHAGE DU PROFIL
    # -----------------------------------------------------

    return render(
        request,
        "dashboard/profil-tresorier.html",
        {
            "activites": activites,

            "nombre_cotisations": nombre_cotisations,

            "nombre_prets": nombre_prets,

            "nombre_remboursements": nombre_remboursements,
        }
    )


# =========================================================
# API PROFIL
# =========================================================

@login_required
def profil_api(request):

    utilisateur = request.user

    # -----------------------------------------------------
    # UTILISATEUR NON CONNECTÉ
    # -----------------------------------------------------

    if not utilisateur.is_authenticated:

        return JsonResponse({
            "mecano": "",
            "nom": "",
            "prenom": "",
            "grade": "",
            "unite": "",
            "pays": "",
            "ville": "",
            "statut": "",
            "telephone": "",
            "email": "",
        })

    # -----------------------------------------------------
    # INFORMATIONS DU TRÉSORIER CONNECTÉ
    # -----------------------------------------------------

    return JsonResponse({

        "mecano": getattr(
            utilisateur,
            "mecano",
            ""
        ),

        "nom": utilisateur.last_name,

        "prenom": utilisateur.first_name,

        "grade": getattr(
            utilisateur,
            "grade",
            ""
        ),

        "unite": getattr(
            utilisateur,
            "unite",
            ""
        ),

        "pays": getattr(
            utilisateur,
            "pays",
            ""
        ),

        "ville": getattr(
            utilisateur,
            "ville",
            ""
        ),

        "statut": getattr(
            utilisateur,
            "statut",
            ""
        ),

        "telephone": getattr(
            utilisateur,
            "telephone",
            ""
        ),

        "email": utilisateur.email,
    })


# =========================================================
# COTISATIONS
# =========================================================

@login_required
def cotisations(request):

    # Récupérer toutes les cotisations
    cotisations = Cotisation.objects.select_related(
        "payeur"
    ).all()

    # Nombre de cotisations
    nombre_cotisations = cotisations.count()

    # Calcul du montant total
    montant_total = sum(
        cotisation.montant
        for cotisation in cotisations
    )

    return render(
        request,
        "dashboard/cotisations.html",
        {
            "cotisations": cotisations,

            "nombre_cotisations":
                nombre_cotisations,

            "montant_total":
                montant_total,
        }
    )


# =========================================================
# PRÊTS
# =========================================================

@login_required
def pret(request):

    return render(
        request,
        "dashboard/pret.html"
    )


# =========================================================
# REMBOURSEMENTS
# =========================================================

@login_required
def remboursements(request):

    # -----------------------------------------------------
    # ENREGISTREMENT D'UN REMBOURSEMENT
    # -----------------------------------------------------

    if request.method == "POST":

        pret_id = request.POST.get(
            "pret_id"
        )

        montant_verse = request.POST.get(
            "montant_verse"
        )

        date_remboursement = request.POST.get(
            "date_remboursement"
        )

        mode_paiement = request.POST.get(
            "mode_paiement"
        )

        try:

            # -------------------------------------------------
            # RECHERCHER LE PRÊT ACTIF
            # -------------------------------------------------

            pret = Pret.objects.get(
                id=pret_id,
                etat=Pret.Etat.ACTIF
            )

            # -------------------------------------------------
            # ENREGISTRER LE REMBOURSEMENT
            # -------------------------------------------------

            Remboursement.objects.create(
                pret=pret,
                montant=montant_verse,
                date_remboursement=date_remboursement,
                mode_paiement=mode_paiement
            )

            # -------------------------------------------------
            # ENREGISTRER L'ACTIVITÉ DANS L'AUDIT
            # -------------------------------------------------

            if request.user.is_authenticated:

                Audit.objects.create(

                    id_user=request.user,

                    operation_effectuee="CREATION",

                    type_modification=
                        "Enregistrement d'un remboursement",

                    donnees_avant=None,

                    donnees_apres={

                        "montant":
                            montant_verse,

                        "date_remboursement":
                            str(date_remboursement),

                        "mode_paiement":
                            mode_paiement,
                    },

                    nom_table="Remboursement"
                )

            # -------------------------------------------------
            # MESSAGE DE SUCCÈS
            # -------------------------------------------------

            return render(
                request,
                "dashboard/remboursements.html",
                {
                    "success":
                        "Remboursement enregistré avec succès."
                }
            )

        except Pret.DoesNotExist:

            # -------------------------------------------------
            # PRÊT INTROUVABLE
            # -------------------------------------------------

            return render(
                request,
                "dashboard/remboursements.html",
                {
                    "error":
                        "Prêt introuvable ou inactif."
                }
            )

    # -----------------------------------------------------
    # AFFICHAGE DE LA PAGE DES REMBOURSEMENTS
    # -----------------------------------------------------

    prets = Pret.objects.filter(
        etat=Pret.Etat.ACTIF
    ).select_related(
        "adherent"
    )

    return render(
        request,
        "dashboard/remboursements.html",
        {
            "prets": prets
        }
    )


# =========================================================
# HISTORIQUE
# =========================================================

@login_required
def historique(request):

    # -----------------------------------------------------
    # RÉCUPÉRER LES COTISATIONS
    # -----------------------------------------------------

    cotisations = Cotisation.objects.select_related(
        "payeur"
    ).all()

    # -----------------------------------------------------
    # RÉCUPÉRER LES PRÊTS
    # -----------------------------------------------------

    prets = Pret.objects.select_related(
        "adherent"
    ).all()

    # -----------------------------------------------------
    # RÉCUPÉRER LES REMBOURSEMENTS
    # -----------------------------------------------------

    remboursements = Remboursement.objects.select_related(
        "pret",
        "pret__adherent"
    ).all()

    # -----------------------------------------------------
    # AFFICHAGE
    # -----------------------------------------------------

    return render(
        request,
        "dashboard/historique.html",
        {
            "cotisations":
                cotisations,

            "prets":
                prets,

            "remboursements":
                remboursements,
        }
    )


# =========================================================
# RECHERCHE D'UN MÉCANO
# =========================================================

@login_required
def rechercher_mecano(request):

    mecano = request.GET.get(
        "mecano",
        ""
    ).strip()

    try:

        # -------------------------------------------------
        # RECHERCHER L'ADHÉRENT
        # -------------------------------------------------

        adherent = Adherent.objects.get(
            mecano=mecano
        )

        # -------------------------------------------------
        # RECHERCHER LE PRÊT ACTIF
        # -------------------------------------------------

        pret = Pret.objects.filter(
            adherent=adherent,
            etat=Pret.Etat.ACTIF
        ).first()

        # -------------------------------------------------
        # AUCUN PRÊT ACTIF
        # -------------------------------------------------

        if not pret:

            return JsonResponse({

                "success": False,

                "message":
                    "Aucun prêt actif trouvé."
            })

        # -------------------------------------------------
        # RETOURNER LES INFORMATIONS
        # -------------------------------------------------

        return JsonResponse({

            "success": True,

            "pret_id":
                pret.id,

            "nom":
                adherent.nom,

            "prenom":
                adherent.prenom,

            "montant_pret":
                str(pret.montant),
        })

    except Adherent.DoesNotExist:

        # -------------------------------------------------
        # MÉCANO INTROUVABLE
        # -------------------------------------------------

        return JsonResponse({

            "success": False,

            "message":
                "Mécano introuvable."
        })


# =========================================================
# DÉCONNEXION
# =========================================================

def deconnexion(request):

    logout(request)

    return redirect(
        "connexion"
    )