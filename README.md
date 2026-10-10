# CRM: студенты, факультеты, направления, группы + REST API

Приложения: `users` (модель `Student` на основе `AbstractUser`, веб-CRUD) и `academics`
(`Faculty`, `Direction`, `Group`). REST API на Django REST Framework, документация drf-spectacular.

## Запуск
```bash
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Адреса
| Что | URL |
|---|---|
| Swagger UI | http://127.0.0.1:8000/api/docs/ |
| ReDoc | http://127.0.0.1:8000/api/redoc/ |
| OpenAPI-схема | http://127.0.0.1:8000/api/schema/ |
| Корень API | http://127.0.0.1:8000/api/ |
| Админка | http://127.0.0.1:8000/admin/ |
| Веб-список студентов | http://127.0.0.1:8000/students/ |

## Эндпоинты API (префикс `/api/`)
`faculties/`, `directions/` (фильтр `?faculty=<id>`), `groups/` (фильтр `?direction=<id>`),
`students/` (фильтры `group`, `course`, `status`, поиск `?search=`). Для каждого: list, create, retrieve, update, partial_update, delete.

Права: читать могут все, изменять только авторизованные. Пагинация: 10 записей на страницу (`?page=2`).

## Как тестировать в Swagger
1. Откройте `/api/docs/`, нажмите **Authorize**, в блоке `basicAuth` введите логин и пароль суперпользователя.
2. Создайте по порядку: факультет → направление (`faculty` = id) → группа (`direction` = id) → студент (`group` = id, `password`).
3. Пароль в ответе не возвращается, в базе хранится хеш.

## Тесты
```bash
python manage.py test
```
