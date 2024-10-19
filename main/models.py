from django.db import models

# Create your models here.
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, UserManager
from django.db import models
from tinymce.models import HTMLField
import datetime


class App(models.Model):
    name    = models.CharField(max_length=450)
    mission = HTMLField("Notre mission",blank=True, null=True)
    working = HTMLField("Desc. fonction:",blank=True, null=True)
    email    =  models.EmailField("Email contact",null=True, blank=True)
    tel1     =  models.CharField("N° telephone 1 ",max_length=45,null=True, blank=True)
    tel2     =  models.CharField("N° telephone 2 ",max_length=45,null=True, blank=True)
    architecture =  models.ImageField(upload_to="media/computers/images/", null=True, blank=True)
    location = models.CharField(max_length=450, null=True, blank=True)
    logo     = models.ImageField(upload_to="media/computers/images/", null=True, blank=True)
    privacies= HTMLField(blank=True, null=True)
    copyright=models.CharField(max_length=450, blank=True, null=True)
    date_creation = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_creation"]
            
    def __str__(self) -> str:
        return f"{self.name}"

class Page(models.Model):
    name = models.CharField(max_length=250)
    date_creation = models.DateTimeField(auto_now=True)
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ["-date_creation", "name"]
        
    def __str__(self) -> str:
        return f"{self.name}"

class SliderInfo(models.Model):
    title       = models.CharField(max_length=450)
    description =  models.TextField(null=True, blank=True)
    position    = models.PositiveIntegerField(null=True, blank=True)
    page        =  models.ForeignKey(Page, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_creation"]
        
    def __str__(self) -> str:
        return f"{self.title}"


class usefulLink(models.Model):
    name = models.CharField(max_length=450)
    link = models.CharField(max_length=450)
    date_creation = models.DateTimeField(auto_now=True)
    app  = models.ForeignKey(App, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ["-date_creation"]
    def __str__(self) -> str:
        return f"{self.name}"

class userMessage(models.Model):
    fullname = models.CharField("Nom & Prenom", max_length=450)
    email    = models.EmailField("Email",null=True, blank=True)
    message  = models.TextField("Topic",null=True, blank=True)
    subject  = models.TextField("Message",null=True, blank=True)
    date_creation = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-date_creation"]
    def __str__(self) -> str:
        return f"{self.fullname}"

class Testimony(models.Model):
    fullname = models.CharField("Nom & Prenom",max_length=450)
    message  = models.TextField("Temoignage")
    address  = models.CharField("Adresse",max_length=450)
    date_creation = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-date_creation"]
    def __str__(self) -> str:
        return f"{self.fullname}"
