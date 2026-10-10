from rest_framework import serializers

from .models import Direction, Faculty, Group


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ('id', 'name', 'short_name', 'dean')


class DirectionSerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source='faculty.name', read_only=True)

    class Meta:
        model = Direction
        fields = ('id', 'code', 'name', 'faculty', 'faculty_name', 'duration_years')


class GroupSerializer(serializers.ModelSerializer):
    direction_name = serializers.CharField(source='direction.name', read_only=True)
    faculty = serializers.IntegerField(source='direction.faculty_id', read_only=True)
    faculty_name = serializers.CharField(source='direction.faculty.name', read_only=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'direction', 'direction_name', 'faculty',
                  'faculty_name', 'admission_year', 'is_active')
