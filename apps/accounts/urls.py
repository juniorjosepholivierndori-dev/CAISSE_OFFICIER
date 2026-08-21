from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('profil-admin/', views.profil_admin, name='profil_admin'),
    # logout route used by the admin UI (calls our logout_view which accepts GET)
    path('logout/', views.logout_view, name='logout'),
]