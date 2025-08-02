from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from django.db import models
from .models import UserProfile, UserSkill
from .serializers import (
    UserRegistrationSerializer, UserSerializer, UserProfileSerializer,
    UserProfileUpdateSerializer, UserSkillSerializer,
    CustomTokenObtainPairSerializer, PasswordChangeSerializer
)


class UserRegistrationView(APIView):
    """
    View for user registration.
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    'message': 'User created successfully.',
                    'user': UserSerializer(user).data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT token view that includes user profile information.
    """
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = User.objects.get(username=request.data['username'])
            profile = user.profile
            first_login = profile.first_login
            if first_login:
                profile.first_login = False
                profile.save()
            response.data['first_login'] = first_login
        return response


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user profiles.
    """
    queryset = UserProfile.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """
        Return appropriate serializer based on action.
        """
        if self.action in ['update', 'partial_update']:
            return UserProfileUpdateSerializer
        return UserProfileSerializer
    
    def get_queryset(self):
        """
        Filter queryset based on user permissions.
        """
        if self.request.user.is_staff:
            return UserProfile.objects.all()
        
        # Regular users can only see public profiles and their own
        return UserProfile.objects.filter(
            models.Q(public_profile=True) |
            models.Q(user=self.request.user)
        )
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Get current user's profile.
        """
        profile = UserProfile.objects.get(user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'])
    def update_me(self, request):
        """
        Update current user's profile.
        """
        profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileUpdateSerializer(
            profile,
            data=request.data,
            partial=request.method == 'PATCH'
        )
        if serializer.is_valid():
            serializer.save()
            return Response(UserProfileSerializer(profile).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """
        Change user password.
        """
        serializer = PasswordChangeSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Password changed successfully.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSkillViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user skills.
    """
    serializer_class = UserSkillSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Return skills for the current user only.
        """
        return UserSkill.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """
        Set the user to the current user when creating a skill.
        """
        serializer.save(user=self.request.user)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_dashboard(request):
    """
    Get dashboard data for the current user.
    """
    user = request.user
    profile = UserProfile.objects.get(user=user)
    
    # Get user's learning paths and courses
    from learning_paths.models import LearningPath, UserLearningProgress
    from courses.models import Course, UserCourseProgress
    
    learning_paths_created = LearningPath.objects.filter(creator=user).count()
    courses_added = Course.objects.filter(creator=user).count()
    
    learning_progress = UserLearningProgress.objects.filter(user=user)
    course_progress = UserCourseProgress.objects.filter(user=user)
    
    # Calculate statistics
    total_learning_paths_started = learning_progress.count()
    completed_learning_paths = learning_progress.filter(completed_at__isnull=False).count()
    
    total_courses_started = course_progress.count()
    completed_courses = course_progress.filter(completed_at__isnull=False).count()
    
    # Calculate average progress
    avg_learning_path_progress = 0
    if total_learning_paths_started > 0:
        total_progress = sum([p.calculate_progress() for p in learning_progress])
        avg_learning_path_progress = total_progress / total_learning_paths_started
    
    avg_course_progress = 0
    if total_courses_started > 0:
        total_progress = sum([p.progress_percentage for p in course_progress])
        avg_course_progress = total_progress / total_courses_started
    
    # Get recent activity
    recent_learning_paths = learning_progress.order_by('-started_at')[:5]
    recent_courses = course_progress.order_by('-started_at')[:5]
    
    dashboard_data = {
        'user': UserSerializer(user).data,
        'profile': UserProfileSerializer(profile).data,
        'statistics': {
            'learning_paths_created': learning_paths_created,
            'courses_added': courses_added,
            'learning_paths_started': total_learning_paths_started,
            'learning_paths_completed': completed_learning_paths,
            'courses_started': total_courses_started,
            'courses_completed': completed_courses,
            'avg_learning_path_progress': round(avg_learning_path_progress, 1),
            'avg_course_progress': round(avg_course_progress, 1),
        },
        'recent_activity': {
            'learning_paths': [
                {
                    'id': p.learning_path.id,
                    'title': p.learning_path.title,
                    'progress': p.calculate_progress(),
                    'started_at': p.started_at
                }
                for p in recent_learning_paths
            ],
            'courses': [
                {
                    'id': p.course.id,
                    'title': p.course.title,
                    'progress': p.progress_percentage,
                    'started_at': p.started_at
                }
                for p in recent_courses
            ]
        }
    }
    
    return Response(dashboard_data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def public_stats(request):
    """
    Get public statistics about the platform.
    """
    from learning_paths.models import LearningPath
    from courses.models import Course
    
    total_users = User.objects.count()
    total_learning_paths = LearningPath.objects.filter(is_public=True, status='published').count()
    total_courses = Course.objects.filter(is_public=True, status='published').count()
    total_free_courses = Course.objects.filter(
        is_public=True,
        status='published',
        price=0.00
    ).count()
    
    stats = {
        'total_users': total_users,
        'total_learning_paths': total_learning_paths,
        'total_courses': total_courses,
        'total_free_courses': total_free_courses,
    }
    
    return Response(stats)
