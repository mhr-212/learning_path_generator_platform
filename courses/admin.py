from django.contrib import admin
from .models import Course, Category, CourseReview, UserCourseProgress


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for Category model.
    """
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Admin configuration for Course model.
    """
    list_display = [
        'title', 'creator', 'category', 'difficulty_level', 
        'course_type', 'price', 'rating', 'status', 'is_public', 'created_at'
    ]
    list_filter = [
        'difficulty_level', 'course_type', 'status', 'is_public', 
        'certificate_available', 'category', 'created_at'
    ]
    search_fields = ['title', 'description', 'instructor', 'platform', 'tags', 'creator__username']
    readonly_fields = ['created_at', 'updated_at', 'rating', 'total_ratings', 'is_free']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'short_description', 'description', 'creator', 'category')
        }),
        ('Course Details', {
            'fields': ('difficulty_level', 'course_type', 'duration_hours', 'url', 'instructor', 'platform')
        }),
        ('Pricing & Ratings', {
            'fields': ('price', 'rating', 'total_ratings', 'is_free'),
            'classes': ('collapse',)
        }),
        ('Content', {
            'fields': ('prerequisites', 'learning_outcomes', 'language', 'certificate_available')
        }),
        ('Organization', {
            'fields': ('tags', 'status', 'is_public')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CourseReview)
class CourseReviewAdmin(admin.ModelAdmin):
    """
    Admin configuration for CourseReview model.
    """
    list_display = ['course', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['course__title', 'user__username', 'review_text']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(UserCourseProgress)
class UserCourseProgressAdmin(admin.ModelAdmin):
    """
    Admin configuration for UserCourseProgress model.
    """
    list_display = [
        'user', 'course', 'progress_percentage', 
        'time_spent_hours', 'started_at', 'is_completed'
    ]
    list_filter = ['progress_percentage', 'started_at', 'completed_at']
    search_fields = ['user__username', 'course__title']
    readonly_fields = ['started_at', 'is_completed']
    
    fieldsets = (
        ('Progress Information', {
            'fields': ('user', 'course', 'progress_percentage', 'time_spent_hours')
        }),
        ('Dates', {
            'fields': ('started_at', 'completed_at')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
    )