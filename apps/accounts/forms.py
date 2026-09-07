import datetime

from django import forms
from django.contrib.auth import get_user_model

from apps.operations.models import Cotisation, Pret, Remboursement

User = get_user_model()


# =========================================================
# COTISATION
# =========================================================

class CotisationForm(forms.ModelForm):

    class Meta:
        model = Cotisation
        fields = ("montant", "mois_concerne", "mode_paiement", "payeur")
        widgets = {
            "mois_concerne": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "montant": "Montant (FCFA)",
            "mois_concerne": "Mois concerné",
            "mode_paiement": "Mode de paiement",
            "payeur": "Officier payeur",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # N'afficher que les utilisateurs actifs avec un label lisible
        self.fields["payeur"].queryset = User.objects.filter(
            statut="ACTIF"
        ).order_by("last_name", "first_name")
        self.fields["payeur"].label_from_instance = lambda u: (
            f"{u.get_full_name() or u.username}"
            + (f" — {u.grade}" if u.grade else "")
        )
        # Choix de mode de paiement
        self.fields["mode_paiement"].widget = forms.Select(choices=[
            ("", "— Choisir —"),
            ("ESPECES", "Espèces"),
            ("VIREMENT", "Virement bancaire"),
            ("MOBILE_MONEY", "Mobile Money"),
            ("CHEQUE", "Chèque"),
        ])


# =========================================================
# PRÊT
# =========================================================

class PretForm(forms.ModelForm):

    class Meta:
        model = Pret
        fields = ("adherent", "montant", "date_pret", "motif", "duree_remboursement")
        widgets = {
            "date_pret": forms.DateInput(attrs={"type": "date"}),
            "motif": forms.Textarea(attrs={"rows": 3}),
        }
        labels = {
            "adherent": "Adhérent",
            "montant": "Montant du prêt (FCFA)",
            "date_pret": "Date du prêt",
            "motif": "Motif (facultatif)",
            "duree_remboursement": "Durée de remboursement (mois)",
        }


# =========================================================
# REMBOURSEMENT
# =========================================================

class RemboursementForm(forms.ModelForm):

    class Meta:
        model = Remboursement
        fields = ("pret", "montant", "date_remboursement", "mode_paiement", "observation")
        widgets = {
            "date_remboursement": forms.DateInput(attrs={"type": "date"}),
            "observation": forms.Textarea(attrs={"rows": 2}),
        }
        labels = {
            "pret": "Prêt concerné",
            "montant": "Montant versé (FCFA)",
            "date_remboursement": "Date du remboursement",
            "mode_paiement": "Mode de paiement",
            "observation": "Observation (facultatif)",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # N'afficher que les prêts actifs
        self.fields["pret"].queryset = Pret.objects.filter(
            etat=Pret.Etat.ACTIF
        ).select_related("adherent").order_by("adherent__nom")
        self.fields["pret"].label_from_instance = lambda p: (
            f"{p.adherent.nom} {p.adherent.prenom} — {p.montant} FCFA"
        )
        # Valeur par défaut : aujourd'hui
        if not self.initial.get("date_remboursement"):
            self.initial["date_remboursement"] = datetime.date.today()
        # Choix de mode de paiement
        self.fields["mode_paiement"].widget = forms.Select(choices=[
            ("", "— Choisir —"),
            ("ESPECES", "Espèces"),
            ("VIREMENT", "Virement bancaire"),
            ("MOBILE_MONEY", "Mobile Money"),
            ("CHEQUE", "Chèque"),
        ])


# =========================================================
# PARAMÈTRES ADMINISTRATEUR
# =========================================================

class AdminProfileForm(forms.ModelForm):
    new_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Laisser vide pour ne pas modifier"}),
        label="Nouveau mot de passe",
    )
    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Confirmer le nouveau mot de passe"}),
        label="Confirmer le mot de passe",
    )

    class Meta:
        model = User
        fields = ("last_name", "first_name", "email", "grade", "unite")
        labels = {
            "last_name": "Nom",
            "first_name": "Prénom",
            "email": "Adresse e-mail",
            "grade": "Grade",
            "unite": "Unité",
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("new_password")
        confirmation = cleaned_data.get("confirm_password")
        if password or confirmation:
            if password != confirmation:
                raise forms.ValidationError(
                    "Les mots de passe ne correspondent pas."
                )
            if password and len(password) < 8:
                raise forms.ValidationError(
                    "Le mot de passe doit contenir au moins 8 caractères."
                )
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get("new_password"):
            user.set_password(self.cleaned_data["new_password"])
        if commit:
            user.save()
        return user


# =========================================================
# GESTION UTILISATEURS
# =========================================================

class UserManagementForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Laisser vide pour ne pas modifier"}
        ),
        label="Mot de passe",
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "mecano",
            "grade",
            "unite",
            "statut",
            "password",
        )
        labels = {
            "username": "Nom d'utilisateur",
            "email": "Email",
            "first_name": "Prénom",
            "last_name": "Nom",
            "role": "Rôle",
            "mecano": "Matricule",
            "grade": "Grade",
            "unite": "Unité",
            "statut": "Statut",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["statut"].choices = (
            ("ACTIF", "Actif"),
            ("INACTIF", "Inactif"),
            ("RETRAITE", "Retraité"),
        )

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password and len(password) < 8:
            raise forms.ValidationError(
                "Le mot de passe doit contenir au moins 8 caractères."
            )
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
