from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator


class Category(models.Model):
    """
    Model representing course categories.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Name of the category"
    )
    description = models.TextField(
        blank=True,
        help_text="Description of the category"
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        help_text="URL-friendly version of the category name"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name


class Course(models.Model):
    """
    Model representing individual courses that can be part of learning paths.
    """
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    TYPE_CHOICES = [
        ('video', 'Video Course'),
        ('text', 'Text-based Course'),
        ('interactive', 'Interactive Course'),
        ('project', 'Project-based Course'),
        ('book', 'Book/eBook'),
        ('article', 'Article/Blog Post'),
        ('tutorial', 'Tutorial'),
        ('workshop', 'Workshop'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(
        max_length=200,
        help_text="Title of the course"
    )
    description = models.TextField(
        help_text="Detailed description of the course content"
    )
    short_description = models.CharField(
        max_length=300,
        help_text="Brief summary of the course"
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_courses',
        help_text="User who added this course"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses',
        help_text="Category this course belongs to"
    )
    difficulty_level = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default='beginner',
        help_text="Difficulty level of this course"
    )
    course_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='video',
        help_text="Type of course content"
    )
    duration_hours = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(500)],
        help_text="Estimated duration to complete this course in hours"
    )
    url = models.URLField(
        validators=[URLValidator()],
        help_text="URL to access the course"
    )
    instructor = models.CharField(
        max_length=200,
        blank=True,
        help_text="Name of the course instructor or author"
    )
    platform = models.CharField(
        max_length=100,
        blank=True,
        help_text="Platform where the course is hosted (e.g., Coursera, Udemy, YouTube)"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Course price (0.00 for free courses)"
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        help_text="Course rating (0.0 to 5.0)"
    )
    total_ratings = models.PositiveIntegerField(
        default=0,
        help_text="Total number of ratings"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='published',
        help_text="Current status of the course"
    )
    tags = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma-separated tags for categorization"
    )
    prerequisites = models.TextField(
        blank=True,
        help_text="Prerequisites needed before taking this course"
    )
    learning_outcomes = models.TextField(
        blank=True,
        help_text="What students will learn from this course"
    )
    language = models.CharField(
        max_length=50,
        default='English',
        help_text="Primary language of the course"
    )
    certificate_available = models.BooleanField(
        default=False,
        help_text="Whether a certificate is available upon completion"
    )
    is_public = models.BooleanField(
        default=True,
        help_text="Whether this course is visible to other users"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
    
    def __str__(self):
        return f"{self.title} ({self.platform})"
    
    @property
    def is_free(self):
        """Check if the course is free."""
        return self.price == 0.00
    
    @property
    def tag_list(self):
        """Return tags as a list."""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    @property
    def average_rating_display(self):
        """Return formatted average rating."""
        if self.rating:
            return f"{self.rating:.1f}/5.0"
        return "No ratings yet"


class CourseReview(models.Model):
    """
    Model for user reviews of courses.
    """
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='course_reviews'
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    review_text = models.TextField(
        blank=True,
        help_text="Optional review text"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['course', 'user']
        ordering = ['-created_at']
        verbose_name = 'Course Review'
        verbose_name_plural = 'Course Reviews'
    
    def __str__(self):
        return f"{self.user.username} - {self.course.title} ({self.rating}/5)"


class UserCourseProgress(models.Model):
    """
    Model to track user progress through individual courses.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='course_progress'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='user_progress'
    )
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    progress_percentage = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Progress percentage (0-100)"
    )
    time_spent_hours = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0.00,
        help_text="Time spent on this course in hours"
    )
    notes = models.TextField(
        blank=True,
        help_text="User's personal notes about the course"
    )
    
    class Meta:
        unique_together = ['user', 'course']
        verbose_name = 'User Course Progress'
        verbose_name_plural = 'User Course Progress'
    
    def __str__(self):
        return f"{self.user.username} - {self.course.title} ({self.progress_percentage}%)"
    
    @property
    def is_completed(self):
        """Check if the course is completed."""
        return self.completed_at is not None