from django.contrib import admin

from .models import Notification, Operation, OperationPerso


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ("operation_date", "member", "type", "description", "amount", "status")
    list_filter = ("type", "status", "operation_date")
    search_fields = ("member__username", "description")
    date_hierarchy = "operation_date"


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("created_at", "member", "title", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = ("member__username", "title", "description")


@admin.register(OperationPerso)
class OperationPersoAdmin(admin.ModelAdmin):
    list_display = ("operation", "adherent", "utilisateur", "date_operation")
    list_select_related = ("operation", "adherent", "utilisateur")
    search_fields = ("adherent__matricule", "utilisateur__username")
