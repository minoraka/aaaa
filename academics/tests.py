from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Direction, Faculty, Group

Student = get_user_model()


class ApiTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = Student.objects.create_user(
            'admin', password='admin12345', student_id='A-0')
        cls.f1 = Faculty.objects.create(name='Информационные технологии', short_name='ФИТ', dean='Иванов И.И.')
        cls.f2 = Faculty.objects.create(name='Экономика', short_name='ФЭ', dean='Петров П.П.')
        cls.d1 = Direction.objects.create(code='09.03.01', name='Информатика', faculty=cls.f1, duration_years=4)
        cls.d2 = Direction.objects.create(code='38.03.01', name='Экономика', faculty=cls.f2, duration_years=4)
        cls.g1 = Group.objects.create(name='ИС-21', direction=cls.d1, admission_year=2024)
        cls.g2 = Group.objects.create(name='ЭК-21', direction=cls.d2, admission_year=2024)

    def login(self):
        self.client.force_authenticate(self.admin)

    def student_payload(self, **extra):
        data = {
            'username': 'ivanov', 'password': 'Str0ngPass!77',
            'last_name': 'Иванов', 'first_name': 'Иван', 'student_id': '101',
            'group': self.g1.pk, 'course': 1, 'admission_year': 2024,
            'education_form': 'очная', 'funding': 'бюджет',
        }
        data.update(extra)
        return data


class PermissionsTests(ApiTestCase):
    def test_anonymous_can_read(self):
        for name in ('faculty', 'direction', 'group', 'student'):
            r = self.client.get(f'/api/{name}s/'.replace('facultys', 'faculties'))
            self.assertEqual(r.status_code, 200, name)

    def test_anonymous_cannot_write(self):
        r = self.client.post('/api/faculties/', {'name': 'X', 'short_name': 'X', 'dean': 'X'})
        self.assertIn(r.status_code, (401, 403))
        r = self.client.post('/api/students/', self.student_payload(), format='json')
        self.assertIn(r.status_code, (401, 403))

    def test_pagination(self):
        r = self.client.get('/api/faculties/')
        self.assertEqual(r.data['count'], 2)
        self.assertIn('results', r.data)


class CrudTests(ApiTestCase):
    def test_faculty_crud(self):
        self.login()
        r = self.client.post('/api/faculties/', {'name': 'Право', 'short_name': 'ФП', 'dean': 'Сидоров'})
        self.assertEqual(r.status_code, 201)
        pk = r.data['id']
        r = self.client.patch(f'/api/faculties/{pk}/', {'dean': 'Новый'})
        self.assertEqual(r.data['dean'], 'Новый')
        self.assertEqual(self.client.delete(f'/api/faculties/{pk}/').status_code, 204)

    def test_direction_has_faculty_name(self):
        self.login()
        r = self.client.post('/api/directions/', {
            'code': '01.01.01', 'name': 'Математика', 'faculty': self.f1.pk, 'duration_years': 4})
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.data['faculty_name'], self.f1.name)

    def test_group_has_names(self):
        r = self.client.get(f'/api/groups/{self.g1.pk}/')
        self.assertEqual(r.data['direction_name'], 'Информатика')
        self.assertEqual(r.data['faculty_name'], self.f1.name)

    def test_filters(self):
        r = self.client.get(f'/api/directions/?faculty={self.f1.pk}')
        self.assertEqual([d['id'] for d in r.data['results']], [self.d1.pk])
        r = self.client.get(f'/api/groups/?direction={self.d2.pk}')
        self.assertEqual([g['id'] for g in r.data['results']], [self.g2.pk])

    def test_delete_with_children_returns_409(self):
        self.login()
        self.assertEqual(self.client.delete(f'/api/faculties/{self.f1.pk}/').status_code, 409)
        self.assertEqual(self.client.delete(f'/api/directions/{self.d1.pk}/').status_code, 409)


class StudentApiTests(ApiTestCase):
    def test_create_student(self):
        self.login()
        r = self.client.post('/api/students/', self.student_payload(), format='json')
        self.assertEqual(r.status_code, 201, r.data)
        self.assertNotIn('password', r.data)
        self.assertEqual(r.data['group'], self.g1.pk)
        self.assertEqual(r.data['group_name'], 'ИС-21')
        self.assertEqual(r.data['faculty_name'], self.f1.name)
        student = Student.objects.get(username='ivanov')
        self.assertNotEqual(student.password, 'Str0ngPass!77')
        self.assertTrue(student.password.startswith(('pbkdf2_', 'argon2', 'bcrypt', 'scrypt')))
        self.assertTrue(student.check_password('Str0ngPass!77'))

    def test_student_id_unique(self):
        self.login()
        self.client.post('/api/students/', self.student_payload(), format='json')
        r = self.client.post('/api/students/', self.student_payload(username='other'), format='json')
        self.assertEqual(r.status_code, 400)
        self.assertIn('student_id', r.data)

    def test_group_and_password_required(self):
        self.login()
        p = self.student_payload()
        del p['group']
        self.assertIn('group', self.client.post('/api/students/', p, format='json').data)
        p = self.student_payload()
        del p['password']
        self.assertIn('password', self.client.post('/api/students/', p, format='json').data)

    def test_weak_password_rejected(self):
        self.login()
        r = self.client.post('/api/students/', self.student_payload(password='123'), format='json')
        self.assertEqual(r.status_code, 400)
        self.assertIn('password', r.data)

    def test_unknown_group_rejected(self):
        self.login()
        r = self.client.post('/api/students/', self.student_payload(group=9999), format='json')
        self.assertEqual(r.status_code, 400)

    def test_update_without_password_keeps_it(self):
        self.login()
        pk = self.client.post('/api/students/', self.student_payload(), format='json').data['id']
        r = self.client.patch(f'/api/students/{pk}/', {'course': 2}, format='json')
        self.assertEqual(r.status_code, 200)
        self.assertTrue(Student.objects.get(pk=pk).check_password('Str0ngPass!77'))

    def test_filter_students_by_group(self):
        self.login()
        self.client.post('/api/students/', self.student_payload(), format='json')
        self.client.post('/api/students/', self.student_payload(
            username='petrova', student_id='102', group=self.g2.pk), format='json')
        r = self.client.get(f'/api/students/?group={self.g2.pk}')
        self.assertEqual([s['username'] for s in r.data['results']], ['petrova'])

    def test_group_with_students_cannot_be_deleted(self):
        self.login()
        self.client.post('/api/students/', self.student_payload(), format='json')
        self.assertEqual(self.client.delete(f'/api/groups/{self.g1.pk}/').status_code, 409)
