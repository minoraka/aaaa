from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView,
                                  ListView, UpdateView)

from .forms import StudentCreateForm, StudentUpdateForm
from academics.models import Group

from .models import Student


class StudentListView(ListView):
    model = Student
    queryset = Student.objects.select_related('group')
    template_name = 'users/student_list.html'
    context_object_name = 'students'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '').strip()
        group = self.request.GET.get('group', '').strip()
        for word in q.split():
            qs = qs.filter(
                Q(last_name__icontains=word) |
                Q(first_name__icontains=word) |
                Q(middle_name__icontains=word)
            )
        if group.isdigit():
            qs = qs.filter(group_id=group)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['groups'] = Group.objects.all()
        ctx['q'] = self.request.GET.get('q', '')
        ctx['current_group'] = self.request.GET.get('group', '')
        return ctx


class StudentDetailView(DetailView):
    queryset = Student.objects.select_related('group__direction__faculty')
    template_name = 'users/student_detail.html'
    context_object_name = 'student'


class StudentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Student
    form_class = StudentCreateForm
    template_name = 'users/student_form.html'
    success_message = 'Студент создан'


class StudentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Student
    form_class = StudentUpdateForm
    template_name = 'users/student_form.html'
    success_message = 'Данные студента обновлены'


class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'users/student_confirm_delete.html'
    success_url = reverse_lazy('students:list')
