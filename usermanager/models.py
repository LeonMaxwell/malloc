import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.db import models
import datetime

# Create your models here.
from usermanager.manager import MallocUserManager


class MallocProfileUser(models.Model):
    login = models.CharField(max_length=256, verbose_name="Логин", unique=True)
    secret_keys = models.UUIDField(default=uuid.uuid4(), editable=False, unique=True, verbose_name="Секретный ключ")
    path_user = models.SlugField(max_length=255, verbose_name="Адрес пользователя", default=login)

    class Meta:
        abstract = True


class MediaMallocManagerUser(MallocProfileUser):
    class Meta:
        abstract = True

    photo_profile = models.ImageField(upload_to="{}/photos_profile".format(MallocProfileUser.login),
                                      verbose_name="Фото профиля", height_field=200, width_field=200)


class GeneralMallocManagerUser(MallocProfileUser):
    class Meta:
        abstract = True

    date_of_birth = models.DateField(datetime.date)
    number_profile = models.PositiveIntegerField(verbose_name="Номер телефона")
    language_user = models.CharField(max_length=255, verbose_name="Язык")
    personal_user_site = models.CharField(max_length=255, verbose_name="Личный сайт")
    about = models.TextField(null=True, blank=True, verbose_name="О себе")


class MallocBaseUser(AbstractBaseUser, PermissionsMixin, GeneralMallocManagerUser, MediaMallocManagerUser):
    email = models.EmailField(_('email address'), unique=True)
    password = models.CharField(_('password'), max_length=128)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(_('last_login'), blank=True, null=True)

    objects = MallocUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['login']

    class Meta:
        verbose_name = "Данные пользователя"
        verbose_name_plural = 'Данные пользователей'

    def __str__(self):
        return "{}:({} {})".format(self.pk, self.login, self.email)