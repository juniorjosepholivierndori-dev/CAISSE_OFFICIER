from django.db import models


class Adherent(models.Model):

    mecano = models.CharField(
        max_length=50,
        unique=True
    )

    nom = models.CharField(
        max_length=100
    )

    prenom = models.CharField(
        max_length=100
    )

    grade = models.CharField(
        max_length=100
    )

    unite = models.CharField(
        max_length=150
    )

    pays = models.CharField(
        max_length=100
    )

    ville = models.CharField(
        max_length=100
    )

    statut = models.CharField(
        max_length=50
    )

    telephone = models.CharField(
        max_length=30
    )

    email = models.EmailField(
        unique=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["nom", "prenom"]

    def __str__(self):
        return f"{self.mecano} - {self.nom} {self.prenom}"