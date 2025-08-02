from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import UserProfile, UserSkill


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password_confirm']
    
    def validate(self, attrs):
        """
        Validate that passwords match.
        """
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs
    
    def validate_email(self, value):
        """
        Validate that email is unique.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def create(self, validated_data):
        """
        Create a new user with encrypted password.
        """
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UserSkillSerializer(serializers.ModelSerializer):
    """
    Serializer for UserSkill model.
    """
    class Meta:
        model = UserSkill
        fields = [
            'id', 'skill_name', 'proficiency_level', 'years_of_experience',
            'verified', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for UserProfile model.
    """
    user = UserSerializer(read_only=True)
    skills = UserSkillSerializer(many=True, read_only=True, source='user.skills')
    full_name = serializers.ReadOnlyField()
    interest_list = serializers.ReadOnlyField()
    total_learning_paths = serializers.ReadOnlyField()
    total_courses_added = serializers.ReadOnlyField()
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'bio', 'avatar', 'birth_date', 'location', 'website',
            'github_username', 'linkedin_profile', 'twitter_handle',
            'experience_level', 'learning_style', 'interests', 'goals',
            'time_zone', 'weekly_learning_hours', 'email_notifications',
            'public_profile', 'created_at', 'updated_at', 'skills',
            'full_name', 'interest_list', 'total_learning_paths',
            'total_courses_added'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile.
    """
    class Meta:
        model = UserProfile
        fields = [
            'bio', 'avatar', 'birth_date', 'location', 'website',
            'github_username', 'linkedin_profile', 'twitter_handle',
            'experience_level', 'learning_style', 'interests', 'goals',
            'time_zone', 'weekly_learning_hours', 'email_notifications',
            'public_profile'
        ]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT token serializer that includes user profile information.
    """
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add user profile information to response
        user_profile = UserProfile.objects.get(user=self.user)
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'profile': UserProfileSerializer(user_profile).data
        }
        
        return data


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for changing user password.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, attrs):
        """
        Validate that new passwords match.
        """
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match.")
        return attrs
    
    def validate_old_password(self, value):
        """
        Validate that old password is correct.
        """
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value
    
    def save(self):
        """
        Save the new password.
        """
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user