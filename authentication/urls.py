from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserRegistrationView, CustomTokenObtainPairView, UserProfileViewSet,
    UserSkillViewSet, user_dashboard, public_stats
)

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet)
router.register(r'skills', UserSkillViewSet, basename='user-skills')

urlpatterns = [
    # Authentication endpoints
    path('api/auth/register/', UserRegistrationView.as_view(), name='user-register'),
    path('api/auth/login/', CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    # Dashboard and stats
    path('api/auth/dashboard/', user_dashboard, name='user-dashboard'),
    path('api/stats/', public_stats, name='public-stats'),
    
    # Router URLs
    path('api/', include(router.urls)),
]
