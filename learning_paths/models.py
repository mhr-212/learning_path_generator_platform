from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class LearningPath(models.Model):
    """
    Model representing a personalized learning path created by users.
    """
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(
        max_length=200,
        help_text="Title of the learning path"
    )
    description = models.TextField(
        help_text="Detailed description of what this learning path covers"
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_learning_paths',
        help_text="User who created this learning path"
    )
    difficulty_level = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default='beginner',
        help_text="Difficulty level of this learning path"
    )
    estimated_duration_hours = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(1000)],
        help_text="Estimated time to complete this learning path in hours"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        help_text="Current status of the learning path"
    )
    tags = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma-separated tags for categorization"
    )
    prerequisites = models.TextField(
        blank=True,
        help_text="Prerequisites needed before starting this learning path"
    )
    learning_objectives = models.TextField(
        help_text="What learners will achieve after completing this path"
    )
    is_public = models.BooleanField(
        default=True,
        help_text="Whether this learning path is visible to other users"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Many-to-many relationship with courses
    courses = models.ManyToManyField(
        'courses.Course',
        through='LearningPathCourse',
        related_name='learning_paths',
        blank=True
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Learning Path'
        verbose_name_plural = 'Learning Paths'
    
    def __str__(self):
        return f"{self.title} by {self.creator.username}"
    
    @property
    def total_courses(self):
        """Return the total number of courses in this learning path."""
        return self.courses.count()
    
    @property
    def tag_list(self):
        """Return tags as a list."""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]


class LearningPathCourse(models.Model):
    """
    Through model for the many-to-many relationship between LearningPath and Course.
    Allows ordering of courses within a learning path.
    """
    learning_path = models.ForeignKey(
        LearningPath,
        on_delete=models.CASCADE,
        related_name='path_courses'
    )
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name='path_courses'
    )
    order = models.PositiveIntegerField(
        default=1,
        help_text="Order of this course in the learning path"
    )
    is_required = models.BooleanField(
        default=True,
        help_text="Whether this course is required or optional"
    )
    notes = models.TextField(
        blank=True,
        help_text="Additional notes about this course in the context of the learning path"
    )
    
    class Meta:
        ordering = ['order']
        unique_together = ['learning_path', 'course']
        verbose_name = 'Learning Path Course'
        verbose_name_plural = 'Learning Path Courses'
    
    def __str__(self):
        return f"{self.learning_path.title} - {self.course.title} (Order: {self.order})"


class UserLearningProgress(models.Model):
    """
    Model to track user progress through learning paths.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='learning_progress'
    )
    learning_path = models.ForeignKey(
        LearningPath,
        on_delete=models.CASCADE,
        related_name='user_progress'
    )
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    current_course = models.ForeignKey(
        'courses.Course',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Current course the user is working on"
    )
    notes = models.TextField(
        blank=True,
        help_text="User's personal notes about their progress"
    )
    
    class Meta:
        unique_together = ['user', 'learning_path']
        verbose_name = 'User Learning Progress'
        verbose_name_plural = 'User Learning Progress'
    
    def __str__(self):
        return f"{self.user.username} - {self.learning_path.title} ({self.progress_percentage}%)"
    
    @property
    def is_completed(self):
        """Check if the learning path is completed."""
        return self.completed_at is not None

    def calculate_progress(self):
        """
        Calculate the progress of the learning path based on completed courses.
        """
        required_courses = self.learning_path.path_courses.filter(is_required=True)
        if not required_courses.exists():
            return 100 if self.completed_at else 0

        completed_courses = self.user.course_progress.filter(
            course__in=required_courses.values('course'),
            completed_at__isnull=False
        ).count()

        return int((completed_courses / required_courses.count()) * 100)
