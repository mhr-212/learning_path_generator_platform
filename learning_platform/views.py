from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class HomeView(TemplateView):
    """
    Home page view.
    """
    template_name = 'base/home.html'


class LoginView(TemplateView):
    """
    Login page view.
    """
    template_name = 'auth/login.html'


class RegisterView(TemplateView):
    """
    Registration page view.
    """
    template_name = 'auth/register.html'


class LearningPathsView(TemplateView):
    """
    Learning paths listing page view.
    """
    template_name = 'learning_paths/list.html'


class LearningPathDetailView(TemplateView):
    """
    Learning path detail page view.
    """
    template_name = 'learning_paths/detail.html'


class CoursesView(TemplateView):
    """
    Courses listing page view.
    """
    template_name = 'courses/list.html'


class CourseDetailView(TemplateView):
    """
    Course detail page view.
    """
    template_name = 'courses/detail.html'


class CategoriesView(TemplateView):
    """
    Categories listing page view.
    """
    template_name = 'categories/list.html'


class DashboardView(TemplateView):
    """
    User dashboard view (requires authentication).
    """
    template_name = 'dashboard.html'


class ProfileView(TemplateView):
    """
    User profile view (requires authentication).
    """
    template_name = 'profile.html'


class MyLearningPathsView(TemplateView):
    """
    User's learning paths view (requires authentication).
    """
    template_name = 'learning_paths/my_paths.html'


class MyCoursesView(TemplateView):
    """
    User's courses view (requires authentication).
    """
    template_name = 'courses/my_courses.html'
