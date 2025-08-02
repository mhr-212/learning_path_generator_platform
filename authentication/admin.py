from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, UserSkill


class UserProfileInline(admin.StackedInline):
    """
    Inline admin for UserProfile.
    """
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = [
        'bio', 'avatar', 'birth_date', 'location', 'website',
        'github_username', 'linkedin_profile', 'twitter_handle',
        'experience_level', 'learning_style', 'interests', 'goals',
        'time_zone', 'weekly_learning_hours', 'email_notifications', 'public_profile'
    ]


class UserSkillInline(admin.TabularInline):
    """
    Inline admin for UserSkill.
    """
    model = UserSkill
    extra = 0
    fields = ['skill_name', 'proficiency_level', 'years_of_experience', 'verified']


class UserAdmin(BaseUserAdmin):
    """
    Extended User admin with profile and skills.
    """
    inlines = (UserProfileInline, UserSkillInline)
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for UserProfile model.
    """
    list_display = [
        'user', 'full_name', 'experience_level', 'learning_style', 
        'weekly_learning_hours', 'public_profile', 'created_at'
    ]
    list_filter = ['experience_level', 'learning_style', 'public_profile', 'email_notifications']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'bio', 'interests']
    readonly_fields = ['created_at', 'updated_at', 'full_name', 'total_learning_paths', 'total_courses_added']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'full_name')
        }),
        ('Profile Details', {
            'fields': ('bio', 'avatar', 'birth_date', 'location')
        }),
        ('Social Links', {
            'fields': ('website', 'github_username', 'linkedin_profile', 'twitter_handle')
        }),
        ('Learning Preferences', {
            'fields': ('experience_level', 'learning_style', 'interests', 'goals', 'weekly_learning_hours')
        }),
        ('Settings', {
            'fields': ('time_zone', 'email_notifications', 'public_profile')
        }),
        ('Statistics', {
            'fields': ('total_learning_paths', 'total_courses_added'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    """
    Admin configuration for UserSkill model.
    """
    list_display = ['user', 'skill_name', 'proficiency_level', 'years_of_experience', 'verified', 'created_at']
    list_filter = ['proficiency_level', 'verified', 'created_at']
    search_fields = ['user__username', 'skill_name', 'notes']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Skill Information', {
            'fields': ('user', 'skill_name', 'proficiency_level', 'years_of_experience')
        }),
        ('Verification', {
            'fields': ('verified', 'notes')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )