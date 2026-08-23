from django.contrib import admin

from .models import AuditOperation, Log


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ("date_heure", "operation", "type_modification", "utilisateur")
    list_filter = ("type_modification", "date_heure")
    search_fields = ("operation", "utilisateur__username")
    readonly_fields = ("date_heure",)


@admin.register(AuditOperation)
class AuditOperationAdmin(admin.ModelAdmin):
    list_display = ("date_operation", "operation", "type_operation", "utilisateur", "etat")
    list_filter = ("type_operation", "consommation", "mise_a_jour", "suppression")
    search_fields = ("operation__description", "utilisateur__username")
    readonly_fields = ("date_operation",)
