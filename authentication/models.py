from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from helpers.models import TrackingModel


class UserManager(BaseUserManager):
    
    def create_user(self, email, password=None, country=None, phone_number=None, *args, **kwargs):

        if email is None:
            raise TypeError('Users should have an Email')
        
        user = self.model(email=self.normalize_email(email), country=country, phone_number=phone_number)
        user.set_password(password)
        user.save()
        return user
        
    def create_superuser(self, email, password=None, country=None, phone_number=None, *args, **kwargs):
        
        if password is None:
            raise TypeError('Password should not be none')
        
        user = self.create_user(email, password, country, phone_number)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
    
class User(AbstractBaseUser, PermissionsMixin, TrackingModel):
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    country = models.CharField(max_length=50, null=True)
    phone_number = models.IntegerField(null=True)
    is_verified=models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    def tokens(self):
        return ''