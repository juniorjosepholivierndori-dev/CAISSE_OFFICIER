from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrateur"
        TRESORIER = "TRESORIER", "Trésorier"
        OFFICIER = "OFFICIER", "Officier"

    class Statut(models.TextChoices):
        ACTIF = "ACTIF", "Actif"
        INACTIF = "INACTIF", "Inactif"
        RETRAITE = "RETRAITE", "Retraité"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.OFFICIER,
    )
    mecano = models.CharField(max_length=50, blank=True, null=True)
    grade = models.CharField(max_length=100, blank=True, null=True)
    unite = models.CharField(max_length=150, blank=True, null=True)
    statut = models.CharField(
        max_length=20,
        choices=Statut.choices,
        default=Statut.ACTIF,
        blank=True,
    )