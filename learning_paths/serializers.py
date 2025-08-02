from rest_framework import serializers
from django.contrib.auth.models import User
from .models import LearningPath, LearningPathCourse, UserLearningProgress
from courses.models import Course
from courses.serializers import CourseSerializer


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model (basic info).
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id']


class LearningPathCourseSerializer(serializers.ModelSerializer):
    """
    Serializer for LearningPathCourse through model.
    """
    course = CourseSerializer(read_only=True)
    course_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = LearningPathCourse
        fields = ['id', 'course', 'course_id', 'order', 'is_required', 'notes']
        read_only_fields = ['id']


class LearningPathSerializer(serializers.ModelSerializer):
    """
    Serializer for LearningPath model.
    """
    creator = UserSerializer(read_only=True)
    path_courses = LearningPathCourseSerializer(many=True, read_only=True)
    total_courses = serializers.ReadOnlyField()
    tag_list = serializers.ReadOnlyField()
    
    class Meta:
        model = LearningPath
        fields = [
            'id', 'title', 'description', 'creator', 'difficulty_level',
            'estimated_duration_hours', 'status', 'tags', 'prerequisites',
            'learning_objectives', 'is_public', 'created_at', 'updated_at',
            'path_courses', 'total_courses', 'tag_list'
        ]
        read_only_fields = ['id', 'creator', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """
        Create a new learning path and assign the current user as creator.
        """
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)


class LearningPathCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating learning paths with course assignments.
    """
    course_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        help_text="List of course IDs to add to this learning path"
    )
    
    class Meta:
        model = LearningPath
        fields = [
            'id', 'title', 'description', 'difficulty_level',
            'estimated_duration_hours', 'status', 'tags', 'prerequisites',
            'learning_objectives', 'is_public', 'course_ids'
        ]
        read_only_fields = ['id']
    
    def create(self, validated_data):
        """
        Create learning path and associate courses.
        """
        course_ids = validated_data.pop('course_ids', [])
        validated_data['creator'] = self.context['request'].user
        learning_path = super().create(validated_data)
        
        # Add courses to the learning path
        for i, course_id in enumerate(course_ids, 1):
            try:
                course = Course.objects.get(id=course_id)
                LearningPathCourse.objects.create(
                    learning_path=learning_path,
                    course=course,
                    order=i
                )
            except Course.DoesNotExist:
                continue
        
        return learning_path
    
    def update(self, instance, validated_data):
        """
        Update learning path and optionally update course associations.
        """
        course_ids = validated_data.pop('course_ids', None)
        learning_path = super().update(instance, validated_data)
        
        if course_ids is not None:
            # Remove existing course associations
            LearningPathCourse.objects.filter(learning_path=learning_path).delete()
            
            # Add new course associations
            for i, course_id in enumerate(course_ids, 1):
                try:
                    course = Course.objects.get(id=course_id)
                    LearningPathCourse.objects.create(
                        learning_path=learning_path,
                        course=course,
                        order=i
                    )
                except Course.DoesNotExist:
                    continue
        
        return learning_path


class UserLearningProgressSerializer(serializers.ModelSerializer):
    """
    Serializer for UserLearningProgress model.
    """
    user = UserSerializer(read_only=True)
    learning_path = LearningPathSerializer(read_only=True)
    current_course = CourseSerializer(read_only=True)
    is_completed = serializers.ReadOnlyField()
    progress = serializers.SerializerMethodField()

    class Meta:
        model = UserLearningProgress
        fields = [
            'id', 'user', 'learning_path', 'started_at', 'completed_at',
            'progress', 'current_course', 'notes', 'is_completed'
        ]
        read_only_fields = ['id', 'user', 'started_at']

    def get_progress(self, obj):
        return obj.calculate_progress()


class LearningPathDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for learning path with all related information.
    """
    creator = UserSerializer(read_only=True)
    path_courses = LearningPathCourseSerializer(many=True, read_only=True)
    total_courses = serializers.ReadOnlyField()
    tag_list = serializers.ReadOnlyField()
    user_progress = serializers.SerializerMethodField()
    
    class Meta:
        model = LearningPath
        fields = [
            'id', 'title', 'description', 'creator', 'difficulty_level',
            'estimated_duration_hours', 'status', 'tags', 'prerequisites',
            'learning_objectives', 'is_public', 'created_at', 'updated_at',
            'path_courses', 'total_courses', 'tag_list', 'user_progress'
        ]
        read_only_fields = ['id', 'creator', 'created_at', 'updated_at']
    
    def get_user_progress(self, obj):
        """
        Get user's progress for this learning path if authenticated.
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                progress = UserLearningProgress.objects.get(
                    user=request.user,
                    learning_path=obj
                )
                return UserLearningProgressSerializer(progress).data
            except UserLearningProgress.DoesNotExist:
                return None
        return None
