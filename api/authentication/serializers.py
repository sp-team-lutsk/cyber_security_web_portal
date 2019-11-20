from django.contrib.auth.password_validation import validate_password 

from rest_framework import serializers
from django.contrib.auth import (
        get_user_model, 
        authenticate,)
from django.db.models import Q

from rest_framework.response import Response

from authentication.models import StdUser,Student, Teacher, Faculty, Profession, ACAD_GROUPS_CHOICES
from utils.serializers import SendMailSerializer
User = get_user_model()


class FacultySerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Faculty
        fields = ('name',)

class ProfessionSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Profession
        fields = ('name',)


class CreateUserSerializer(serializers.ModelSerializer):
    read_only_fields = ('date_joined',)

    class Meta(object):
        model = User
        fields = (
            'email',
            'password',
        )

    def create(self, validated_data):

        validate_password(password=validated_data.get('password',), user=validated_data.get('email'), password_validators=None)
        
        email = validated_data.get('email')
        user = User.objects.create_user(**validated_data) 
        user.send_mail(email=email)
        return user

class RecoverySerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=64)
    
    class Meta(object):
        model = User
        fields = ('email',)
        
    def post(self,data):
        email = data.get('email', None)
                
        user = User.objects.filter(Q(email=email)).distinct()
                                 
        if user.exists() and user.count() == 1:
            user_obj = user.first()                                
            user_obj.send_recovery_password(email=email)
        else:
            raise serializers.ValidationError("This email is not valid")
        
        if user_obj:
            if not user_obj.is_active:
                raise serializers.ValidationError("User not active")
        return data

class VerifyUserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ('code',)

class VerifyUserPassSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=64)

    class Meta(object):
        model = User
        fields = ('code',
                'password',)
    
    def post(self, data, code):
        user = User.objects.get(code=code)

class DeleteUserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User

        fields = ('email',
                'password',)

    def delete(self, request, pk=None, **kwargs):
        request.user.is_active = False
        request.user.save()
        
        return Response(status = 204)

class TeacherSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer(many=False)

    class Meta(object):
        model = Teacher
        fields = (
            'user',
            'faculty',
        )

class StudentSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer(many=False)
    profession = ProfessionSerializer(many=False)
    acad_group = ACAD_GROUPS_CHOICES

    class Meta(object):
        model = Student
        fields = (
            'user', 
            'faculty',
            'profession',
            'acad_group',
        )

class FindUserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField() 
    email = serializers.ReadOnlyField()
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
            
                'news_subscription',
                'is_moderator',
                'is_active',
                'is_admin',

                'is_student',
                'is_teacher',
                'student',
                'teacher',

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
            
            'news_subscription',
            'is_active',
            'is_admin',
            'is_moderator',
            'user_permissions',

            'is_student',
            'is_teacher',
            'student',
            'teacher',

            'password',
        )

        extra_kwargs = {'password': {'write_only': True}}


class UpdateUserSerializer(serializers.ModelSerializer):
   
    class Meta(object):
        model = User
        exclude = (
                'email',
                'id',
                'password',
                'is_moderator', 
                'is_active', 
                'is_admin',
                'is_student', 
                'is_teacher',
                'username',
                'last_login',
                'groups',
                'code',
                'user_permissions')

class BulkUpdateUserSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = User
        fields = ('first_name',
                  'last_name',
                  'patronymic',
                  'bio',
                  'avatar',
                  'date_of_birth',
                  'news_subscription',
                  'user_permissions')

class DeleteAllSerializer(serializers.ModelSerializer):
    
    class Meta(object):
        model = User
        fields = ('email',
                  'password')

class CreateTeacherSerializer(serializers.ModelSerializer):
    faculty = serializers.CharField(max_length=128)
    read_only_fields = ('date_joined',)

    class Meta(object):
        model = User
        fields = (
            'email',
            'password',
            'faculty',
        )

    def create(self, validated_data):

        validate_password(password=validated_data.get('password',), user=validated_data.get('email'), password_validators=None)
        
        email = validated_data.get('email')
        user = User.objects.create_teacher(**validated_data) 
        user.send_mail(email=email)
        return user

class UpdateTeacherSerializer(serializers.ModelSerializer):
   
    class Meta(object):
        model = Teacher
        fields = (
                'faculty',)

class BulkUpdateTeacherSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Teacher
        fields = (
                'faculty',)

class CreateStudentSerializer(serializers.ModelSerializer):
    faculty = serializers.CharField(max_length=128)
    profession = serializers.CharField(max_length=128)
    acad_group = serializers.CharField(max_length=128)
    read_only_fields = ('date_joined',)

    class Meta(object):
        model = User
        fields = (
            'email',
            'password',
            'faculty',
            'profession',
            'acad_group',
        )

    def create(self, validated_data):

        validate_password(password=validated_data.get('password',), user=validated_data.get('email'), password_validators=None)
        
        email = validated_data.get('email')
        user = User.objects.create_student(**validated_data) 
        user.send_mail(email=email)
        return user

class UpdateStudentSerializer(serializers.ModelSerializer):
    faculty = serializers.CharField(max_length=128)
    profession = serializers.CharField(max_length=128)
    acad_group = serializers.CharField(max_length=128)
    
    class Meta(object):
        model = Student
        fields = (
                'faculty',
                'profession',
                'acad_group',)

class BulkUpdateStudentSerializer(serializers.ModelSerializer):
    faculty = serializers.CharField(max_length=128)
    profession = serializers.CharField(max_length=128)
    acad_group = serializers.CharField(max_length=128)
    
    class Meta(object):
        model = Student
        fields = (
                'faculty',
                'profession',
                'acad_group',)
 
class SetModeratorSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = User
        fields = (
                'id',)


