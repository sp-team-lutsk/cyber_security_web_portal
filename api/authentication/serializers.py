from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework.response import Response

from authentication.models import (Student, Teacher, Faculty,
        Profession, ACAD_GROUPS_CHOICES)

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

        validate_password(password=validated_data.get('password',),
                user=validated_data.get('email'),
                password_validators=None)

        email = validated_data.get('email');
        user = User.objects.create_user(**validated_data, user_type=3)
        user.send_mail(email=email)
        return user


class RecoverySerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=64)

    class Meta(object):
        model = User
        fields = ('email',)

    def post(self, data):
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
        fields = ('code', 'password',)

    def post(self, data, code):
        user = User.objects.get(code=code)


class DeleteUserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User

        fields = ('email', 'password',)

    def delete(self, request, pk=None, **kwargs):
        request.user.is_active = False
        request.user.save()

        return Response(status=204)


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
    date_of_birth = serializers.ReadOnlyField()
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
        fields = (
            'email',
            'first_name',
            'last_name',
            'patronymic',
            'bio',
            'news_subscription'
        )

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


class UpdateTeacherSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer(many=False, read_only=True)

    class Meta(object):
        model = Teacher
        fields = ('faculty',)

    def save(self, user, data):
        try:
            name = data.get('faculty').get('name')
            f = Faculty.objects.get(name=name)
            user.faculty = f
            user.save()

        except Faculty.DoesNotExist:
            raise ValueError("Faculty does not exist")

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


class UpdateStudentSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer(many=False, read_only=True)
    profession = ProfessionSerializer(many=False, read_only=True)

    class Meta(object):
        model = Student
        fields = (
                'faculty',
                'profession',
                'acad_group',)

    def save(self, user, data):
        try:
            name = data.get('faculty').get('name')
            f = Faculty.objects.get(name=name)
            user.faculty = f

            name2 = data.get('profession').get('name')
            f2 = Profession.objects.get(name=name2)
            user.profession = f2


            name3 = data.get('acad_group')
            i=list(ACAD_GROUPS_CHOICES)

            for x in i:
                if user.acad_group == x[0] and x[0] == name3:
                    user.save()
                elif x[0]==name3:
                    user.acad_group=x[0]
                    user.save()

        except Faculty.DoesNotExist:
            raise ValueError("Faculty or Profession does not exist ")



class SetModeratorSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = User
        fields = (
                'id','is_moderator',)


class NewsSubscriptionSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = User
        fields = (
            'id', 'news_subscription',)
