from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrateur"
        TRESORIER = "TRESORIER", "Trésorier"
        OFFICIER = "OFFICIER", "Officier"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.OFFICIER,
    )