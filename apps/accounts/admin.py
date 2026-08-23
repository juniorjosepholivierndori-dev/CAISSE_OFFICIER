from django.contrib import admin

from .models import Adherent, MemberProfile, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "is_staff", "is_active")
    search_fields = ("username", "first_name", "last_name", "email")
    list_filter = ("is_staff", "is_active", "is_superuser")


@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ("matricule", "user", "grade", "unite", "telephone")
    search_fields = ("matricule", "user__username", "user__last_name", "user__first_name")
    list_filter = ("grade", "unite")


@admin.register(Adherent)
class AdherentAdmin(admin.ModelAdmin):
    list_display = ("matricule", "nom", "prenom", "user", "grade", "unite", "statut")
    list_select_related = ("user", "grade", "unite", "statut")
    search_fields = ("matricule", "nom", "prenom", "user__username")
    list_filter = ("grade", "unite", "statut")
