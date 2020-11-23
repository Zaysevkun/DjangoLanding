from django.db import models


class HeaderBlock(models.Model):
    title = models.CharField('Заголовок модуля', max_length=47)
    subtitle = models.CharField('Подзаголовок модуля', max_length=73)
