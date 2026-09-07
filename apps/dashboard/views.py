from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from apps.operations.models import Cotisation, Pret, Remboursement
from apps.referentiels.models import Adherent
from apps.audit.models import Audit


class DashboardLoginView(LoginView):
    template_name = "dashboard/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.role == user.Role.ADMIN:
            return "/accounts/profile-admin/"
        elif user.role == user.Role.OFFICIER:
            return "/profil-officier/"
        else:
            return "/profil-tresorier/"


class InscriptionForm(UserCreationForm):
    mecano = forms.CharField(max_length=50, label="Numéro mécano")
    nom = forms.CharField(max_length=100)
    prenom = forms.CharField(max_length=100, label="Prénom")
    grade = forms.CharField(max_length=100)
    unite = forms.CharField(max_length=150)
    statut = forms.ChoiceField(
        choices=(("", "Sélectionnez votre statut"), ("ACTIF", "Actif"), ("RETRAITE", "Retraité")),
        required=True,
    )
    date_naissance = forms.DateField(
        label="Date de naissance",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    telephone = forms.CharField(max_length=30, label="Téléphone")
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("mecano", "nom", "prenom", "grade", "unite", "statut", "date_naissance", "telephone", "email")

    def save(self, commit=True):
        adherent = Adherent(
            mecano=self.cleaned_data["mecano"],
            nom=self.cleaned_data["nom"],
            prenom=self.cleaned_data["prenom"],
            grade=self.cleaned_data["grade"],
            unite=self.cleaned_data["unite"],
            pays="",
            ville="",
            statut=self.cleaned_data["statut"],
            telephone=self.cleaned_data["telephone"],
            email=self.cleaned_data["email"],
        )
        if commit:
            adherent.save()
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["prenom"]
        user.last_name = self.cleaned_data["nom"]
        if commit:
            user.save()
        return user


def inscription(request):
    if request.method == "POST":
        form = InscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard:inscription-reussie")
    else:
        form = InscriptionForm()
    return render(request, "dashboard/inscription.html", {"form": form})


def inscription_reussie(request):
    return render(request, "dashboard/inscription-reussie.html")


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
# PROFIL OFFICIER
# =========================================================

@login_required
def profil_officier(request):
    user = request.user

    # Leurs cotisations
    cotisations = Cotisation.objects.filter(payeur=user)
    
    # Leur prêt actif ou en attente
    pret = None
    remboursements = []
    
    adherent = Adherent.objects.filter(mecano=user.mecano).first()
    
    if adherent:
        pret = Pret.objects.filter(
            adherent=adherent, 
            etat__in=[Pret.Etat.ACTIF, Pret.Etat.EN_ATTENTE]
        ).first()
        
        if pret:
            remboursements = Remboursement.objects.filter(pret=pret).order_by('-date_remboursement')
            
    activites = Audit.objects.filter(id_user=user).order_by("-date_heure")[:10]
        
    return render(
        request,
        "dashboard/profil-officier.html",
        {
            "cotisations": cotisations,
            "pret": pret,
            "remboursements": remboursements,
            "activites": activites,
        }
    )

@login_required
def officier_cotisations(request):
    from django.core.paginator import Paginator
    user = request.user
    cotisations_list = Cotisation.objects.filter(payeur=user).order_by("-date_paiement")
    
    paginator = Paginator(cotisations_list, 15)
    page_number = request.GET.get('page')
    cotisations = paginator.get_page(page_number)
    
    return render(request, "dashboard/officier-cotisations.html", {
        "cotisations": cotisations,
    })

@login_required
def officier_prets(request):
    from django.contrib import messages
    user = request.user
    
    adherent = Adherent.objects.filter(mecano=user.mecano).first()
    
    if request.method == "POST":
        montant = request.POST.get("montant")
        duree = request.POST.get("duree_remboursement")
        motif = request.POST.get("motif", "")
        
        try:
            m_val = float(montant)
            d_val = int(duree)
            if m_val < 1000 or m_val > 50000000:
                messages.error(request, "❌ Le montant doit être compris entre 1 000 et 50 000 000 FCFA.")
                return redirect("dashboard:officier-prets")
            if d_val < 1 or d_val > 120:
                messages.error(request, "❌ La durée de remboursement doit être comprise entre 1 et 120 mois.")
                return redirect("dashboard:officier-prets")
        except (TypeError, ValueError):
            messages.error(request, "❌ Les valeurs saisies (montant ou durée) sont invalides.")
            return redirect("dashboard:officier-prets")

        
        if adherent:
            pret_existant = Pret.objects.filter(
                adherent=adherent, 
                etat__in=[Pret.Etat.ACTIF, Pret.Etat.EN_ATTENTE]
            ).first()
            
            if pret_existant:
                messages.error(request, "❌ Vous avez déjà un prêt actif ou en attente.")
            else:
                from datetime import date
                Pret.objects.create(
                    adherent=adherent,
                    montant=montant,
                    date_pret=date.today(),
                    duree_remboursement=duree,
                    motif=motif,
                    etat=Pret.Etat.EN_ATTENTE
                )
                
                Audit.objects.create(
                    id_user=request.user,
                    operation_effectuee="CREATION",
                    type_modification="Demande de prêt",
                    donnees_avant=None,
                    donnees_apres={"montant": montant, "duree": duree},
                    nom_table="Pret"
                )
                messages.success(request, "Votre demande de prêt a été soumise avec succès. Elle est en attente de validation.")
        else:
            messages.error(request, "❌ Aucun matricule (mécano) trouvé pour votre profil.")
            
        return redirect("dashboard:officier-prets")
        
    prets = Pret.objects.filter(adherent=adherent) if adherent else []
    
    return render(request, "dashboard/officier-prets.html", {
        "prets": prets,
    })

@login_required
def officier_remboursements(request):
    from django.core.paginator import Paginator
    user = request.user
    adherent = Adherent.objects.filter(mecano=user.mecano).first()
    
    remboursements_list = []
    if adherent:
        remboursements_list = Remboursement.objects.filter(pret__adherent=adherent).order_by("-date_remboursement")
        
    paginator = Paginator(remboursements_list, 15)
    page_number = request.GET.get('page')
    remboursements = paginator.get_page(page_number)
        
    return render(request, "dashboard/officier-remboursements.html", {
        "remboursements": remboursements,
    })

@login_required
def officier_validation(request):
    from django.core.paginator import Paginator
    user = request.user
    adherent = Adherent.objects.filter(mecano=user.mecano).first()
    
    demandes_list = []
    if adherent:
        demandes_list = Pret.objects.filter(adherent=adherent, etat__in=[Pret.Etat.EN_ATTENTE, Pret.Etat.REFUSE, Pret.Etat.ACTIF]).order_by("-date_pret")
        
    paginator = Paginator(demandes_list, 15)
    page_number = request.GET.get('page')
    demandes = paginator.get_page(page_number)
        
    return render(request, "dashboard/officier-validation.html", {
        "demandes": demandes,
    })


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
    from django.core.paginator import Paginator

    # Récupérer toutes les cotisations
    cotisations_list = Cotisation.objects.select_related(
        "payeur"
    ).all().order_by("-date_paiement")

    # Nombre de cotisations (total)
    nombre_cotisations = cotisations_list.count()

    # Calcul du montant total
    montant_total = sum(
        cotisation.montant
        for cotisation in cotisations_list
    )
    
    paginator = Paginator(cotisations_list, 15)
    page_number = request.GET.get('page')
    cotisations_page = paginator.get_page(page_number)

    return render(
        request,
        "dashboard/cotisations.html",
        {
            "cotisations": cotisations_page,

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
    from django.contrib import messages

    if request.method == "POST":
        mecano = request.POST.get("mecano")
        montant = request.POST.get("montant")
        date_pret = request.POST.get("date_pret")
        duree = request.POST.get("duree_remboursement")
        motif = request.POST.get("motif", "")

        try:
            m_val = float(montant)
            d_val = int(duree)
            if m_val < 1000 or m_val > 50000000:
                messages.error(request, "❌ Le montant doit être compris entre 1 000 et 50 000 000 FCFA.")
                return redirect("dashboard:pret")
            if d_val < 1 or d_val > 120:
                messages.error(request, "❌ La durée doit être comprise entre 1 et 120 mois.")
                return redirect("dashboard:pret")
        except (TypeError, ValueError):
            messages.error(request, "❌ Les valeurs saisies (montant ou durée) sont invalides.")
            return redirect("dashboard:pret")

        try:
            adherent = Adherent.objects.get(mecano=mecano)

            pret_existant = Pret.objects.filter(
                adherent=adherent,
                etat__in=[Pret.Etat.ACTIF, Pret.Etat.EN_ATTENTE]
            ).first()
            if pret_existant:
                messages.error(request, f"❌ {adherent.nom} {adherent.prenom} a déjà un prêt actif ou en attente.")
                return redirect("dashboard:pret")

            Pret.objects.create(
                adherent=adherent,
                montant=montant,
                date_pret=date_pret,
                duree_remboursement=duree,
                motif=motif,
                etat=Pret.Etat.EN_ATTENTE
            )

            if request.user.is_authenticated:
                Audit.objects.create(
                    id_user=request.user,
                    operation_effectuee="CREATION",
                    type_modification="Enregistrement d'un prêt",
                    donnees_avant=None,
                    donnees_apres={"montant": montant, "date_pret": str(date_pret), "duree": duree},
                    nom_table="Pret"
                )

            messages.success(request, f"✅ La demande de prêt de {adherent.nom} {adherent.prenom} a été soumise avec succès.")
            return redirect("dashboard:pret")

        except Adherent.DoesNotExist:
            messages.error(request, "❌ Mécano introuvable. Veuillez vérifier le matricule.")

    prets_en_attente = Pret.objects.filter(
        etat=Pret.Etat.EN_ATTENTE
    ).select_related("adherent").order_by("-date_pret")

    tous_les_prets = Pret.objects.select_related("adherent").order_by("-date_pret")

    return render(
        request,
        "dashboard/pret.html",
        {
            "prets_en_attente": prets_en_attente,
            "prets_en_attente_count": prets_en_attente.count(),
            "tous_les_prets": tous_les_prets,
        }
    )


@login_required
def valider_pret(request, pret_id):
    from django.contrib import messages
    from django.shortcuts import get_object_or_404

    if request.method != "POST":
        return redirect("dashboard:pret")

    pret_obj = get_object_or_404(Pret, id=pret_id, etat=Pret.Etat.EN_ATTENTE)
    action = request.POST.get("action")

    if action == "valider":
        pret_obj.etat = Pret.Etat.ACTIF
        pret_obj.save()
        Audit.objects.create(
            id_user=request.user,
            operation_effectuee="VALIDATION",
            type_modification=f"Validation du prêt de {pret_obj.adherent.nom} {pret_obj.adherent.prenom}",
            donnees_avant={"etat": "EN_ATTENTE"},
            donnees_apres={"etat": "ACTIF", "montant": str(pret_obj.montant)},
            nom_table="Pret"
        )
        messages.success(request, f"✅ Le prêt de {pret_obj.adherent.nom} {pret_obj.adherent.prenom} ({int(pret_obj.montant):,} FCFA) a été validé.")
    elif action == "refuser":
        pret_obj.etat = Pret.Etat.REFUSE
        pret_obj.save()
        Audit.objects.create(
            id_user=request.user,
            operation_effectuee="REFUS",
            type_modification=f"Refus du prêt de {pret_obj.adherent.nom} {pret_obj.adherent.prenom}",
            donnees_avant={"etat": "EN_ATTENTE"},
            donnees_apres={"etat": "REFUSE"},
            nom_table="Pret"
        )
        messages.success(request, f"Le prêt de {pret_obj.adherent.nom} {pret_obj.adherent.prenom} a été refusé.")
    else:
        messages.error(request, "❌ Action invalide.")

    return redirect("dashboard:pret")



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
            m_verse = float(montant_verse)
            if m_verse <= 0:
                from django.contrib import messages
                messages.error(request, "❌ Le montant remboursé doit être supérieur à zéro.")
                return redirect("dashboard:remboursements")
        except (TypeError, ValueError):
            from django.contrib import messages
            messages.error(request, "❌ Le montant remboursé est invalide.")
            return redirect("dashboard:remboursements")

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

    operations = []

    # 1. COTISATIONS
    for c in Cotisation.objects.select_related("payeur").all():
        operations.append({
            "action": "Cotisation",
            "description": f"Cotisation mensuelle {c.mois_concerne.strftime('%m/%Y')} de {c.payeur.get_full_name() or c.payeur.username}",
            "date": c.date_paiement,
            "montant": c.montant,
        })

    # 2. PRÊTS
    for p in Pret.objects.select_related("adherent").all():
        operations.append({
            "action": "Prêt",
            "description": f"Prêt accordé à {p.adherent.nom} {p.adherent.prenom}",
            "date": p.date_pret,
            "montant": p.montant,
        })

    # 3. REMBOURSEMENTS
    for r in Remboursement.objects.select_related("pret__adherent").all():
        operations.append({
            "action": "Remboursement",
            "description": f"Versement de {r.pret.adherent.nom} {r.pret.adherent.prenom}",
            "date": r.date_remboursement,
            "montant": r.montant,
        })

    # Trier par date décroissante
    operations.sort(key=lambda x: x["date"], reverse=True)

    from django.core.paginator import Paginator
    paginator = Paginator(operations, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "dashboard/historique.html",
        {
            "historique_operations": page_obj,
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
        "dashboard:login"
    )