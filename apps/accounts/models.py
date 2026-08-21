from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from apps.core.models import TimeStampedModel, SoftDeleteModel


class ROLES(models.TextChoices):
    ADMIN = "ADMIN", "Administrateur"
    TRESORIER = "TRESORIER", "Trésorier"
    OFFICIER = "OFFICIER", "Officier"


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est obligatoire.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", ROLES.ADMIN)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel, SoftDeleteModel):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLES.choices, default=ROLES.OFFICIER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    otp_active = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email