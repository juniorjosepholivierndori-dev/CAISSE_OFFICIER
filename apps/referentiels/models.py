from django.db import models


class Pays(models.Model):
    id_pays = models.AutoField(primary_key=True)

    libelle_pays = models.CharField(max_length=100)

    indicatif = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        db_table = "pays"

    def __str__(self):
        return self.libelle_pays


class Ville(models.Model):
    id_ville = models.AutoField(primary_key=True)

    id_pays = models.ForeignKey(
        Pays,
        on_delete=models.PROTECT,
        db_column="id_pays"
    )

    libelle_ville = models.CharField(max_length=100)

    code_postal = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = "ville"

    def __str__(self):
        return self.libelle_ville


class Grade(models.Model):
    id_grade = models.AutoField(primary_key=True)

    libelle_grade = models.CharField(max_length=100)

    echelon = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = "grade"

    def __str__(self):
        return self.libelle_grade


class Unite(models.Model):
    id_unite = models.AutoField(primary_key=True)

    libelle_unite = models.CharField(max_length=150)

    id_ville = models.ForeignKey(
        Ville,
        on_delete=models.PROTECT,
        db_column="id_ville",
        null=True,
        blank=True
    )

    adresse_unite = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "unite"

    def __str__(self):
        return self.libelle_unite


class Statut(models.Model):
    id_statut = models.AutoField(primary_key=True)

    libelle_statut = models.CharField(max_length=100)

    class Meta:
        db_table = "statut"

    def __str__(self):
        return self.libelle_statut