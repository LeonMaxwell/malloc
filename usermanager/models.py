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
    path_user = models.SlugField(max_length=255, verbose_name="Адрес пользователя")

    class Meta:
        abstract = True


def user_directory_path(instance, filename):
    return '{}/{}/{}'.format(instance.login, instance.TYPE, filename)


class MediaMallocManagerUser(models.Model):
    TYPE = "photos_profile"

    class Meta:
        abstract = True

    photo_profile = models.ImageField(upload_to=user_directory_path,
                                      verbose_name="Фото профиля")


class GeneralMallocManagerUser(models.Model):
    GENDERS_USERS = (
        ('male', 'Мужской'),
        ('female', 'Женский')
    )

    class Meta:
        abstract = True

    date_of_birth = models.DateField(verbose_name="Дата рождения", blank=True, null=True)
    number_profile = models.CharField(max_length=255, verbose_name="Номер телефона")
    language_user = models.CharField(max_length=255, verbose_name="Язык")
    personal_user_site = models.CharField(max_length=255, verbose_name="Личный сайт")
    about = models.TextField(null=True, blank=True, verbose_name="О себе")
    gender = models.CharField(max_length=255, choices=GENDERS_USERS, verbose_name="Пол")
    city = models.CharField(max_length=255, verbose_name="Город")


class InterestingUserManager(models.Model):
    SPECIFICATION = (
        ('management', "Менеджмент"),
        ('web', "Разработка сайтов"),
        ('design', 'Дизайн и Арт'),
        ('programming', "Программирование"),
        ('seo', "Оптимизация (SEO)"),
        ("polygraphy", "Полиграфия"),
        ("text", "Тексты"),
        ("translate", "Переводы"),
        ("3dgraphics", "3D графика"),
        ("animations", "Анимация и Флэш"),
        ("photos", "Фотографии"),
        ("media", "Аудио/Видео"),
        ("advertising", "Реклама/Маркетинг"),
        ("gamedev", "Разработка игр"),
        ("architecture", "Архитектура/Интерьер"),
        ("engineering", "Инженеринг"),
        ("teacher", "Обучение и консультации"),
        ("mobile", "Разработка мобильных приложений"),
        ("net", "Сети")

    )

    class Meta:
        abstract = True

    education_type = models.CharField(max_length=255, verbose_name="Тип образования",
                                      help_text="Высшее/среднее/индивидуальное/удаленное/онлайн курс")
    theNameOfTheInstitution = models.CharField(max_length=255, verbose_name="Название учебного заведения",
                                               help_text="Указывать полное название учебного заведения")
    year_of_ending = models.CharField(max_length=255, verbose_name="Год окончания")
    name_specialty = models.CharField(max_length=255, verbose_name="Название специальности")
    type_specialisation = models.CharField(blank=True, null=True, max_length=255, choices=SPECIFICATION, verbose_name="Название специализации")
    skill_name = models.TextField(blank=True, null=True, verbose_name="Описание навыков")
    exp_spec = models.CharField(max_length=255, verbose_name="Опыт в специализации", blank=True, null=True)


class PortfolioUserManager(models.Model):
    TYPE = "portfolio_project"

    user_portfolio = models.ForeignKey("MallocBaseUser", on_delete=models.CASCADE, verbose_name="Проекты пользователя")
    name_project = models.CharField(max_length=255, verbose_name="Название проекта")
    about_project = models.TextField(blank=True, null=True, verbose_name="Описание проекта")
    project_view = models.ImageField(upload_to=user_directory_path, verbose_name="Представление проекта")
    used_tech = models.CharField(max_length=255, verbose_name="Использованные технологии")
    url_repos = models.CharField(max_length=255, verbose_name="Ссылка на репозиторий")

    class Meta:
        verbose_name = 'Портфолио пользователя'
        verbose_name_plural = 'Портфолио пользователей'

    def __str__(self):
        return self.name_project


class ContactInfoUser(models.Model):
    user_contacts = models.ForeignKey("MallocBaseUser", on_delete=models.CASCADE, verbose_name="Контакты")
    name_scoial = models.CharField(max_length=255, verbose_name="Название ресурса")
    user_url = models.CharField(max_length=255, verbose_name="Связь в ресурсе")

    class Meta:
        verbose_name = "Контактная информация пользователя"
        verbose_name_plural = "Контактные информации пользователей"

    def __str__(self):
        return "{} - {}({})".format(self.user_contacts.login, self.name_scoial, self.user_url)


class MallocBaseUser(AbstractBaseUser,
                     PermissionsMixin,
                     MallocProfileUser,
                     InterestingUserManager,
                     GeneralMallocManagerUser,
                     MediaMallocManagerUser):
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