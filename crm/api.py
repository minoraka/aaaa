from rest_framework.routers import DefaultRouter

from academics.views import DirectionViewSet, FacultyViewSet, GroupViewSet
from users.api import StudentViewSet

router = DefaultRouter()
router.register('faculties', FacultyViewSet)
router.register('directions', DirectionViewSet)
router.register('groups', GroupViewSet)
router.register('students', StudentViewSet)
