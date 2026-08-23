from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url="/connexion/")
def member_dashboard(request):
    return render(request, "dashboard/member.html")
