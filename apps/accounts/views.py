from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.operations.models import Cotisation, Pret, Remboursement
from apps.audit.models import Audit
from .forms import AdminProfileForm, CotisationForm, PretForm, RemboursementForm, UserManagementForm
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()


# =========================================================
# UTILITAIRES
# =========================================================

def admin_required(view):
    return user_passes_test(
        lambda user: user.is_authenticated and user.role == user.Role.ADMIN,
        login_url="dashboard:login",
    )(view)


def get_sidebar_context():
    """
    Retourne les compteurs dynamiques utilisés dans toutes les sidebars.
    """
    return {
        "nb_en_attente": Pret.objects.filter(etat=Pret.Etat.EN_ATTENTE).count(),
        "nb_utilisateurs": User.objects.count(),
    }


# =========================================================
# API PROFIL TRÉSORIER
# =========================================================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profil_tresorier(request):
    user = request.user

    if user.role != user.Role.TRESORIER:
        return Response(
            {"detail": "Accès réservé au trésorier."},
            status=status.HTTP_403_FORBIDDEN,
        )

    return Response({
        "id": user.id,
        "username": user.username,
        "nom": user.last_name,
        "prenom": user.first_name,
        "email": user.email,
        "role": user.get_role_display(),
    })


# =========================================================
# PROFIL ADMINISTRATEUR (TABLEAU DE BORD)
# =========================================================

@admin_required
def profile_admin(request):
    montant_total_cotisations = Cotisation.objects.aggregate(
        total=Sum("montant")
    )["total"] or 0

    total_prets_actifs = Pret.objects.filter(
        etat=Pret.Etat.ACTIF
    ).aggregate(total=Sum("montant"))["total"] or 0

    context = {
        **get_sidebar_context(),
        "users_count": User.objects.count(),
        "cotisations_count": Cotisation.objects.count(),
        "prets_count": Pret.objects.filter(etat=Pret.Etat.ACTIF).count(),
        "demandes_count": Pret.objects.filter(etat=Pret.Etat.EN_ATTENTE).count(),
        "montant_total_cotisations": montant_total_cotisations,
        "total_prets_actifs": total_prets_actifs,
        "derniers_audits": Audit.objects.select_related("id_user").order_by("-date_heure")[:8],
    }
    return render(request, "accounts/profile-admin.html", context)


# =========================================================
# GESTION DES UTILISATEURS
# =========================================================

@admin_required
def utilisateurs(request):
    search = request.GET.get("q", "").strip()
    role_filter = request.GET.get("role", "")
    statut_filter = request.GET.get("statut", "")

    users = User.objects.all().order_by("last_name", "first_name")

    if search:
        users = users.filter(
            Q(username__icontains=search)
            | Q(email__icontains=search)
            | Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
            | Q(mecano__icontains=search)
            | Q(grade__icontains=search)
            | Q(unite__icontains=search)
        )

    if role_filter:
        users = users.filter(role=role_filter)

    if statut_filter:
        users = users.filter(statut=statut_filter)

    selected_user = None
    form = UserManagementForm()

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "delete":
            target_user = get_object_or_404(User, pk=request.POST.get("user_id"))
            if target_user.pk != request.user.pk:
                target_user.delete()
                messages.success(request, "Utilisateur supprimé.")
            else:
                messages.error(request, "Vous ne pouvez pas supprimer votre propre compte.")
            return redirect("accounts:utilisateurs")

        if action == "edit":
            selected_user = get_object_or_404(User, pk=request.POST.get("user_id"))
            form = UserManagementForm(instance=selected_user)
            return render(
                request,
                "accounts/utilisateurs.html",
                {
                    **get_sidebar_context(),
                    "users": users,
                    "form": form,
                    "selected_user": selected_user,
                    "search": search,
                    "role_filter": role_filter,
                    "statut_filter": statut_filter,
                },
            )

        if action in {"create", "update"}:
            instance = None
            if action == "update":
                instance = get_object_or_404(User, pk=request.POST.get("user_id"))
            form = UserManagementForm(request.POST, instance=instance)
            if form.is_valid():
                user = form.save(commit=False)
                password = request.POST.get("password")
                if action == "create" and not password:
                    form.add_error("password", "Le mot de passe est obligatoire pour créer un utilisateur.")
                if form.errors:
                    messages.error(request, "Veuillez corriger les champs du formulaire.")
                else:
                    if password:
                        user.set_password(password)
                    user.save()
                    messages.success(
                        request,
                        "Utilisateur créé avec succès." if action == "create" else "Utilisateur mis à jour.",
                    )
                    return redirect("accounts:utilisateurs")

            messages.error(request, "Une erreur s'est produite lors de la soumission du formulaire.")

    edit_id = request.GET.get("edit")
    if edit_id:
        selected_user = get_object_or_404(User, pk=edit_id)
        form = UserManagementForm(instance=selected_user)

    return render(
        request,
        "accounts/utilisateurs.html",
        {
            **get_sidebar_context(),
            "users": users,
            "form": form,
            "selected_user": selected_user,
            "search": search,
            "role_filter": role_filter,
            "statut_filter": statut_filter,
        },
    )


# =========================================================
# COTISATIONS
# =========================================================

@admin_required
def cotisations_admin(request):
    if request.method == "POST":
        form = CotisationForm(request.POST)
        if form.is_valid():
            cotisation = form.save()
            # Audit
            Audit.objects.create(
                id_user=request.user,
                operation_effectuee="CREATION",
                type_modification="Enregistrement d'une cotisation (admin)",
                donnees_avant=None,
                donnees_apres={
                    "id": cotisation.id,
                    "montant": str(cotisation.montant),
                    "mois_concerne": str(cotisation.mois_concerne),
                    "mode_paiement": cotisation.mode_paiement,
                },
                nom_table="Cotisation",
            )
            messages.success(request, "✅ Cotisation enregistrée avec succès.")
            return redirect("accounts:cotisations-admin")
        else:
            messages.error(request, "❌ Veuillez corriger les erreurs du formulaire.")
    else:
        form = CotisationForm()

    cotisations = Cotisation.objects.select_related("payeur").order_by("-date_paiement")
    montant_total = cotisations.aggregate(total=Sum("montant"))["total"] or 0

    return render(request, "accounts/cotisations-admin.html", {
        **get_sidebar_context(),
        "form": form,
        "cotisations": cotisations,
        "montant_total": montant_total,
        "nombre_cotisations": cotisations.count(),
    })


# =========================================================
# PRÊTS
# =========================================================

@admin_required
def prets_admin(request):
    if request.method == "POST":
        form = PretForm(request.POST)
        if form.is_valid():
            pret = form.save()
            # Audit
            Audit.objects.create(
                id_user=request.user,
                operation_effectuee="CREATION",
                type_modification="Enregistrement d'un prêt (admin)",
                donnees_avant=None,
                donnees_apres={
                    "id": pret.id,
                    "adherent": str(pret.adherent),
                    "montant": str(pret.montant),
                    "date_pret": str(pret.date_pret),
                    "motif": pret.motif,
                    "duree_remboursement": pret.duree_remboursement,
                    "etat": pret.etat,
                },
                nom_table="Pret",
            )
            messages.success(request, "✅ Demande de prêt enregistrée.")
            return redirect("accounts:prets-admin")
        else:
            messages.error(request, "❌ Veuillez corriger les erreurs du formulaire.")
    else:
        form = PretForm(initial={"date_pret": timezone.localdate()})

    prets = Pret.objects.select_related(
        "adherent", "valide_par"
    ).prefetch_related("remboursements").order_by("-date_pret")

    # Statistiques
    total_prets_actifs = prets.filter(etat=Pret.Etat.ACTIF).aggregate(
        total=Sum("montant")
    )["total"] or 0

    return render(request, "accounts/prets-admin.html", {
        **get_sidebar_context(),
        "form": form,
        "prets": prets,
        "total_prets_actifs": total_prets_actifs,
        "prets_en_attente_count": prets.filter(etat=Pret.Etat.EN_ATTENTE).count(),
    })


# =========================================================
# REMBOURSEMENTS
# =========================================================

@admin_required
def remboursements_admin(request):
    if request.method == "POST":
        form = RemboursementForm(request.POST)
        if form.is_valid():
            remboursement = form.save()
            pret = remboursement.pret

            # Vérifier si le prêt est soldé
            total_rembourse = pret.total_rembourse
            if total_rembourse >= pret.montant:
                pret.etat = Pret.Etat.INACTIF
                pret.save(update_fields=["etat"])
                messages.success(
                    request,
                    f"✅ Remboursement enregistré. Le prêt #{pret.id} est maintenant soldé."
                )
            else:
                messages.success(request, "✅ Remboursement enregistré.")

            # Audit
            Audit.objects.create(
                id_user=request.user,
                operation_effectuee="CREATION",
                type_modification="Enregistrement d'un remboursement (admin)",
                donnees_avant=None,
                donnees_apres={
                    "pret_id": pret.id,
                    "montant": str(remboursement.montant),
                    "date_remboursement": str(remboursement.date_remboursement),
                    "mode_paiement": remboursement.mode_paiement,
                },
                nom_table="Remboursement",
            )
            return redirect("accounts:remboursements-admin")
        else:
            messages.error(request, "❌ Veuillez corriger les erreurs du formulaire.")
    else:
        form = RemboursementForm()

    remboursements = Remboursement.objects.select_related(
        "pret", "pret__adherent"
    ).order_by("-date_remboursement")

    total_remboursements = remboursements.aggregate(total=Sum("montant"))["total"] or 0

    return render(request, "accounts/remboursements-admin.html", {
        **get_sidebar_context(),
        "form": form,
        "remboursements": remboursements,
        "total_remboursements": total_remboursements,
        "nombre_remboursements": remboursements.count(),
    })


# =========================================================
# VALIDATION DES PRÊTS
# =========================================================

@admin_required
def validation_admin(request):
    if request.method == "POST":
        pret = get_object_or_404(Pret, pk=request.POST.get("pret_id"))
        decision = request.POST.get("decision")
        ancien_etat = pret.etat

        if decision == "approve":
            pret.etat = Pret.Etat.ACTIF
            pret.valide_par = request.user
            pret.date_validation = timezone.now()
            pret.save(update_fields=["etat", "valide_par", "date_validation"])
            # Audit
            Audit.objects.create(
                id_user=request.user,
                operation_effectuee="VALIDATION",
                type_modification="Approbation d'un prêt",
                donnees_avant={"etat": ancien_etat},
                donnees_apres={
                    "pret_id": pret.id,
                    "etat": pret.etat,
                    "valide_par": request.user.get_full_name(),
                    "date_validation": str(pret.date_validation),
                },
                nom_table="Pret",
            )
            messages.success(
                request,
                f"✅ Prêt #{pret.id} de {pret.adherent.nom} {pret.adherent.prenom} approuvé."
            )
        elif decision == "reject":
            pret.etat = Pret.Etat.REFUSE
            pret.valide_par = request.user
            pret.date_validation = timezone.now()
            pret.save(update_fields=["etat", "valide_par", "date_validation"])
            # Audit
            Audit.objects.create(
                id_user=request.user,
                operation_effectuee="REFUS",
                type_modification="Refus d'un prêt",
                donnees_avant={"etat": ancien_etat},
                donnees_apres={
                    "pret_id": pret.id,
                    "etat": pret.etat,
                    "valide_par": request.user.get_full_name(),
                    "date_validation": str(pret.date_validation),
                },
                nom_table="Pret",
            )
            messages.warning(
                request,
                f"⚠️ Prêt #{pret.id} de {pret.adherent.nom} {pret.adherent.prenom} refusé."
            )

        return redirect("accounts:validation-admin")

    prets_en_attente = Pret.objects.filter(
        etat=Pret.Etat.EN_ATTENTE
    ).select_related("adherent").order_by("-created_at")

    return render(request, "accounts/validation-admin.html", {
        **get_sidebar_context(),
        "prets": prets_en_attente,
    })


# =========================================================
# PARAMÈTRES ADMIN
# =========================================================

@admin_required
def parametres_admin(request):
    if request.method == "POST":
        form = AdminProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Paramètres enregistrés avec succès.")
            return redirect("accounts:parametres-admin")
        else:
            messages.error(request, "❌ Veuillez corriger les erreurs ci-dessous.")
    else:
        form = AdminProfileForm(instance=request.user)

    return render(request, "accounts/parametres-admin.html", {
        **get_sidebar_context(),
        "form": form,
    })


# =========================================================
# DÉCONNEXION ADMIN
# =========================================================

def deconnexion_admin(request):
    return render(request, "accounts/deconnexion-admin.html")