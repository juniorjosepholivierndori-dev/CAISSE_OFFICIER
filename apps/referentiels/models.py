from django.db import models


class Pays(models.Model):
    libelle_pays = models.CharField(max_length=100)
    indicatif = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = "Pays"
        verbose_name_plural = "Pays"

    def __str__(self):
        return self.libelle_pays


class Ville(models.Model):
    libelle_ville = models.CharField(max_length=150)
    code_postal = models.CharField(max_length=20, blank=True, null=True)
    pays = models.ForeignKey('Pays', on_delete=models.CASCADE, related_name='villes')

    def __str__(self):
        return self.libelle_ville


class Grade(models.Model):
    libelle = models.CharField(max_length=100)
    echelon = models.CharField(max_length=50)

    def __str__(self):
        return self.libelle


class Statut(models.Model):
    libelle = models.CharField(max_length=100)

    def __str__(self):
        return self.libelle


class Unite(models.Model):
    libelle_unite = models.CharField(max_length=150)
    adresse_unite = models.CharField(max_length=255, blank=True, null=True)
    ville = models.ForeignKey('Ville', on_delete=models.CASCADE, related_name='unites')

    def __str__(self):
        return self.libelle_unite


class TypeService(models.Model):
    libelle = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.libelle


class Service(models.Model):
    libelle_service = models.CharField(max_length=150)
    description_service = models.TextField(blank=True, null=True)
    type_service = models.ForeignKey('TypeService', on_delete=models.CASCADE, related_name='services')

    def __str__(self):
        return self.libelle_service


class Etablissement(models.Model):
    solde_actuel = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    type_etablissement = models.CharField(max_length=100)
    date_creation = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.type_etablissement