from django.contrib import admin
from .models import Cotisation, Pret, Remboursement


@admin.register(Cotisation)
class CotisationAdmin(admin.ModelAdmin):
    list_display = ('id', 'membre', 'montant', 'date', 'type_cotisation')
    search_fields = ('membre__email', )


@admin.register(Pret)
class PretAdmin(admin.ModelAdmin):
    list_display = ('id', 'emprunteur', 'montant', 'solde_restant', 'statut', 'date_debut')
    search_fields = ('emprunteur__email', )


@admin.register(Remboursement)
class RemboursementAdmin(admin.ModelAdmin):
    list_display = ('id', 'pret', 'montant', 'date')
    search_fields = ('pret__id', )