from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import User


@login_required
def profil_admin(request):
    nb_utilisateurs = User.objects.count()
    contexte = {
        'nb_utilisateurs': nb_utilisateurs,
    }
    return render(request, 'profil_admin.html', contexte)

@login_required
def liste_utilisateurs(request):
    utilisateurs = User.objects.all()
    return render(request, 'utilisateurs.html', {'utilisateurs': utilisateurs})


def logout_view(request):
    """Log the user out (accepts GET) and redirect to admin login."""
    logout(request)
    return redirect('/admin/login/')