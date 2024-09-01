from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    role = models.CharField(max_length=10, choices=(
        ('Admin', 'Admin'),
        ('Operator', 'Operator')
    ))
    
    def __str__(self) -> str:
        return self.username
