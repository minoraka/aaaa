from django.db.models import ProtectedError
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Direction, Faculty, Group
from .serializers import DirectionSerializer, FacultySerializer, GroupSerializer


class ProtectedDeleteMixin:
    """Вместо ошибки 500 возвращает 409, если у объекта есть связанные записи."""

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {'detail': 'Нельзя удалить: есть связанные объекты.'},
                status=status.HTTP_409_CONFLICT)


class FacultyViewSet(ProtectedDeleteMixin, viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    search_fields = ('name', 'short_name', 'dean')


class DirectionViewSet(ProtectedDeleteMixin, viewsets.ModelViewSet):
    queryset = Direction.objects.select_related('faculty')
    serializer_class = DirectionSerializer
    filterset_fields = ('faculty',)
    search_fields = ('code', 'name')


class GroupViewSet(ProtectedDeleteMixin, viewsets.ModelViewSet):
    queryset = Group.objects.select_related('direction__faculty')
    serializer_class = GroupSerializer
    filterset_fields = ('direction', 'is_active', 'admission_year')
    search_fields = ('name',)
