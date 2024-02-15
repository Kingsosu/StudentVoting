# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
import uuid

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None, matric_number=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        if not username:
            raise ValueError(_('The Username field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, matric_number=matric_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, username, password, **extra_fields)

def get_profile_image_filepath(self, filename):
    return 'profile_images/' + str(self.pk) + '/profile_image.png'
    # return f'profile_images/{str(self.pk)}/{"profile_image.png"}'

def get_profile_image():
    return f'kscode/profile_image.png'

class Account(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('username'), max_length=150, unique=True)
    matric_number = models.CharField(_('matric number'), max_length=20, blank=True, null=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    
    profile_image = models.ImageField(upload_to=get_profile_image_filepath, default=get_profile_image, blank=True, null=True)
    
    is_student = models.BooleanField(default=False)
    is_candidate = models.BooleanField(default=False)

    
    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def get_profile_image_filepath(self):
        return str(self.profile_image)[str(self.profile_image).index('profile_images/' + str(self.pk) + "/"):]
        # return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{str(self.pk)}/'):]


    class Meta:
        verbose_name = _('account')
        verbose_name_plural = _('accounts')

    def __str__(self):
        return self.username
