from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager

# Create your models here.
class CustomAccountManager(BaseUserManager):
    def create_user(self,username,email,first_name,password,**other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))
        email=self.normalize_email(email)
        user=self.model(username=username,email=email,first_name=first_name,password=password,**other_fields)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self,username,email,first_name,password,**other_fields):
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_active',True)
        other_fields.setdefault('is_superuser',True)
        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff =True')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser =True')
        return self.create_user(username,email,first_name,password,**other_fields)

class NewUser(AbstractBaseUser,PermissionsMixin):
    username=models.CharField(max_length=150,unique=True)
    email=models.EmailField(_('email address'),unique=True)
    first_name=models.CharField(max_length=150)
    last_name=models.CharField(max_length=150)
    start_date=models.DateTimeField(default=timezone.now)
    about=models.TextField(_('about'),max_length=500,blank=True)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    objects=CustomAccountManager()

    USERNAME_FIELD='username'
    REQUIRED_FIELDS=['email','first_name']
    def __str__(self):
        return self.username
