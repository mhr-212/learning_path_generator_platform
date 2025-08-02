from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    Extended user profile model to store additional user information.
    """
    EXPERIENCE_CHOICES = [
        ('beginner', 'Beginner (0-1 years)'),
        ('intermediate', 'Intermediate (1-3 years)'),
        ('advanced', 'Advanced (3-5 years)'),
        ('expert', 'Expert (5+ years)'),
    ]
    
    LEARNING_STYLE_CHOICES = [
        ('visual', 'Visual Learner'),
        ('auditory', 'Auditory Learner'),
        ('kinesthetic', 'Kinesthetic Learner'),
        ('reading', 'Reading/Writing Learner'),
        ('mixed', 'Mixed Learning Style'),
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        help_text="Brief biography or description"
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        help_text="Profile picture"
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date of birth"
    )
    location = models.CharField(
        max_length=100,
        blank=True,
        help_text="City, Country"
    )
    website = models.URLField(
        blank=True,
        help_text="Personal website or portfolio"
    )
    github_username = models.CharField(
        max_length=100,
        blank=True,
        help_text="GitHub username"
    )
    linkedin_profile = models.URLField(
        blank=True,
        help_text="LinkedIn profile URL"
    )
    twitter_handle = models.CharField(
        max_length=100,
        blank=True,
        help_text="Twitter handle (without @)"
    )
    experience_level = models.CharField(
        max_length=20,
        choices=EXPERIENCE_CHOICES,
        default='beginner',
        help_text="Overall experience level in technology/programming"
    )
    learning_style = models.CharField(
        max_length=20,
        choices=LEARNING_STYLE_CHOICES,
        default='mixed',
        help_text="Preferred learning style"
    )
    interests = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma-separated list of interests and topics"
    )
    goals = models.TextField(
        blank=True,
        help_text="Learning goals and career objectives"
    )
    time_zone = models.CharField(
        max_length=50,
        default='UTC',
        help_text="User's time zone"
    )
    weekly_learning_hours = models.PositiveIntegerField(
        default=5,
        help_text="Target hours per week for learning"
    )
    email_notifications = models.BooleanField(
        default=True,
        help_text="Receive email notifications"
    )
    public_profile = models.BooleanField(
        default=True,
        help_text="Make profile visible to other users"
    )
    first_login = models.BooleanField(
        default=True,
        help_text="True if the user has not logged in before"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    @property
    def full_name(self):
        """Return user's full name."""
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username
    
    @property
    def interest_list(self):
        """Return interests as a list."""
        return [interest.strip() for interest in self.interests.split(',') if interest.strip()]
    
    @property
    def total_learning_paths(self):
        """Return total number of learning paths created by user."""
        return self.user.created_learning_paths.count()
    
    @property
    def total_courses_added(self):
        """Return total number of courses added by user."""
        return self.user.created_courses.count()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to automatically create a UserProfile when a User is created.
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal to save the UserProfile when the User is saved.
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()


class UserSkill(models.Model):
    """
    Model to track user skills and proficiency levels.
    """
    PROFICIENCY_CHOICES = [
        ('novice', 'Novice'),
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='skills'
    )
    skill_name = models.CharField(
        max_length=100,
        help_text="Name of the skill (e.g., Python, JavaScript, Machine Learning)"
    )
    proficiency_level = models.CharField(
        max_length=20,
        choices=PROFICIENCY_CHOICES,
        default='novice',
        help_text="Current proficiency level in this skill"
    )
    years_of_experience = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        default=0.0,
        help_text="Years of experience with this skill"
    )
    verified = models.BooleanField(
        default=False,
        help_text="Whether this skill has been verified through assessments"
    )
    notes = models.TextField(
        blank=True,
        help_text="Additional notes about this skill"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'skill_name']
        ordering = ['-proficiency_level', 'skill_name']
        verbose_name = 'User Skill'
        verbose_name_plural = 'User Skills'
    
    def __str__(self):
        return f"{self.user.username} - {self.skill_name} ({self.proficiency_level})"
