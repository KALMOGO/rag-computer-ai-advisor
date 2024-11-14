# models.py
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, keyword, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, keyword=keyword, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, keyword, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, keyword, password, **extra_fields)

    def create_superuser(self, email, keyword, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, keyword, password, **extra_fields)

class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=245, 
        null=True, 
        blank=True, 
        unique=False  # Important since we're using email as unique identifier
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        db_index=True  # Add index for better performance
    )
    tel1 = models.CharField(max_length=250, null=True, blank=True)
    tel2 = models.CharField(max_length=250, null=True, blank=True)
    last_name = models.CharField(max_length=280, null=True, blank=True)
    first_name = models.CharField(max_length=245, null=True, blank=True)
    photo = models.ImageField(
        upload_to='users/photos/', 
        null=True, 
        blank=True
    )
    keyword = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['keyword']

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_set',
        help_text='The groups this user belongs to.'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_permissions_set',
        help_text='Specific permissions for this user.'
    )

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['email']

    def __str__(self):
        return self.email

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.email

    def get_short_name(self):
        return self.first_name if self.first_name else self.email

    def clean(self):
        super().clean()
        self.email = self.email.lower()