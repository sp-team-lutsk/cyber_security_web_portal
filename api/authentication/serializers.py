from rest_framework import serializers
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from django.contrib.auth import (
        get_user_model, 
        authenticate,)
from django.db.models import Q

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
   
        user = User.objects.filter(
                Q(email=email)).distinct()

        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise serializers.ValidationError("This email is not valid")

        if user_obj:
            if not user_obj.check_password(password):
                raise serializers.ValidationError("Password incorrect")
            
            if not user_obj.is_active:
                raise serializers.ValidationError("User has been deactivated")
        
        data["token"] = user_obj.token

        return data

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
    teacher = TeacherSerializer(many=False, read_only=True)

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
   
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance
