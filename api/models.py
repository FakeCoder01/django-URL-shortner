from django.db import models

# Create your models here.

class links(models.Model):
    lid = models.CharField(max_length=8)
    link = models.CharField(max_length=1000)
    trough = models.CharField(max_length=5, blank=True)
    api_key = models.CharField(max_length=10, blank=True)
    created_on = models.DateTimeField()

    def __str__(self) :
        return self.lid

#in-development
class authTokens(models.Model):
    email = models.EmailField(max_length=100)
    psw = models.CharField(max_length=10)
    otp = models.IntegerField(max_length=6)
    api_key = models.CharField(max_length=10, blank=True)
    status = models.CharField(max_length=8, blank=True)
    created_on = models.DateTimeField()

    def __str__(self) :
        return self.email
