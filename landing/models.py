from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class HeaderBlock(models.Model):
    title = models.CharField('Заголовок модуля', max_length=47)
    subtitle = models.CharField('Подзаголовок модуля', max_length=73)
    left_button = models.CharField('текст левой кнопки',max_length=20)
    right_button = models.CharField('текст левой кнопки', max_length=20)


class ChatMessages(models.Model):
    message = models.CharField('Сообщение чата', max_length=30)


class Bullets(models.Model):
    bullet = models.CharField('элемент списка', max_length=32)


class List(models.Model):
    title = models.CharField('название элемента списка', max_length=20)
    text = models.TextField('текст элемента списка')


class ChatBlock(models.Model):
    title = models.CharField('Текст над изображением', max_length=16)
    image = models.FileField('Изображение')
    text = models.CharField('Текст под изображением', max_length=50)
    chat = models.ManyToManyField(ChatMessages, verbose_name='текст сообщений в чате')


class TwoTextBoxesBlock(models.Model):
    title = models.CharField('Заголовок модуля', max_length=47)
    subtitle = models.CharField('Подзаголовок модуля', max_length=73)
    top_text_block = models.TextField('верхний блок текста')
    bottom_text_block = models.TextField('нижний блок текста')


class FormLinkBlock(models.Model):
    title = models.CharField('Заголовок модуля', max_length=47)
    subtitle = models.CharField('Подзаголовок модуля', max_length=73)
    button_text = models.CharField('Текст кнопки', max_length=20)


class GridTextFieldsBlock(models.Model):
    title = models.CharField('Заголовок модуля', max_length=47)
    subtitle = models.CharField('Подзаголовок модуля', max_length=73)
    image_text_block = models.TextField('Текст у изображения')
    image = models.FileField('изображение')
    top_left_text_block = models.TextField('Левый верхний блок текста')
    top_right_text_block = models.TextField('Правый верхний блок текста')
    bottom_left_text_block = models.TextField('Левый нижний блок текста')
    bottom_right_text_block = models.TextField('Правый нижний блок текста')


class ProfileBlock(models.Model):
    title = models.CharField('Заголовок модуля', max_length=47)
    subtitle = models.CharField('Подзаголовок модуля', max_length=73)
    first_list = models.ManyToManyField(Bullets, verbose_name='Элементы списка')
    image = models.FileField('Изображение')
    text_under_image = models.TextField('Текст под изображением')
    second_list_title = models.CharField('Заголовок модуля', max_length=47)
    second_list = models.ManyToManyField(Bullets, verbose_name='Элементы списка')


class CourseBlock(models.Model):
    title = models.CharField('Заголовок модуля', max_length=47)
    subtitle = models.CharField('Подзаголовок модуля', max_length=73)
    sub_subtitle = models.CharField('Подзаголовок модуля', max_length=73)
    description = models.CharField('Описание модуля', max_length=47)
    price = models.PositiveSmallIntegerField('цена предмета')
    date = models.DateField('Дата начала')


class DropdownListBlock(models.Model):
    title = models.CharField('Заголовок модуля', max_length=47)
    list = models.ManyToManyField(List, verbose_name='выпадающий список')


class FAQBlock(models.Model):
    title = models.CharField('Заголовок модуля', max_length=47)
    FAQ = models.ManyToManyField(List, verbose_name='FAQ')


class FormBlock(models.Model):
    title = models.CharField('Заголовок модуля', max_length=47)
    bullet_list = models.ManyToManyField(Bullets, verbose_name='список')


# Define a model manager for User model with no username set
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'manager')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


# Custom User Class
class User(AbstractUser):
    class RoleChoices(models.TextChoices):
        CLIENT = 'client', 'Клиент'
        MANAGER = 'manager', 'Менеджер'

    username = None
    full_name = models.CharField('ФИО', max_length=100)
    role = models.CharField('Роль пользователя', max_length=10, choices=RoleChoices.choices,
                            default=RoleChoices.CLIENT)
    mailing_address = models.CharField('Адрес доставки', max_length=100)
    email = models.EmailField('Email', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.full_name

