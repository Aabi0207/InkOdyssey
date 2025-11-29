from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HabitViewSet, HabitLogViewSet, DailyReflectionViewSet

router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habit')
router.register(r'logs', HabitLogViewSet, basename='habitlog')
router.register(r'reflections', DailyReflectionViewSet, basename='dailyreflection')

urlpatterns = [
    path('', include(router.urls)),
]
