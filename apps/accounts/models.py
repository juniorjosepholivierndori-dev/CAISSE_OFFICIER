from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models


class Adherent(models.Model):
    id_adherant = models.AutoField(primary_key=True)

    mecano = models.CharField(max_length=50, unique=True)

    nom = models.CharField(max_length=100)

    prenom = models.CharField(max_length=100)
    pays = models.CharField(max_length=100)

    ville = models.CharField(max_length=100)

    grade = models.CharField(max_length=100)

    unite = models.CharField(max_length=150)

    id_statut = models.ForeignKey(
        "referentiels.Statut",
        on_delete=models.PROTECT,
        db_column="id_statut"
    )

    date_naissance = models.DateField()

    telephone = models.CharField(max_length=30)

    email = models.EmailField(max_length=150, unique=True)

    class Meta:
        db_table = "adherant"

    def __str__(self):
        return f"{self.nom} {self.prenom}"


class ROLES(models.TextChoices):
    ADMIN = "admin", "Administrateur"
    GESTIONNAIRE = "gestionnaire", "Gestionnaire"
    OFFICIER = "officier", "Officier"


class User(AbstractBaseUser, PermissionsMixin):
    id_user = models.AutoField(primary_key=True)

    login = models.CharField(max_length=100, unique=True)

    role = models.CharField(
        max_length=50,
        choices=ROLES.choices,
        default=ROLES.OFFICIER
    )

    id_adherant = models.OneToOneField(
        Adherent,
        on_delete=models.PROTECT,
        db_column="id_adherant",
        related_name="utilisateur"
    )

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "login"

    class Meta:
        db_table = "utilisateur"

    def __str__(self):
        return self.login