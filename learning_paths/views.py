from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from .models import LearningPath, LearningPathCourse, UserLearningProgress
from .serializers import (
    LearningPathSerializer, LearningPathCreateUpdateSerializer,
    LearningPathDetailSerializer, UserLearningProgressSerializer,
    LearningPathCourseSerializer
)
from .permissions import IsOwnerOrReadOnly


class LearningPathViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing learning paths.
    Provides CRUD operations with proper permissions and filtering.
    """
    queryset = LearningPath.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['difficulty_level', 'status', 'creator', 'is_public']
    search_fields = ['title', 'description', 'tags', 'learning_objectives']
    ordering_fields = ['created_at', 'updated_at', 'title', 'estimated_duration_hours']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """
        Return appropriate serializer based on action.
        """
        if self.action == 'retrieve':
            return LearningPathDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return LearningPathCreateUpdateSerializer
        return LearningPathSerializer
    
    def get_queryset(self):
        """
        Filter queryset based on user permissions.
        """
        queryset = LearningPath.objects.all()
        
        # If user is not authenticated, only show public learning paths
        if not self.request.user.is_authenticated:
            return queryset.filter(is_public=True, status='published')
        
        # For authenticated users, show public paths and their own paths
        return queryset.filter(
            Q(is_public=True, status='published') |
            Q(creator=self.request.user)
        ).distinct()
    
    @action(detail=False, methods=['get'])
    def my_paths(self, request):
        """
        Get learning paths created by the current user.
        """
        queryset = LearningPath.objects.filter(creator=request.user)
        queryset = self.filter_queryset(queryset)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def start_learning(self, request, pk=None):
        """
        Start learning a specific learning path.
        """
        learning_path = self.get_object()
        
        # Check if user already started this path
        progress, created = UserLearningProgress.objects.get_or_create(
            user=request.user,
            learning_path=learning_path,
            defaults={'progress_percentage': 0}
        )
        
        if not created:
            return Response(
                {'detail': 'You have already started this learning path.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = UserLearningProgressSerializer(progress)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def progress(self, request, pk=None):
        """
        Get user's progress for a specific learning path.
        """
        learning_path = self.get_object()
        
        try:
            progress = UserLearningProgress.objects.get(
                user=request.user,
                learning_path=learning_path
            )
            serializer = UserLearningProgressSerializer(progress)
            return Response(serializer.data)
        except UserLearningProgress.DoesNotExist:
            return Response(
                {'detail': 'You have not started this learning path yet.'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def add_course(self, request, pk=None):
        """
        Add a course to the learning path.
        """
        learning_path = self.get_object()
        
        # Check if user is the owner
        if learning_path.creator != request.user:
            return Response(
                {'detail': 'You can only modify your own learning paths.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        course_id = request.data.get('course_id')
        order = request.data.get('order', learning_path.total_courses + 1)
        is_required = request.data.get('is_required', True)
        notes = request.data.get('notes', '')
        
        if not course_id:
            return Response(
                {'detail': 'course_id is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from courses.models import Course
            course = Course.objects.get(id=course_id)
            
            # Check if course is already in the path
            if LearningPathCourse.objects.filter(
                learning_path=learning_path,
                course=course
            ).exists():
                return Response(
                    {'detail': 'Course is already in this learning path.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            path_course = LearningPathCourse.objects.create(
                learning_path=learning_path,
                course=course,
                order=order,
                is_required=is_required,
                notes=notes
            )
            
            serializer = LearningPathCourseSerializer(path_course)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Course.DoesNotExist:
            return Response(
                {'detail': 'Course not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['delete'])
    def remove_course(self, request, pk=None):
        """
        Remove a course from the learning path.
        """
        learning_path = self.get_object()
        
        # Check if user is the owner
        if learning_path.creator != request.user:
            return Response(
                {'detail': 'You can only modify your own learning paths.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        course_id = request.data.get('course_id')
        
        if not course_id:
            return Response(
                {'detail': 'course_id is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            path_course = LearningPathCourse.objects.get(
                learning_path=learning_path,
                course_id=course_id
            )
            path_course.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        except LearningPathCourse.DoesNotExist:
            return Response(
                {'detail': 'Course not found in this learning path.'},
                status=status.HTTP_404_NOT_FOUND
            )


class UserLearningProgressViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user learning progress.
    """
    serializer_class = UserLearningProgressSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['learning_path', 'progress_percentage']
    ordering_fields = ['started_at', 'progress_percentage']
    ordering = ['-started_at']
    
    def get_queryset(self):
        """
        Return progress records for the current user only.
        """
        return UserLearningProgress.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """
        Set the user to the current user when creating progress.
        """
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        """
        Mark a learning path as completed.
        """
        progress = self.get_object()
        
        if progress.completed_at:
            return Response(
                {'detail': 'Learning path is already completed.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from django.utils import timezone
        progress.completed_at = timezone.now()
        progress.progress_percentage = 100
        progress.save()
        
        serializer = self.get_serializer(progress)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def update_progress(self, request, pk=None):
        """
        Update progress percentage and current course.
        """
        progress = self.get_object()
        
        progress_percentage = request.data.get('progress_percentage')
        current_course_id = request.data.get('current_course_id')
        notes = request.data.get('notes')
        
        if progress_percentage is not None:
            if 0 <= progress_percentage <= 100:
                progress.progress_percentage = progress_percentage
                
                # If 100%, mark as completed
                if progress_percentage == 100:
                    from django.utils import timezone
                    progress.completed_at = timezone.now()
            else:
                return Response(
                    {'detail': 'Progress percentage must be between 0 and 100.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        if current_course_id is not None:
            try:
                from courses.models import Course
                course = Course.objects.get(id=current_course_id)
                progress.current_course = course
            except Course.DoesNotExist:
                return Response(
                    {'detail': 'Course not found.'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        if notes is not None:
            progress.notes = notes
        
        progress.save()
        serializer = self.get_serializer(progress)
        return Response(serializer.data)
