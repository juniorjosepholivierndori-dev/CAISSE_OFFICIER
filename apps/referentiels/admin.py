from django.contrib import admin

from .models import Etablissement, Etat, Grade, Pays, Service, Statut, TypeService, Unite, Ville


for model in (Pays, Ville, Statut, Grade, Unite, TypeService, Service, Etablissement, Etat):
    admin.site.register(model)
