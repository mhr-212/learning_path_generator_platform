from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Course, Category, CourseReview, UserCourseProgress


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model (basic info).
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id']


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'slug', 'created_at']
        read_only_fields = ['id', 'created_at']


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for Course model.
    """
    creator = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    is_free = serializers.ReadOnlyField()
    tag_list = serializers.ReadOnlyField()
    average_rating_display = serializers.ReadOnlyField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'short_description', 'creator',
            'category', 'category_id', 'difficulty_level', 'course_type',
            'duration_hours', 'url', 'instructor', 'platform', 'price',
            'rating', 'total_ratings', 'status', 'tags', 'prerequisites',
            'learning_outcomes', 'language', 'certificate_available',
            'is_public', 'created_at', 'updated_at', 'is_free', 'tag_list',
            'average_rating_display'
        ]
        read_only_fields = ['id', 'creator', 'created_at', 'updated_at', 'rating', 'total_ratings']
    
    def create(self, validated_data):
        """
        Create a new course and assign the current user as creator.
        """
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)


class CourseCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating courses.
    """
    category_id = serializers.IntegerField(required=False, allow_null=True)
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'short_description', 'category_id',
            'difficulty_level', 'course_type', 'duration_hours', 'url',
            'instructor', 'platform', 'price', 'status', 'tags',
            'prerequisites', 'learning_outcomes', 'language',
            'certificate_available', 'is_public'
        ]
        read_only_fields = ['id']
    
    def create(self, validated_data):
        """
        Create course with proper category assignment.
        """
        category_id = validated_data.pop('category_id', None)
        validated_data['creator'] = self.context['request'].user
        
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
                validated_data['category'] = category
            except Category.DoesNotExist:
                pass
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """
        Update course with proper category assignment.
        """
        category_id = validated_data.pop('category_id', None)
        
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
                validated_data['category'] = category
            except Category.DoesNotExist:
                pass
        elif category_id is None:
            validated_data['category'] = None
        
        return super().update(instance, validated_data)


class CourseReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for CourseReview model.
    """
    user = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    
    class Meta:
        model = CourseReview
        fields = [
            'id', 'course', 'user', 'rating', 'review_text',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class CourseReviewCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating course reviews.
    """
    course_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = CourseReview
        fields = ['id', 'course_id', 'rating', 'review_text']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        """
        Create review with proper course and user assignment.
        """
        course_id = validated_data.pop('course_id')
        validated_data['user'] = self.context['request'].user
        
        try:
            course = Course.objects.get(id=course_id)
            validated_data['course'] = course
        except Course.DoesNotExist:
            raise serializers.ValidationError("Course not found.")
        
        return super().create(validated_data)


class UserCourseProgressSerializer(serializers.ModelSerializer):
    """
    Serializer for UserCourseProgress model.
    """
    user = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    is_completed = serializers.ReadOnlyField()
    
    class Meta:
        model = UserCourseProgress
        fields = [
            'id', 'user', 'course', 'started_at', 'completed_at',
            'progress_percentage', 'time_spent_hours', 'notes', 'is_completed'
        ]
        read_only_fields = ['id', 'user', 'started_at']


class CourseDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for course with all related information.
    """
    creator = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    is_free = serializers.ReadOnlyField()
    tag_list = serializers.ReadOnlyField()
    average_rating_display = serializers.ReadOnlyField()
    reviews = CourseReviewSerializer(many=True, read_only=True)
    user_progress = serializers.SerializerMethodField()
    user_review = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'short_description', 'creator',
            'category', 'difficulty_level', 'course_type', 'duration_hours',
            'url', 'instructor', 'platform', 'price', 'rating', 'total_ratings',
            'status', 'tags', 'prerequisites', 'learning_outcomes', 'language',
            'certificate_available', 'is_public', 'created_at', 'updated_at',
            'is_free', 'tag_list', 'average_rating_display', 'reviews',
            'user_progress', 'user_review'
        ]
        read_only_fields = ['id', 'creator', 'created_at', 'updated_at', 'rating', 'total_ratings']
    
    def get_user_progress(self, obj):
        """
        Get user's progress for this course if authenticated.
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                progress = UserCourseProgress.objects.get(
                    user=request.user,
                    course=obj
                )
                return UserCourseProgressSerializer(progress).data
            except UserCourseProgress.DoesNotExist:
                return None
        return None
    
    def get_user_review(self, obj):
        """
        Get user's review for this course if authenticated and exists.
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                review = CourseReview.objects.get(
                    user=request.user,
                    course=obj
                )
                return CourseReviewSerializer(review).data
            except CourseReview.DoesNotExist:
                return None
        return None