from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LearningPathViewSet, UserLearningProgressViewSet

router = DefaultRouter()
router.register(r'learning-paths', LearningPathViewSet)
router.register(r'learning-progress', UserLearningProgressViewSet, basename='learning-progress')

urlpatterns = [
    path('api/', include(router.urls)),
]
