from django.shortcuts import render, redirect
from .forms import AdherentForm
from .models import User


def inscription(request):

    if request.method == "POST":

        form = AdherentForm(request.POST)

        if form.is_valid():

            adherant = form.save()

            user = User(
                login=adherant.mecano,
                id_adherant=adherant
            )

            user.set_password(
                form.cleaned_data["password"]
            )

            user.save()

            return redirect("inscription_reussie")

    else:

        form = AdherentForm()

    return render(
        request,
        "inscription.html",
        {"form": form}
    )


def inscription_reussie(request):
    return render(request, "inscription-reussie.html")


def connexion(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(
                id_adherant__email=email
            )

            if user.check_password(password):
                return render(
                    request,
                    "connexion.html",
                    {
                        "success": "Connexion réussie !"
                    }
                )

            else:
                return render(
                    request,
                    "connexion.html",
                    {
                        "error": "Email ou mot de passe incorrect."
                    }
                )

        except User.DoesNotExist:
            return render(
                request,
                "connexion.html",
                {
                    "error": "Email ou mot de passe incorrect."
                }
            )

    return render(
        request,
        "connexion.html"
    )