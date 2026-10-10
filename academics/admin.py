from django.contrib import admin

from .models import Direction, Faculty, Group


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'dean')
    search_fields = ('name', 'short_name', 'dean')


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'faculty', 'duration_years')
    list_filter = ('faculty',)
    search_fields = ('code', 'name')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'direction', 'admission_year', 'is_active')
    list_filter = ('direction__faculty', 'direction', 'admission_year', 'is_active')
    search_fields = ('name',)
