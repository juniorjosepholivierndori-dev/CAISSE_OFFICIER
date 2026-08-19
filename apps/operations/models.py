from django.conf import settings
from django.db import models


class Cotisation(models.Model):
    montant = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    date_paiement = models.DateField(
        auto_now_add=True
    )

    mois_concerne = models.DateField()

    mode_paiement = models.CharField(
        max_length=30
    )

    enregistre_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="cotisations_enregistrees"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-date_paiement"]

    def __str__(self):
        return f"Cotisation de {self.montant} FCFA"