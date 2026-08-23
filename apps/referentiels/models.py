from django.db import models


class Pays(models.Model):
    libelle_pays = models.CharField(max_length=100, unique=True)
    code_iso = models.CharField(max_length=3, unique=True)

    class Meta:
        ordering = ["libelle_pays"]
        verbose_name = "Pays"
        verbose_name_plural = "Pays"

    def __str__(self):
        return self.libelle_pays


class Ville(models.Model):
    pays = models.ForeignKey(Pays, on_delete=models.PROTECT, related_name="villes")
    libelle_ville = models.CharField(max_length=100)
    code_postal = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ["libelle_ville"]
        constraints = [models.UniqueConstraint(fields=["pays", "libelle_ville"], name="unique_ville_pays")]

    def __str__(self):
        return self.libelle_ville


class Statut(models.Model):
    libelle_statut = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.libelle_statut


class Grade(models.Model):
    libelle_grade = models.CharField(max_length=100, unique=True)
    echelon = models.CharField(max_length=30, blank=True)

    class Meta:
        ordering = ["libelle_grade"]

    def __str__(self):
        return self.libelle_grade


class Unite(models.Model):
    libelle_unite = models.CharField(max_length=150, unique=True)
    ville = models.ForeignKey(Ville, on_delete=models.PROTECT, related_name="unites")
    adresse_unite = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["libelle_unite"]

    def __str__(self):
        return self.libelle_unite


class TypeService(models.Model):
    libelle_type_service = models.CharField(max_length=150, unique=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.libelle_type_service


class Service(models.Model):
    libelle_service = models.CharField(max_length=150, unique=True)
    type_service = models.ForeignKey(TypeService, on_delete=models.PROTECT, related_name="services")
    description_service = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["libelle_service"]

    def __str__(self):
        return self.libelle_service


class Etablissement(models.Model):
    libelle_etablissement = models.CharField(max_length=150, unique=True)
    solde_actuel = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    type_etablissement = models.CharField(max_length=100, blank=True)
    date_creation = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.libelle_etablissement


class Etat(models.Model):
    libelle_etat = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.libelle_etat
