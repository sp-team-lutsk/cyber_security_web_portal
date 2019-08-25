from rest_framework import serializers
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from django.contrib.auth import get_user_model 
from django.contrib.auth import authenticate

from .models import Student, Teacher, Faculty, Profession

User = get_user_model()

class FacultySerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Faculty
        fields = ('name',)

class ProfessionSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Profession
        fields = ('name',)

class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta(object):
        model = User
        fields = (
            'email',
            'password',
            'token'
        )
    
    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError("Email is required")

        if password is None:
            raise serializers.ValidationError("Password is required")
    
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("User with such email not found")

        if not user.is_active:
            raise serializers.ValidationError("User is deactivated")

        return {
            'email': user.email,
            'password': user.password,
            'token': user.token
        }

class CreateUserSerializer(serializers.ModelSerializer):
    read_only_fields = ('date_joined', 'token')

    class Meta(object):
        model = User
        fields = (
            'email',
            'password',
            'token',
        )
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class TeacherSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer(many=False)

    class Meta(object):
        model = Teacher
        fields = (
            'faculty',
        )

class StudentSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer(many=False)
    profession = ProfessionSerializer(many=False)

    class Meta(object):
        model = Student
        fields = ( 
            'faculty',
            'profession',
        )

class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField() 
    student = StudentSerializer(many=False, read_only=True)

    class Meta(object):
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'patronymic',
            'bio',
            'avatar',
            'date_of_birth',
            
            'date_joined',
            'last_update',
            
            'is_staff',
            'is_active',
            'is_superuser',
            'user_permissions',

            'is_student',
            'is_teacher',
            'student',
            'teacher',

            'password',
        )

        extra_kwargs = {'password': {'write_only': True}}


class SocialSerializer(serializers.Serializer):
    """
    Serializer which accepts an OAuth2 access token and provider.
    """
    provider = serializers.CharField(max_length=255, required=True)
    access_token = serializers.CharField(max_length=4096, required=True, trim_whitespace=True)


