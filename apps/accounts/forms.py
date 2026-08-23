from django import forms
from .models import Adherent
from apps.referentiels.models import Statut


class AdherentForm(forms.ModelForm):

    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput
    )

    confirm_password = forms.CharField(
        label="Confirmer le mot de passe",
        widget=forms.PasswordInput
    )

    statut = forms.ModelChoiceField(
        queryset=Statut.objects.all(),
        empty_label="Sélectionnez votre statut"
    )

    class Meta:
        model = Adherent

        fields = [
            "mecano",
            "nom",
            "prenom",
            "pays",
            "ville",
            "grade",
            "unite",
            "statut",
            "date_naissance",
            "telephone",
            "email",
            "password",
            "confirm_password",
        ]

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:

            if password != confirm_password:

                raise forms.ValidationError(
                    "Les deux mots de passe ne correspondent pas."
                )

        return cleaned_data

    def save(self, commit=True):

        adherant = super().save(commit=False)

        adherant.id_statut = self.cleaned_data["statut"]

        if commit:
            adherant.save()

        return adherant

