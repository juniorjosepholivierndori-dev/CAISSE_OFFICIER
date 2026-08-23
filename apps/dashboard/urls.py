from django.urls import path

from .views import member_dashboard

app_name = "dashboard"

urlpatterns = [
    path("", member_dashboard, name="member"),
]
