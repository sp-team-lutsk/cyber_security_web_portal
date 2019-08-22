from rest_framework import serializers
from django.contrib.auth import get_user_model 

from .models import Student, Teacher, Faculty, Profession

from rest_framework.authentication import BasicAuthentication, SessionAuthentication

User = get_user_model()

class FacultySerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Faculty
        fields = ('name',)

class ProfessionSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Profession
        fields = ('name',)

class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField() 

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

            'password',
        )

        extra_kwargs = {'password': {'write_only': True}}

class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    faculty = FacultySerializer(many=False)

    class Meta(object):
        model = Teacher
        fields = (
            'user',
            'faculty',
        )


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    faculty = FacultySerializer(many=False)
    profession = ProfessionSerializer(many=False)

    class Meta(object):
        model = Student
        fields = ( 
            'user',
            'faculty',
            'profession',
        )

class SocialSerializer(serializers.Serializer):
    """
    Serializer which accepts an OAuth2 access token and provider.
    """
    provider = serializers.CharField(max_length=255, required=True)
    access_token = serializers.CharField(max_length=4096, required=True, trim_whitespace=True)

