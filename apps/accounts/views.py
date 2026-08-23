from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render


def member_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard:member")

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("dashboard:member")
    return render(request, "accounts/login.html", {"form": form})
