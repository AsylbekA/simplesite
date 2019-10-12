from django.db import models
from django.core import validators
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class MinMaxValueValidator:
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

    def __call__(self, val):
        if val < self.min_value or val > self.max_value:
            raise ValidationError('Введенное число должно' +\
                                  'находиться в диапозоне от %(min)s до %(max)s',
                                  code='out_of_range',
                                  params={'min': self.min_value, 'max': self.max_value})


def validate_even(val):
    if val % 2 != 0:
        raise ValidationError('Число %(value)s нечетное',
                              code='odd', params={'value': val})


class AdvUser(models.Model):
    is_activated = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Spare(models.Model):
    name = models.CharField(max_length=30)


class Machine(models.Model):
    name = models.CharField(max_length=30)
    spares = models.ManyToManyField(Spare)


class Bb(models.Model):
    title = models.CharField(max_length=50, verbose_name='Товар',
                             validators=[validators.RegexValidator(regex='^.{4,}$')],
                             error_messages={'invalid': 'Неправильно называние товара'})
    content = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(null=True, blank=True, verbose_name='Цена', validators=[validate_even])
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    rubric = models.ForeignKey('Rubric', null=True, on_delete=models.PROTECT, verbose_name='Рубрика')

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['-published', 'title']

    def __str__(self):
        return self.title


class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='Называние')

    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['-name']

    def __str__(self):
        return self.name
