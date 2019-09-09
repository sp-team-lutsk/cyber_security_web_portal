from django.contrib.auth.password_validation import validate_password 

from rest_framework import serializers
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from django.contrib.auth import (
        get_user_model, 
        authenticate,)
from django.db.models import Q

from rest_framework.response import Response

from .models import StdUser,Student, Teacher, Faculty, Profession

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
    email = serializers.CharField(max_length=64, write_only=True)
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
        
        new_data = {"token": user_obj.token}

        return new_data


class CreateUserSerializer(serializers.ModelSerializer):
    read_only_fields = ('date_joined', 'token')

    class Meta(object):
        model = User
        fields = (
            'email',
            'password',
        )

    def create(self, validated_data):

        if validate_password(password=validated_data.get('password',), user=validated_data.get('email'), password_validators=None) is not None:
            raise serializers.ValidationError(
            "Password must have at least:8 characters, one uppercase/lowercase letter, one symbol, one digit")
        
        email = validated_data.get('email')
        user = User.objects.create_user(**validated_data) 
        user.send_mail(email=email)
        return user

class RecoverySerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=64)
    
    class Meta(object):
        model = User
        fields = (
                'email',
                'password'
                )
        
    def post(self,data):
        print('password = ',data.get('password'))
        if validate_password(password=data.get('password',), user=data.get('email'), password_validators=None) is not None:
            raise serializers.ValidationError(                                
            "Password must have at least:8 characters, one uppercase/lowercase letter, one symbol, one digit")
        print('tyt')
        email = data.get('email', None)
        password = data.get('password',None)
        
        if email is None:
            raise serializers.ValidationError("Email is required")
                                 
        user = User.objects.filter(Q(email=email)).distinct()
                                 
        if user.exists() and user.count() == 1:
            user_obj = user.first()                                
            print(email)
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
        fields = (
                'code',
                )
    def get(self, data, code):
        user = User.objects.get(code=code)
        
class VerifyUserPassSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = (
                'code',
                'password',
                )
    def post(self, data, code):
        user = User.objects.get(code=code)
        

class DeleteUserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User

        fields = (
                'email',
                'password',
                )
        extra_kwargs = {'password': {'write_only' : True}}

    def delete(self, request, pk=None, **kwargs):
        request.user.is_active = False
        request.user.save()
        return Response(status = 204)

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

class FindUserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=20)

    class Meta(object):
        model = User
        
        fields = (
                'email',
                )

    def post(self, data):
         email = data.get('email')                                                          
         user = User.objects.get(email=email).first()
         return UserSerializer(user)    

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


class UpdateUserSerializer(serializers.ModelSerializer):
   
    class Meta(object):
        model = User
        exclude = (
                'email',
                'password',
                'is_staff', 
                'is_active', 
                'is_superuser', 
                'is_student', 
                'is_teacher',
                'username',
                'last_login',
                'groups',
                'user_permissions') 
