from datetime import date

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


def current_year():
    return date.today().year


class Faculty(models.Model):
    name = models.CharField('Название', max_length=200, unique=True)
    short_name = models.CharField('Сокращённое название', max_length=30, unique=True)
    dean = models.CharField('Декан', max_length=150)

    class Meta:
        verbose_name = 'Факультет'
        verbose_name_plural = 'Факультеты'
        ordering = ['name']

    def __str__(self):
        return self.name


class Direction(models.Model):
    code = models.CharField('Код', max_length=20, unique=True)
    name = models.CharField('Название', max_length=200)
    faculty = models.ForeignKey(
        Faculty, verbose_name='Факультет',
        on_delete=models.PROTECT, related_name='directions')
    duration_years = models.PositiveSmallIntegerField(
        'Срок обучения (лет)', default=4,
        validators=[MinValueValidator(1), MaxValueValidator(10)])

    class Meta:
        verbose_name = 'Направление'
        verbose_name_plural = 'Направления'
        ordering = ['code']

    def __str__(self):
        return f'{self.code} {self.name}'


class Group(models.Model):
    name = models.CharField('Название', max_length=20, unique=True)
    direction = models.ForeignKey(
        Direction, verbose_name='Направление',
        on_delete=models.PROTECT, related_name='groups')
    admission_year = models.PositiveSmallIntegerField('Год набора', default=current_year)
    is_active = models.BooleanField('Активна', default=True)

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ['name']

    def __str__(self):
        return self.name
