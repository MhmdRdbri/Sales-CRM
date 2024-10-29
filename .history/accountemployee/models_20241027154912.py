from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
import random
import asyncio
import http.client
import json

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone Number field must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone_number, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(unique=True, max_length=15)
    full_name = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(default='a@gmail.com')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Changed related name
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions '
                  'granted to each of their groups.',
        verbose_name='groups',
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Changed related name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.phone_number
        



class PasswordResetToken(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    token = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)

    @classmethod
    def create_code(cls, user):
        token = ''.join(random.choices('0123456789', k=6))
        expiration_time = timezone.now() + timezone.timedelta(minutes=2)
        return cls.objects.create(user=user, token=token)

    @classmethod
    def delete_code(cls, token):
        cls.objects.filter(token=token).delete()

    def is_expired(self):
        return self.expiration_time <= timezone.now()

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    fullname = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    WORK_POSITION_CHOICES = [
        ('admin', 'مدیر کل مجموعه'),
        ('system_manager', 'مدیر سامانه'),
        ('accountant', 'حسابدار'),
        ('regular', 'عادی'),
    ]
    work_position = models.CharField(max_length=20, choices=WORK_POSITION_CHOICES)
    department = models.CharField(max_length=255, blank=True, null=True)
    telegram_id = models.CharField(max_length=255, blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if not self.phone_number:
            self.phone_number = self.user.phone_number

        if self.phone_number != self.user.phone_number:
            self.user.phone_number = self.phone_number
            self.user.save()
            
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return f'پروفایل {self.name} {self.last_name} '