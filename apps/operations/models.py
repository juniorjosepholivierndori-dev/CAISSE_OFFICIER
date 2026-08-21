from django.db import models
from django.conf import settings


class Cotisation(models.Model):
    membre = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cotisations')
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    type_cotisation = models.CharField(max_length=100, blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Cotisation"
        verbose_name_plural = "Cotisations"

    def __str__(self):
        return f"Cotisation {self.id} - {self.membre} - {self.montant}"


class Pret(models.Model):
    emprunteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='prets')
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    taux_annuel = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    date_debut = models.DateField(auto_now_add=True)
    duree_mois = models.PositiveIntegerField(default=12)
    solde_restant = models.DecimalField(max_digits=12, decimal_places=2)
    statut = models.CharField(max_length=30, default='EN_COURS')

    class Meta:
        verbose_name = "Prêt"
        verbose_name_plural = "Prêts"

    def __str__(self):
        return f"Prêt {self.id} - {self.emprunteur} - {self.montant}"


class Remboursement(models.Model):
    pret = models.ForeignKey(Pret, on_delete=models.CASCADE, related_name='remboursements')
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Remboursement"
        verbose_name_plural = "Remboursements"

    def __str__(self):
        return f"Remboursement {self.id} - Pret {self.pret.id} - {self.montant}"