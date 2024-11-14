from django.db import models
from  ..computers.models import Computer

class Commend(models.Model):
    first_name = models.CharField(max_length=250)
    last_name  = models.CharField(max_length=250)
    computer   = models.ForeignKey(Computer, related_name = "commend",on_delete=models.CASCADE)
    phone      = models.CharField(max_length=250)
    number     = models.PositiveIntegerField(default=1)
    email      = models.EmailField(null=True, blank=True)
    creation_date  = models.DateTimeField(auto_now_add=True)
    delivery_date  = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    location   = models.CharField(max_length=250)
    is_traited = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "User commend"
        ordering = ("-creation_date",)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class UserInfo(models.Model):
    ip    = models.CharField(max_length=250)
    city  = models.CharField(max_length=250)
    country     = models.CharField(max_length=250)
    region      = models.CharField(max_length=250)
    creation_date  = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Information utilisateur"
        ordering = ("-creation_date",)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class TokensList(models.Model):
    number = models.CharField(max_length=250)
    creation_date  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-creation_date',)
    
    def __str__(self):
        return f"{self.number }{self.creation_date}"