from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

from apps.referentiels.models import Grade, Statut, Unite, Ville


class User(AbstractUser):
    """Utilisateur de la caisse, compatible avec AUTH_USER_MODEL."""


class MemberProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="member_profile")
    matricule = models.CharField(max_length=30, unique=True)
    grade = models.CharField(max_length=100, blank=True)
    unite = models.CharField(max_length=150, blank=True)
    telephone = models.CharField(max_length=30, blank=True)

    class Meta:
        ordering = ["matricule"]

    def __str__(self):
        return f"{self.matricule} - {self.user.get_full_name() or self.user.username}"


class Adherent(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="adherent")
    matricule = models.CharField(max_length=30, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    telephone = models.CharField(max_length=30, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    lieu_naissance = models.ForeignKey(Ville, on_delete=models.PROTECT, null=True, blank=True, related_name="adherents_nes")
    adresse = models.CharField(max_length=255, blank=True)
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT, null=True, blank=True, related_name="adherents")
    unite = models.ForeignKey(Unite, on_delete=models.PROTECT, null=True, blank=True, related_name="adherents")
    statut = models.ForeignKey(Statut, on_delete=models.PROTECT, null=True, blank=True, related_name="adherents")
    date_adhesion = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["matricule"]

    def __str__(self):
        return f"{self.matricule} - {self.nom} {self.prenom}"
