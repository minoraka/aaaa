from datetime import date

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


def current_year():
    return date.today().year


class Student(AbstractUser):
    class Gender(models.TextChoices):
        MALE = 'М', 'М'
        FEMALE = 'Ж', 'Ж'

    class Course(models.IntegerChoices):
        FIRST = 1, '1'
        SECOND = 2, '2'
        THIRD = 3, '3'
        FOURTH = 4, '4'

    class EducationForm(models.TextChoices):
        FULL_TIME = 'очная', 'Очная'
        EXTRAMURAL = 'заочная', 'Заочная'
        EVENING = 'вечерняя', 'Вечерняя'

    class Funding(models.TextChoices):
        BUDGET = 'бюджет', 'Бюджет'
        CONTRACT = 'контракт', 'Контракт'

    class Status(models.TextChoices):
        STUDYING = 'обучается', 'Обучается'
        ACADEMIC_LEAVE = 'академический отпуск', 'Академический отпуск'
        EXPELLED = 'отчислен', 'Отчислен'
        GRADUATED = 'выпускник', 'Выпускник'

    middle_name = models.CharField('Отчество', max_length=100, blank=True)
    birth_date = models.DateField('Дата рождения', null=True, blank=True)
    gender = models.CharField('Пол', max_length=1, choices=Gender.choices, blank=True)
    phone = models.CharField('Телефон', max_length=20, blank=True)
    address = models.TextField('Адрес', blank=True)
    photo = models.ImageField('Фото', upload_to='students/', blank=True, null=True)

    student_id = models.CharField('Номер студенческого билета', max_length=20, unique=True)
    group = models.ForeignKey(
        'academics.Group', verbose_name='Группа', on_delete=models.PROTECT,
        related_name='students', null=True, blank=True)
    course = models.PositiveSmallIntegerField('Курс', choices=Course.choices, default=1)
    admission_year = models.PositiveSmallIntegerField('Год поступления', default=current_year)
    education_form = models.CharField(
        'Форма обучения', max_length=20,
        choices=EducationForm.choices, default=EducationForm.FULL_TIME)
    funding = models.CharField(
        'Основа обучения', max_length=20,
        choices=Funding.choices, default=Funding.BUDGET)
    status = models.CharField(
        'Статус', max_length=30,
        choices=Status.choices, default=Status.STUDYING)

    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлён', auto_now=True)

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
        ordering = ['last_name', 'first_name']

    @property
    def full_name(self):
        return ' '.join(p for p in (self.last_name, self.first_name, self.middle_name) if p)

    def __str__(self):
        return f'{self.full_name or self.username} ({self.group})'

    def get_absolute_url(self):
        return reverse('students:detail', args=[self.pk])
