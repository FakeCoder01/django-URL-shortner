from django.db import models

# Create your models here.

class links(models.Model):
    lid = models.CharField(max_length=8)
    link = models.CharField(max_length=1000)
    trough = models.CharField(max_length=5, blank=True)
    api_key = models.CharField(max_length=10, blank=True)
    created_on = models.DateTimeField()


#in-development
class authTokens(models.Model):
    email = models.EmailField(max_length=100)
    otp = models.IntegerField(max_length=6)
    verified = models.BooleanField()
    api_key = models.CharField(max_length=10, blank=True)
    status = models.CharField(max_length=8, blank=True)