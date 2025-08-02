# Learning Path Generator

A comprehensive Django REST API application for creating personalized learning journeys and managing educational content. This platform allows users to create custom learning paths, discover courses, track progress, and build a community around shared learning goals.

## 🚀 Features

### Core Functionality
- **Personalized Learning Paths**: Create custom learning journeys with curated courses
- **Course Management**: Add, organize, and discover educational content from various platforms
- **Progress Tracking**: Monitor learning progress with detailed analytics and insights
- **User Authentication**: Secure JWT-based authentication with user profiles
- **Search & Filtering**: Advanced search capabilities with multiple filter options
- **Community Features**: Share learning paths and discover content created by others

### Technical Features
- **RESTful API**: Comprehensive API built with Django REST Framework
- **Interactive Documentation**: Auto-generated API documentation with Swagger/OpenAPI
- **Responsive UI**: Modern, mobile-friendly web interface
- **Admin Interface**: Full-featured Django admin for content management
- **Database Models**: Well-designed relational database schema
- **Authentication & Authorization**: Token-based authentication with proper permissions

## 🛠 Technologies Used

### Backend
- **Django 5.2.4**: Web framework
- **Django REST Framework**: API development
- **Simple JWT**: JWT authentication
- **django-filter**: Advanced filtering
- **django-cors-headers**: CORS support
- **drf-yasg**: API documentation
- **Pillow**: Image processing

### Frontend
- **HTML5/CSS3**: Modern web standards
- **Bootstrap 5**: Responsive design framework
- **JavaScript (ES6+)**: Interactive functionality
- **Axios**: HTTP client for API calls

### Database
- **SQLite**: Development database (easily configurable for PostgreSQL/MySQL)

## 📋 Installation & Setup

### Prerequisites
- Python 3.11+
- pip (Python package manager)
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd learning_path_generator
   ```

2. **Create and activate virtual environment**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser account**
   ```bash
   python manage.py createsuperuser
   ```

6. **Load sample data (optional)**
   ```bash
   python manage.py shell < populate_data.py
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Web Interface: http://127.0.0.1:8000
   - API Documentation: http://127.0.0.1:8000/api/docs/
   - Admin Interface: http://127.0.0.1:8000/admin/

## 🎯 Usage

### Demo Credentials
For testing purposes, use these demo credentials:
- **Username**: `demo`
- **Password**: `demo123456`

### API Endpoints

#### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login (JWT token)
- `POST /api/auth/refresh/` - Refresh JWT token
- `GET /api/auth/dashboard/` - User dashboard data

#### Learning Paths
- `GET /api/learning-paths/` - List all learning paths
- `POST /api/learning-paths/` - Create new learning path
- `GET /api/learning-paths/{id}/` - Get learning path details
- `PUT/PATCH /api/learning-paths/{id}/` - Update learning path
- `DELETE /api/learning-paths/{id}/` - Delete learning path
- `POST /api/learning-paths/{id}/start_learning/` - Start learning path

#### Courses
- `GET /api/courses/` - List all courses
- `POST /api/courses/` - Create new course
- `GET /api/courses/{id}/` - Get course details
- `PUT/PATCH /api/courses/{id}/` - Update course
- `DELETE /api/courses/{id}/` - Delete course
- `GET /api/courses/featured/` - Get featured courses
- `GET /api/courses/free_courses/` - Get free courses

#### Categories
- `GET /api/categories/` - List all categories
- `POST /api/categories/` - Create new category

#### User Management
- `GET /api/profiles/me/` - Get current user profile
- `PUT/PATCH /api/profiles/update_me/` - Update user profile
- `POST /api/profiles/change_password/` - Change password

### Web Interface Features

#### For All Users
- Browse learning paths and courses
- View detailed information about content
- Search and filter content
- View public statistics

#### For Authenticated Users
- Create and manage learning paths
- Add and organize courses
- Track learning progress
- Manage user profile and skills
- Access personal dashboard

## 🏗 Project Structure

```
learning_path_generator/
├── learning_platform/          # Main Django project
│   ├── settings.py             # Django settings
│   ├── urls.py                 # URL configuration
│   ├── views.py                # Template views
│   └── wsgi.py                 # WSGI configuration
├── authentication/             # User authentication app
│   ├── models.py               # User profile and skills models
│   ├── serializers.py          # DRF serializers
│   ├── views.py                # API views
│   └── admin.py                # Admin configuration
├── learning_paths/             # Learning paths app
│   ├── models.py               # Learning path models
│   ├── serializers.py          # DRF serializers
│   ├── views.py                # API views
│   └── permissions.py          # Custom permissions
├── courses/                    # Courses app
│   ├── models.py               # Course and category models
│   ├── serializers.py          # DRF serializers
│   ├── views.py                # API views
│   └── admin.py                # Admin configuration
├── templates/                  # HTML templates
│   ├── base/                   # Base templates
│   ├── auth/                   # Authentication templates
│   ├── learning_paths/         # Learning path templates
│   └── courses/                # Course templates
├── static/                     # Static files
│   ├── css/                    # Stylesheets
│   ├── js/                     # JavaScript files
│   └── images/                 # Images
├── media/                      # User uploaded files
├── requirements.txt            # Python dependencies
└── manage.py                   # Django management script
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file for production settings:
```env
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost/dbname
```

### Database Configuration
For production, update `settings.py` to use PostgreSQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'learning_path_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

For API testing, use the interactive documentation at `/api/docs/` or tools like:
- Postman
- Insomnia
- curl commands

## 📚 API Documentation

The API is fully documented using OpenAPI/Swagger. Access the interactive documentation at:
- **Swagger UI**: `/api/docs/`
- **ReDoc**: `/api/redoc/`
- **JSON Schema**: `/api/schema/`

## 🚀 Deployment

### Production Checklist
1. Set `DEBUG = False` in settings
2. Configure proper database (PostgreSQL recommended)
3. Set up static file serving
4. Configure CORS settings
5. Set up proper logging
6. Use environment variables for sensitive data
7. Set up SSL/HTTPS
8. Configure proper backup strategy

### Docker Deployment (Optional)
Create a `Dockerfile` for containerized deployment:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Write comprehensive docstrings
- Add tests for new features
- Update documentation as needed
- Use meaningful commit messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django and Django REST Framework communities
- Bootstrap for the responsive design framework
- All the open-source libraries that made this project possible

## 📞 Support

For support, email support@learningpathgenerator.com or create an issue in the repository.

## 🔮 Future Enhancements

- [x] Advanced analytics and reporting
- [x] Social learning features
- [ ] Mobile app development
- [ ] Integration with external learning platforms
- [ ] Gamification features
- [ ] AI-powered course recommendations
- [ ] Video content support
- [ ] Offline learning capabilities
- [ ] Multi-language support
- [ ] Advanced search with Elasticsearch

---

**Happy Learning! 🎓**
