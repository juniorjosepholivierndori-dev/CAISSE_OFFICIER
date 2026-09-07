import datetime

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

    payeur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="cotisations_payees"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-date_paiement"]

    def __str__(self):
        return f"Cotisation de {self.montant} FCFA"


class Pret(models.Model):

    class Etat(models.TextChoices):
        EN_ATTENTE = "EN_ATTENTE", "En attente"
        ACTIF = "ACTIF", "Actif"
        INACTIF = "INACTIF", "Inactif"
        REFUSE = "REFUSE", "Refusé"

    adherent = models.ForeignKey(
        "referentiels.Adherent",
        on_delete=models.PROTECT,
        related_name="prets"
    )

    montant = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    date_pret = models.DateField()

    motif = models.TextField(
        blank=True
    )

    duree_remboursement = models.PositiveIntegerField(
        help_text="Durée en mois"
    )

    etat = models.CharField(
        max_length=20,
        choices=Etat.choices,
        default=Etat.EN_ATTENTE
    )

    valide_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="prets_valides",
        null=True,
        blank=True
    )

    date_validation = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-date_pret"]

    def __str__(self):
        return f"Prêt de {self.montant} FCFA - {self.adherent}"

    @property
    def total_rembourse(self):
        """Somme de tous les remboursements liés à ce prêt."""
        return sum(r.montant for r in self.remboursements.all())

    @property
    def montant_restant(self):
        """Montant encore dû."""
        restant = self.montant - self.total_rembourse
        return max(restant, 0)

    @property
    def pourcentage_rembourse(self):
        """Pourcentage remboursé (0-100)."""
        if self.montant == 0:
            return 0
        pct = (self.total_rembourse / self.montant) * 100
        return min(int(pct), 100)


class Remboursement(models.Model):

    pret = models.ForeignKey(
        Pret,
        on_delete=models.PROTECT,
        related_name="remboursements"
    )

    montant = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    # Champ éditable : permet la saisie rétroactive d'une date de remboursement
    date_remboursement = models.DateField(
        default=datetime.date.today
    )

    mode_paiement = models.CharField(
        max_length=30
    )

    observation = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-date_remboursement"]

    def __str__(self):
        return f"Remboursement de {self.montant} FCFA"