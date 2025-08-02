"""
URL configuration for learning_platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import (
    HomeView, LoginView, RegisterView, DashboardView, ProfileView,
    LearningPathsView, LearningPathDetailView, CoursesView, CourseDetailView,
    CategoriesView, MyLearningPathsView, MyCoursesView
)


# API Documentation Schema
schema_view = get_schema_view(
    openapi.Info(
        title="Learning Path Generator API",
        default_version='v1',
        description="A comprehensive API for managing learning paths, courses, and user progress",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@learningpathgenerator.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[AllowAny],
)


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """
    API root endpoint with available endpoints.
    """
    return Response({
        'message': 'Welcome to Learning Path Generator API',
        'version': '1.0.0',
        'endpoints': {
            'authentication': {
                'register': '/api/auth/register/',
                'login': '/api/auth/login/',
                'refresh': '/api/auth/refresh/',
                'dashboard': '/api/auth/dashboard/',
                'profiles': '/api/profiles/',
                'skills': '/api/skills/',
            },
            'learning_paths': {
                'learning_paths': '/api/learning-paths/',
                'my_paths': '/api/learning-paths/my_paths/',
                'learning_progress': '/api/learning-progress/',
            },
            'courses': {
                'courses': '/api/courses/',
                'my_courses': '/api/courses/my_courses/',
                'featured': '/api/courses/featured/',
                'free_courses': '/api/courses/free_courses/',
                'categories': '/api/categories/',
                'reviews': '/api/reviews/',
                'course_progress': '/api/course-progress/',
            },
            'stats': '/api/stats/',
            'admin': '/admin/',
            'api_docs': '/api/docs/',
        }
    })


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/schema/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    
    # API endpoints
    path('api/', api_root, name='api-root'),
    path('', include('authentication.urls')),
    path('', include('learning_paths.urls')),
    path('', include('courses.urls')),
    
    # Template views
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('accounts/login/', LoginView.as_view(), name='accounts-login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('learning-paths/', LearningPathsView.as_view(), name='learning-paths'),
    path('learning-paths/<int:pk>/', LearningPathDetailView.as_view(), name='learning-path-detail'),
    path('my-learning-paths/', MyLearningPathsView.as_view(), name='my-learning-paths'),
    path('courses/', CoursesView.as_view(), name='courses'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('my-courses/', MyCoursesView.as_view(), name='my-courses'),
    path('categories/', CategoriesView.as_view(), name='categories'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
