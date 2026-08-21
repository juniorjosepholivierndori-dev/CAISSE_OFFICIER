from django.contrib import admin
from .models import Pays, Ville, Grade, Statut, Unite, TypeService, Service, Etablissement

admin.site.register(Pays)
admin.site.register(Ville)
admin.site.register(Grade)
admin.site.register(Statut)
admin.site.register(Unite)
admin.site.register(TypeService)
admin.site.register(Service)
admin.site.register(Etablissement)