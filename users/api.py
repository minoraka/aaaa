from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, viewsets

from academics.views import ProtectedDeleteMixin

from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.name', read_only=True)
    direction_name = serializers.CharField(source='group.direction.name', read_only=True)
    faculty_name = serializers.CharField(source='group.direction.faculty.name', read_only=True)

    class Meta:
        model = Student
        fields = (
            'id', 'username', 'password', 'last_name', 'first_name', 'middle_name',
            'email', 'birth_date', 'gender', 'phone', 'address', 'photo',
            'student_id', 'group', 'group_name', 'direction_name', 'faculty_name',
            'course', 'admission_year', 'education_form', 'funding', 'status',
            'created_at', 'updated_at',
        )
        read_only_fields = ('created_at', 'updated_at')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False,
                         'style': {'input_type': 'password'}},
            'group': {'required': True, 'allow_null': False},
        }

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        if self.instance is None and not attrs.get('password'):
            raise serializers.ValidationError({'password': 'Обязательное поле.'})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        student = Student(**validated_data)
        student.set_password(password)
        student.save()
        return student

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save(update_fields=['password'])
        return instance


class StudentViewSet(ProtectedDeleteMixin, viewsets.ModelViewSet):
    queryset = Student.objects.select_related('group__direction__faculty')
    serializer_class = StudentSerializer
    filterset_fields = ('group', 'group__direction', 'group__direction__faculty',
                        'course', 'status')
    search_fields = ('last_name', 'first_name', 'middle_name', 'student_id')
