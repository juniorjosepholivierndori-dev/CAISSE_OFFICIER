from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password

from .forms import AdherentForm
from .models import User


def inscription(request):

    if request.method == "POST":
        form = AdherentForm(request.POST)

        if form.is_valid():

            # Récupérer les données du formulaire
            adherent = form.save(commit=False)

            # Récupérer le mot de passe
            password = form.cleaned_data["password"]

            # Enregistrer l'adhérent
            adherent.save()

            # Créer le compte utilisateur
            utilisateur = User.objects.create(
                login=adherent.mecano,
                role="officier",
                id_adherant=adherent,
                password=make_password(password)
            )

            return redirect("inscription_reussie")

    else:
        form = AdherentForm()

    return render(
        request,
        "inscription.html",
        {"form": form}
    )