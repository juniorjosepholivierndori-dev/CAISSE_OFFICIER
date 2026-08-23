from django.conf import settings
from django.db import models

from apps.operations.models import Operation
from apps.referentiels.models import Etat


class Log(models.Model):
    operation = models.CharField(max_length=100)
    date_heure = models.DateTimeField(auto_now_add=True)
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="logs")
    type_modification = models.CharField(max_length=50)
    donnees_avant = models.JSONField(default=dict, blank=True)
    donnees_apres = models.JSONField(default=dict, blank=True)
    id_user = models.BigIntegerField(null=True, blank=True)

    class Meta:
        ordering = ["-date_heure"]

    def __str__(self):
        return f"{self.operation} - {self.date_heure:%Y-%m-%d %H:%M}"


class AuditOperation(models.Model):
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, related_name="audits")
    type_operation = models.CharField(max_length=100)
    consommation = models.BooleanField(default=False)
    mise_a_jour = models.BooleanField(default=False)
    suppression = models.BooleanField(default=False)
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="audits_operation")
    etat = models.ForeignKey(Etat, on_delete=models.PROTECT, null=True, blank=True, related_name="audits")
    date_operation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_operation"]

    def __str__(self):
        return f"Audit opération #{self.operation_id}"
