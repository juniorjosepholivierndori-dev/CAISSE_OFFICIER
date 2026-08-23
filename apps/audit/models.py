from django.conf import settings
from django.db import models


class Audit(models.Model):

    date_heure = models.DateTimeField(
        auto_now_add=True
    )

    operation_effectuee = models.CharField(
        max_length=100
    )

    type_modification = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    donnees_avant = models.JSONField(
        blank=True,
        null=True
    )

    donnees_apres = models.JSONField(
        blank=True,
        null=True
    )

    id_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    nom_table = models.CharField(
        max_length=100
    )

    class Meta:
        ordering = ["-date_heure"]

    def __str__(self):
        return f"{self.operation_effectuee} - {self.nom_table}"