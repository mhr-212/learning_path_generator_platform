from django.contrib import admin
from .models import LearningPath, LearningPathCourse, UserLearningProgress


@admin.register(LearningPath)
class LearningPathAdmin(admin.ModelAdmin):
    """
    Admin configuration for LearningPath model.
    """
    list_display = [
        'title', 'creator', 'difficulty_level', 'status', 
        'total_courses', 'estimated_duration_hours', 'is_public', 'created_at'
    ]
    list_filter = ['difficulty_level', 'status', 'is_public', 'created_at']
    search_fields = ['title', 'description', 'tags', 'creator__username']
    readonly_fields = ['created_at', 'updated_at', 'total_courses']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'creator')
        }),
        ('Learning Details', {
            'fields': ('difficulty_level', 'estimated_duration_hours', 'learning_objectives', 'prerequisites')
        }),
        ('Organization', {
            'fields': ('tags', 'status', 'is_public')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'total_courses'),
            'classes': ('collapse',)
        }),
    )


@admin.register(LearningPathCourse)
class LearningPathCourseAdmin(admin.ModelAdmin):
    """
    Admin configuration for LearningPathCourse model.
    """
    list_display = ['learning_path', 'course', 'order', 'is_required']
    list_filter = ['is_required', 'learning_path__difficulty_level']
    search_fields = ['learning_path__title', 'course__title']
    ordering = ['learning_path', 'order']


@admin.register(UserLearningProgress)
class UserLearningProgressAdmin(admin.ModelAdmin):
    """
    Admin configuration for UserLearningProgress model.
    """
    list_display = [
        'user', 'learning_path', 'progress',
        'current_course', 'started_at', 'is_completed'
    ]
    list_filter = ['started_at', 'completed_at']
    search_fields = ['user__username', 'learning_path__title']
    readonly_fields = ['started_at', 'is_completed', 'progress']

    fieldsets = (
        ('Progress Information', {
            'fields': ('user', 'learning_path', 'progress', 'current_course')
        }),
        ('Dates', {
            'fields': ('started_at', 'completed_at')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
    )

    def progress(self, obj):
        return f"{obj.calculate_progress()}%"
    progress.short_description = 'Progress'
