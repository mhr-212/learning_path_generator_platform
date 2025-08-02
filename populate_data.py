from django.contrib.auth.models import User
from courses.models import Category, Course
from learning_paths.models import LearningPath, LearningPathCourse

# Create demo user
demo_user, created = User.objects.get_or_create(
    username='demo',
    defaults={
        'email': 'demo@example.com',
        'first_name': 'Demo',
        'last_name': 'User'
    }
)
if created:
    demo_user.set_password('demo123456')
    demo_user.save()

# Create categories
categories = [
    {'name': 'Programming', 'slug': 'programming', 'description': 'Programming languages and software development'},
    {'name': 'Data Science', 'slug': 'data-science', 'description': 'Data analysis, machine learning, and statistics'},
    {'name': 'Web Development', 'slug': 'web-development', 'description': 'Frontend and backend web development'},
    {'name': 'Mobile Development', 'slug': 'mobile-development', 'description': 'iOS and Android app development'},
    {'name': 'DevOps', 'slug': 'devops', 'description': 'Development operations and infrastructure'},
]

for cat_data in categories:
    Category.objects.get_or_create(
        slug=cat_data['slug'],
        defaults=cat_data
    )

# Create sample courses
programming_cat = Category.objects.get(slug='programming')
web_dev_cat = Category.objects.get(slug='web-development')
data_science_cat = Category.objects.get(slug='data-science')

courses_data = [
    {
        'title': 'Python for Beginners',
        'short_description': 'Learn Python programming from scratch',
        'description': 'A comprehensive introduction to Python programming covering basics, data structures, and object-oriented programming.',
        'category': programming_cat,
        'difficulty_level': 'beginner',
        'course_type': 'video',
        'duration_hours': 20,
        'url': 'https://example.com/python-beginners',
        'instructor': 'John Smith',
        'platform': 'Example Learning',
        'price': 0.00,
        'language': 'English',
        'tags': 'python, programming, beginner',
        'learning_outcomes': 'Understand Python syntax, work with data structures, create simple programs',
        'creator': demo_user
    },
    {
        'title': 'JavaScript Fundamentals',
        'short_description': 'Master the basics of JavaScript programming',
        'description': 'Learn JavaScript from the ground up, including ES6+ features, DOM manipulation, and asynchronous programming.',
        'category': web_dev_cat,
        'difficulty_level': 'beginner',
        'course_type': 'video',
        'duration_hours': 25,
        'url': 'https://example.com/javascript-fundamentals',
        'instructor': 'Jane Doe',
        'platform': 'Code Academy',
        'price': 49.99,
        'language': 'English',
        'tags': 'javascript, web development, frontend',
        'learning_outcomes': 'Build interactive web pages, understand modern JavaScript features',
        'creator': demo_user
    },
    {
        'title': 'Data Analysis with Pandas',
        'short_description': 'Analyze data using Python Pandas library',
        'description': 'Learn to manipulate, clean, and analyze data using the powerful Pandas library in Python.',
        'category': data_science_cat,
        'difficulty_level': 'intermediate',
        'course_type': 'video',
        'duration_hours': 15,
        'url': 'https://example.com/pandas-analysis',
        'instructor': 'Dr. Sarah Wilson',
        'platform': 'DataCamp',
        'price': 0.00,
        'language': 'English',
        'tags': 'pandas, data analysis, python',
        'learning_outcomes': 'Clean and analyze datasets, create visualizations',
        'creator': demo_user
    },
    {
        'title': 'React.js Complete Guide',
        'short_description': 'Build modern web applications with React',
        'description': 'Complete guide to React.js including hooks, context, routing, and state management.',
        'category': web_dev_cat,
        'difficulty_level': 'intermediate',
        'course_type': 'video',
        'duration_hours': 40,
        'url': 'https://example.com/react-complete',
        'instructor': 'Mike Johnson',
        'platform': 'Udemy',
        'price': 89.99,
        'language': 'English',
        'tags': 'react, javascript, frontend, spa',
        'learning_outcomes': 'Build complex React applications, manage state effectively',
        'creator': demo_user
    },
    {
        'title': 'Machine Learning Basics',
        'short_description': 'Introduction to machine learning concepts',
        'description': 'Learn the fundamentals of machine learning including supervised and unsupervised learning.',
        'category': data_science_cat,
        'difficulty_level': 'intermediate',
        'course_type': 'video',
        'duration_hours': 30,
        'url': 'https://example.com/ml-basics',
        'instructor': 'Prof. Alex Chen',
        'platform': 'Coursera',
        'price': 79.99,
        'language': 'English',
        'tags': 'machine learning, ai, python, scikit-learn',
        'learning_outcomes': 'Understand ML algorithms, build predictive models',
        'creator': demo_user
    }
]

created_courses = []
for course_data in courses_data:
    course, created = Course.objects.get_or_create(
        title=course_data['title'],
        defaults=course_data
    )
    created_courses.append(course)

# Create sample learning paths
learning_paths_data = [
    {
        'title': 'Full Stack Web Development',
        'description': 'Complete path to become a full stack web developer, covering both frontend and backend technologies.',
        'difficulty_level': 'intermediate',
        'estimated_duration_hours': 120,
        'status': 'published',
        'tags': 'web development, full stack, javascript, python',
        'prerequisites': 'Basic computer skills and familiarity with HTML/CSS',
        'learning_objectives': 'Build complete web applications from scratch, understand both frontend and backend development',
        'is_public': True,
        'creator': demo_user,
        'courses': [created_courses[1], created_courses[3]]  # JavaScript and React
    },
    {
        'title': 'Data Science Fundamentals',
        'description': 'Learn the essential skills for data science including programming, statistics, and machine learning.',
        'difficulty_level': 'beginner',
        'estimated_duration_hours': 80,
        'status': 'published',
        'tags': 'data science, python, machine learning, analytics',
        'prerequisites': 'Basic mathematics and statistics knowledge',
        'learning_objectives': 'Analyze data, build predictive models, create data visualizations',
        'is_public': True,
        'creator': demo_user,
        'courses': [created_courses[0], created_courses[2], created_courses[4]]  # Python, Pandas, ML
    },
    {
        'title': 'Programming for Beginners',
        'description': 'Start your programming journey with Python and build a solid foundation in computer science.',
        'difficulty_level': 'beginner',
        'estimated_duration_hours': 40,
        'status': 'published',
        'tags': 'programming, python, beginner, computer science',
        'prerequisites': 'No prior programming experience required',
        'learning_objectives': 'Understand programming concepts, write clean code, solve problems algorithmically',
        'is_public': True,
        'creator': demo_user,
        'courses': [created_courses[0]]  # Python for Beginners
    }
]

for path_data in learning_paths_data:
    courses = path_data.pop('courses')
    learning_path, created = LearningPath.objects.get_or_create(
        title=path_data['title'],
        defaults=path_data
    )
    
    if created:
        # Add courses to the learning path
        for i, course in enumerate(courses, 1):
            LearningPathCourse.objects.create(
                learning_path=learning_path,
                course=course,
                order=i,
                is_required=True
            )

print("Sample data created successfully!")