from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        WAITER = "WAITER", "Ofitsiant"
        CUSTOMER = "CUSTOMER", "Foydalanuvchi"

    role = models.CharField(
        max_length=20, 
        choices=Role.choices, 
        default=Role.CUSTOMER
    )
    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser
    def is_waiter(self):
        return self.role == self.Role.WAITER
    def is_customer(self):
        return self.role == self.Role.CUSTOMER