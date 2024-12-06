from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50, null = True, unique = True)
    email = models.EmailField(max_length=256, null = False, unique = True)
    password = models.CharField(max_length=50, null = False)