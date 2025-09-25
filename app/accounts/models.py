from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    sub = models.CharField(max_length=255, unique=True, null=True, blank=True, db_index=True)
    email = models.EmailField(blank=True, default="",unique=True)
    phone = models.CharField(max_length=32, blank=True, default="")
    
    def __str__(self):
        return f"{self.email or self.phone}"
