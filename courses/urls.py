from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet, CategoryViewSet, CourseReviewViewSet,
    UserCourseProgressViewSet
)

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'reviews', CourseReviewViewSet, basename='course-reviews')
router.register(r'course-progress', UserCourseProgressViewSet, basename='course-progress')

urlpatterns = [
    path('api/', include(router.urls)),
]
