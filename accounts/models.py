from django.db import models
from django.contrib.auth.models import BaseUserManager , AbstractBaseUser
import pycountry
# Create your models here.



class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, user_name, email, country, password=None):
        if not email:
            raise ValueError('User must have an email address!')
        if not user_name:
            raise ValueError('User must have a user name!')

        user = self.model(
            email=self.normalize_email(email),
            username=user_name,
            first_name=first_name,
            last_name=last_name,
            country=country
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_name, first_name, last_name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            user_name=user_name,
            first_name=first_name,
            last_name=last_name,
            country='MA',
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    @staticmethod
    def get_country():
        countries = list(pycountry.countries)
        return [(country.alpha_2, country.name) for country in countries]

    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=30, unique=True)
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    country = models.CharField(max_length=2, choices=get_country(), default="MA")
    is_premium = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
