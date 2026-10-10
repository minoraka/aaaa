from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Student

PROFILE_FIELDS = (
    'last_name', 'first_name', 'middle_name', 'email', 'birth_date', 'gender',
    'phone', 'address', 'photo', 'student_id', 'group', 'course',
    'admission_year', 'education_form', 'funding', 'status',
)

DATE_WIDGET = forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')


class GroupRequiredMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].required = True


class StudentCreateForm(GroupRequiredMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Student
        fields = ('username',) + PROFILE_FIELDS
        widgets = {'birth_date': DATE_WIDGET}


class StudentUpdateForm(GroupRequiredMixin, forms.ModelForm):
    class Meta:
        model = Student
        fields = PROFILE_FIELDS
        widgets = {'birth_date': DATE_WIDGET}
