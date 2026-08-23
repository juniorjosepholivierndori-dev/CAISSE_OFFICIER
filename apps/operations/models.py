from django.conf import settings
from django.db import models

from apps.accounts.models import Adherent
from apps.referentiels.models import Etat, Etablissement, Service


class Operation(models.Model):
    class Type(models.TextChoices):
        COTISATION = "cotisation", "Cotisation"
        PRET = "pret", "Prêt"
        REMBOURSEMENT = "remboursement", "Remboursement"

    class Status(models.TextChoices):
        PENDING = "attente", "En attente"
        VALIDATED = "valide", "Validée"
        REFUSED = "refuse", "Refusée"

    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="operations")
    adherent = models.ForeignKey(Adherent, on_delete=models.PROTECT, null=True, blank=True, related_name="operations")
    service = models.ForeignKey(Service, on_delete=models.PROTECT, null=True, blank=True, related_name="operations")
    etat = models.ForeignKey(Etat, on_delete=models.PROTECT, null=True, blank=True, related_name="operations")
    etablissement = models.ForeignKey(Etablissement, on_delete=models.PROTECT, null=True, blank=True, related_name="operations")
    type = models.CharField(max_length=20, choices=Type.choices)
    description = models.CharField(max_length=255)
    amount = models.PositiveBigIntegerField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    operation_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-operation_date", "-created_at"]
        indexes = [
            models.Index(fields=["member", "type"]),
            models.Index(fields=["member", "status"]),
        ]

    def __str__(self):
        return f"{self.get_type_display()} - {self.amount} FCFA"


class OperationPerso(models.Model):
    operation = models.OneToOneField(Operation, on_delete=models.CASCADE, related_name="operation_perso")
    adherent = models.ForeignKey(Adherent, on_delete=models.PROTECT, related_name="operations_personnelles")
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="operations_personnelles_creees")
    date_operation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Opération personnelle #{self.operation_id}"


class Notification(models.Model):
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=150)
    description = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
