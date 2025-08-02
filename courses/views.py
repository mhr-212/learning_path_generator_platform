from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q, Avg
from .models import Course, Category, CourseReview, UserCourseProgress
from .serializers import (
    CourseSerializer, CourseCreateUpdateSerializer, CourseDetailSerializer,
    CategorySerializer, CourseReviewSerializer, CourseReviewCreateUpdateSerializer,
    UserCourseProgressSerializer
)
from learning_paths.permissions import IsOwnerOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing course categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing courses.
    Provides CRUD operations with proper permissions and filtering.
    """
    queryset = Course.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        'difficulty_level', 'course_type', 'status', 'creator', 'category',
        'platform', 'certificate_available', 'is_public', 'price'
    ]
    search_fields = ['title', 'description', 'short_description', 'tags', 'instructor']
    ordering_fields = [
        'created_at', 'updated_at', 'title', 'duration_hours', 'price', 'rating'
    ]
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """
        Return appropriate serializer based on action.
        """
        if self.action == 'retrieve':
            return CourseDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return CourseCreateUpdateSerializer
        return CourseSerializer
    
    def get_queryset(self):
        """
        Filter queryset based on user permissions.
        """
        queryset = Course.objects.all()
        
        # If user is not authenticated, only show public courses
        if not self.request.user.is_authenticated:
            return queryset.filter(is_public=True, status='published')
        
        # For authenticated users, show public courses and their own courses
        return queryset.filter(
            Q(is_public=True, status='published') |
            Q(creator=self.request.user)
        ).distinct()
    
    @action(detail=False, methods=['get'])
    def my_courses(self, request):
        """
        Get courses created by the current user.
        """
        queryset = Course.objects.filter(creator=request.user)
        queryset = self.filter_queryset(queryset)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """
        Get featured courses (high-rated, popular courses).
        """
        queryset = self.get_queryset().filter(
            rating__gte=4.0,
            total_ratings__gte=10
        ).order_by('-rating', '-total_ratings')[:20]
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def free_courses(self, request):
        """
        Get all free courses.
        """
        queryset = self.get_queryset().filter(price=0.00)
        queryset = self.filter_queryset(queryset)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def start_course(self, request, pk=None):
        """
        Start taking a specific course.
        """
        course = self.get_object()
        
        # Check if user already started this course
        progress, created = UserCourseProgress.objects.get_or_create(
            user=request.user,
            course=course,
            defaults={'progress_percentage': 0}
        )
        
        if not created:
            return Response(
                {'detail': 'You have already started this course.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = UserCourseProgressSerializer(progress)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def progress(self, request, pk=None):
        """
        Get user's progress for a specific course.
        """
        course = self.get_object()
        
        try:
            progress = UserCourseProgress.objects.get(
                user=request.user,
                course=course
            )
            serializer = UserCourseProgressSerializer(progress)
            return Response(serializer.data)
        except UserCourseProgress.DoesNotExist:
            return Response(
                {'detail': 'You have not started this course yet.'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """
        Get all reviews for a specific course.
        """
        course = self.get_object()
        reviews = CourseReview.objects.filter(course=course).order_by('-created_at')
        
        page = self.paginate_queryset(reviews)
        if page is not None:
            serializer = CourseReviewSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = CourseReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class CourseReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing course reviews.
    """
    serializer_class = CourseReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'rating']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Return reviews that the user can access.
        """
        if self.request.user.is_staff:
            return CourseReview.objects.all()
        return CourseReview.objects.filter(
            Q(user=self.request.user) |
            Q(course__is_public=True, course__status='published')
        )
    
    def get_serializer_class(self):
        """
        Return appropriate serializer based on action.
        """
        if self.action in ['create', 'update', 'partial_update']:
            return CourseReviewCreateUpdateSerializer
        return CourseReviewSerializer
    
    def perform_create(self, serializer):
        """
        Set the user to the current user when creating a review.
        """
        review = serializer.save(user=self.request.user)
        
        # Update course rating
        course = review.course
        avg_rating = CourseReview.objects.filter(course=course).aggregate(
            avg_rating=Avg('rating')
        )['avg_rating']
        
        course.rating = round(avg_rating, 2) if avg_rating else None
        course.total_ratings = CourseReview.objects.filter(course=course).count()
        course.save()
    
    def perform_update(self, serializer):
        """
        Update course rating when a review is updated.
        """
        review = serializer.save()
        
        # Update course rating
        course = review.course
        avg_rating = CourseReview.objects.filter(course=course).aggregate(
            avg_rating=Avg('rating')
        )['avg_rating']
        
        course.rating = round(avg_rating, 2) if avg_rating else None
        course.total_ratings = CourseReview.objects.filter(course=course).count()
        course.save()
    
    def perform_destroy(self, instance):
        """
        Update course rating when a review is deleted.
        """
        course = instance.course
        instance.delete()
        
        # Update course rating
        avg_rating = CourseReview.objects.filter(course=course).aggregate(
            avg_rating=Avg('rating')
        )['avg_rating']
        
        course.rating = round(avg_rating, 2) if avg_rating else None
        course.total_ratings = CourseReview.objects.filter(course=course).count()
        course.save()


class UserCourseProgressViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user course progress.
    """
    serializer_class = UserCourseProgressSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'progress_percentage']
    ordering_fields = ['started_at', 'progress_percentage', 'time_spent_hours']
    ordering = ['-started_at']
    
    def get_queryset(self):
        """
        Return progress records for the current user only.
        """
        return UserCourseProgress.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """
        Set the user to the current user when creating progress.
        """
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        """
        Mark a course as completed.
        """
        progress = self.get_object()
        
        if progress.completed_at:
            return Response(
                {'detail': 'Course is already completed.'},
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
        Update progress percentage and time spent.
        """
        progress = self.get_object()
        
        progress_percentage = request.data.get('progress_percentage')
        time_spent_hours = request.data.get('time_spent_hours')
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
        
        if time_spent_hours is not None:
            if time_spent_hours >= 0:
                progress.time_spent_hours = time_spent_hours
            else:
                return Response(
                    {'detail': 'Time spent must be non-negative.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        if notes is not None:
            progress.notes = notes
        
        progress.save()
        serializer = self.get_serializer(progress)
        return Response(serializer.data)