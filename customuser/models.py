from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.


class CustomUserManager(BaseUserManager):
    def _create_user(self, username, email, password, **kwargs):
        """
        Create a user with the given username, email, password and 
        other fields.
        """
        if not email:
            raise ValueError("Email cannot be empty.")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **kwargs)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, **kwargs):
        kwargs.setdefault("is_staff", False)
        kwargs.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **kwargs)

    def create_superuser(self, username, email, password, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        if kwargs.get("is_superuser") is False:
            raise ValueError("Superuser must have is_superuser set to True")
        if kwargs.get("is_staff") is False:
            raise ValueError("Superuser must have is_staff set to True")
        return self._create_user(username, email, password, **kwargs)


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    is_staff = models.BooleanField(default=False)
    is_worker = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self) -> str:
        return f"{self.username}"

    def is_receptionist(self):
        """
        Check if a user is a receptionist.
        """
        return self.groups.filter(name="reception").exists()
    
    def is_manager(self):
        """
        Check if a user is a manager.
        """
        return self.groups.filter(name="manager").exists()