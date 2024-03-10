from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, name, email, permission, password=None):
        if not email:
            raise ValueError("Kötelező email-t megadni")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, permission=permission)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, name, email, permission, password=None):
        user = self.create_user(
            name=name,
            email=email,
            permission=permission,
            password=password
        )
        user.permission = "admin"
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class UserModel(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    permission = models.CharField(max_length=50, default="basic")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "permission"]

    def __str__(self):
        return self.email
