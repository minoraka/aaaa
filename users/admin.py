from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Student


@admin.register(Student)
class StudentAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Личные данные', {'fields': ('middle_name', 'birth_date', 'gender',
                                      'phone', 'address', 'photo')}),
        ('Обучение', {'fields': ('student_id', 'group', 'course',
                                 'admission_year', 'education_form',
                                 'funding', 'status')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('first_name', 'last_name', 'student_id', 'group')}),
    )
    list_display = ('username', 'last_name', 'first_name', 'student_id',
                    'group', 'course', 'status')
    list_filter = ('group', 'course', 'status')
    search_fields = ('last_name', 'first_name', 'middle_name',
                     'username', 'student_id', 'group__name')
