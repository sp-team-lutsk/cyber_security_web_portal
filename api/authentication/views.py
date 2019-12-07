from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.views import APIView

from utils.permissions import AllowAny
from rest_framework.generics import (ListAPIView,
                                     DestroyAPIView,
                                     CreateAPIView)
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from authentication.serializers import (
    UserSerializer,
    CreateUserSerializer,
    UpdateUserSerializer,
    VerifyUserSerializer,
    VerifyUserPassSerializer,
    BulkUpdateUserSerializer,
    DeleteAllSerializer,
    RecoverySerializer,
    TeacherSerializer,
    CreateTeacherSerializer,
    UpdateTeacherSerializer,
    BulkUpdateTeacherSerializer,
    StudentSerializer,
    CreateStudentSerializer,
    UpdateStudentSerializer,
    BulkUpdateStudentSerializer,
    SetModeratorSerializer,
    NewsSubscriptionSerializer,)

from authentication.models import StdUser, Student, Teacher, Faculty, Profession

from utils.decorators import permission, permissions
from utils.views import get_user,send_mail

User = get_user_model()


class UserAPIView(ListAPIView, ListModelMixin, DestroyAPIView):
    lookup_field = 'id'
    serializer_class = UserSerializer
    permission_classes = [AllowAny, ]
    queryset = User.objects.all()

    @permission("IsStaffUser")
    def get(self, request, *args, **kwargs):
        number = args[0]
        try:
            queryset = User.objects.get(id=number.get('id'))
            if queryset:
                serializer = self.get_serializer(queryset)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except StdUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @permissions(["IsModeratorUser", "IsUser"],"kwargs")
    def put(self, request, *args, **kwargs):
        number = args[0]
        queryset = User.objects.filter(id=number.get('id'))
        self.serializer_class = UpdateUserSerializer
        serializer = self.serializer_class(queryset[0],  data=request.data)

        if(serializer.is_valid()):
            serializer.save()

        return Response(status=status.HTTP_200_OK)

    @permissions(["IsModeratorUser", "IsUser"],"kwargs")
    def delete(self, request, *args, **kwargs):
        number = args[0].get('id')
        user = User.objects.get(id=number)
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_200_OK)


class UsersAPIView(ListAPIView, CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = UserSerializer

    #@permission("IsStaffUser")
    def get(self, request, *args, **kwargs):
        self.queryset = User.objects.all()
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(
                data=serializer.data,
                status=status.HTTP_200_OK)

    def post(self, request):
        self.serializer_class = CreateUserSerializer
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        user_saved = serializer.save()

        return Response(status=status.HTTP_201_CREATED)

    @permission("IsModeratorUser")
    def put(self, request, *args, **kwargs):
        self.serializer_class = UpdateUserSerializer
        queryset = User.objects.all()

        serializer = BulkUpdateUserSerializer(queryset, many=True)
        return Response(
                data=serializer.data,
                status=status.HTTP_200_OK)

    @permission("IsModeratorUser")
    def delete(self, request, *args, **kwargs):
        queryset = User.objects.all()
        for user in list(queryset):
            user.is_active = False
            user.save()
        return Response(status=status.HTTP_200_OK)


class TeacherAPIView(ListAPIView, ListModelMixin, DestroyAPIView):
    lookup_field = 'id'
    serializer_class = UserSerializer
    queryset = User.objects.none()
    permission_classes = [AllowAny,]

    @permissions(["IsStaffUser", "IsUser"],"kwargs")
    def get(self, request, *args, **kwargs):
        number = kwargs.get('id')
        try:
            queryset = User.objects.get(id=number, is_teacher=True)
            if queryset:
                serializer = self.get_serializer(queryset)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
        except StdUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @permissions(["IsModeratorUser", "IsUser"],"kwargs")
    def post(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @permissions(["IsModeratorUser", "IsUser"],"kwargs")
    def put(self, request, *args, **kwargs):
        self.serializer_class = UpdateTeacherSerializer
        number = kwargs.get('id')
        queryset = Teacher.objects.filter(user=number)
        serializer = UpdateTeacherSerializer(queryset[0],  data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Status': 'Update success'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status = status.HTTP_404_NOT_FOUND)

    @permissions(["IsModeratorUser", "IsUser"],"kwargs")
    def delete(self, request, *args, **kwargs):
        number = kwargs.get('id')
        queryset = User.objects.filter(id=number, is_teacher=True)
        user = queryset[0]
        t = Teacher.objects.filter(id=user.teacher.id)
        t.delete()
        user.is_teacher = False
        user.save()
        return Response({'Status': 'OK'}, status=status.HTTP_200_OK)


class TeachersAPIView(ListAPIView):
    """
    All teachers in db (for test)
    """
    permission_classes = [AllowAny,]
    queryset = Teacher.objects.none()
    serializer_class = TeacherSerializer

    @permission("IsStaffUser")
    def get(self, request, *args, **kwargs):
        self.queryset = Teacher.objects.all()
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.serializer_class = CreateTeacherSerializer
        serializer = self.serializer_class(data=request.data)
        user = StdUser.objects.create_teacher(email=request.data.get('email'),
                                       password=request.data.get('password'),
                                       faculty=Faculty.objects.get(name = request.data.get('faculty')))
        return Response(
            data={"success": "User '{}' created successfully".format(str(user))},
            status=status.HTTP_201_CREATED)

    @permission("IsModeratorUser")
    def put(self, request, *args, **kwargs):
        self.serializer_class = BulkUpdateTeacherSerializer
        queryset = Teacher.objects.all()
        for user in list(queryset):
            serializer = UpdateTeacherSerializer(user,  data=request.data)
            if serializer.is_valid():
                serializer.save()
        return Response(data={"200": "OK"}, status=status.HTTP_200_OK)

    @permission("IsModeratorUser")
    def delete(self, request):
        q = User.objects.filter(is_teacher=True)
        for u in q:
            u.is_teacher = False
            t = Teacher.objects.filter(id=u.teacher.id)
            t.delete()
            u.save()
        return Response({'Status': 'OK'}, status=status.HTTP_200_OK)


class StudentAPIView(ListAPIView, ListModelMixin, DestroyAPIView):
    lookup_field = 'id'
    serializer_class = UserSerializer
    queryset = Student.objects.none()
    permission_classes = [AllowAny,]

    @permissions(["IsStaffUser", "IsUser"],"kwargs")
    def get(self, request, *args, **kwargs):
        number = kwargs.get('id')
        try:
            queryset = User.objects.filter(id=number, is_student=True)
            if queryset:
                serializer = self.get_serializer(queryset, many=True)
                return Response({'Status': 'User found'},serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'Status': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({'Status': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @permissions(["IsModeratorUser", "IsUser"],"kwargs")
    def post(self, request, *args, **kwargs):
        return Response({'Status': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @permissions(["IsModeratorUser", "IsUser"],"kwargs")
    def put(self, request, *args, **kwargs):
        self.serializer_class = UpdateStudentSerializer
        number = kwargs.get('id')
        queryset = Student.objects.filter(user=number)
        serializer = UpdateStudentSerializer(queryset[0],  data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Status': 'Update success'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors)

    @permissions(["IsModeratorUser", "IsUser"],"kwargs")
    def delete(self, request, *args, **kwargs):
        number = kwargs.get('id')
        queryset = User.objects.filter(id=number, is_student=True)
        user = queryset[0]
        s = Student.objects.filter(id=user.student.id)
        s.delete()
        user.is_student = False
        user.save()
        return Response({'Status': 'OK'}, status=status.HTTP_200_OK)


class StudentsAPIView(ListAPIView):
    """
    All teachers in db (for test)
    """
    permission_classes = [AllowAny,]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    @permission("IsStaffUser")
    def get(self, request, *args, **kwargs):
        self.queryset = Student.objects.all()
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.serializer_class = CreateStudentSerializer
        serializer = self.serializer_class(data=request.data)

        user_saved = StdUser.objects.create_student(email=request.data.get('email'),
                                       password=request.data.get('password'),
                                       faculty=Faculty.objects.get(name = request.data.get('faculty')),
                                       profession = Profession.objects.get(name = request.data.get('profession')))

        return Response(
                data={"success": "User '{}' created successfully".format(str(user_saved))},
                status=status.HTTP_201_CREATED)


    @permission("IsModeratorUser")
    def put(self, request, *args, **kwargs):
        self.serializer_class = BulkUpdateStudentSerializer
        queryset = Student.objects.all()

        for user in list(queryset):
            serializer = BulkUpdateStudentSerializer(user,  data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data={"200": "OK"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors)
    @permission("IsModeratorUser")
    def delete(self, request):
        q = User.objects.filter(is_student=True)
        for u in q:
            u.is_student = False

            s = Student.objects.filter(id=u.student.id)
            s.delete()

            u.save()
        return Response({'Status': 'OK'}, status=status.HTTP_200_OK)


class VerifyUserAPIView(APIView):
    """
    Verify User by email
    """
    lookup_field = 'code'
    queryset = User.objects.all()
    serializer_class = VerifyUserSerializer
    permission_classes = [AllowAny,]

    def get(self, request, **kwargs):
        code = kwargs.get('code')
        StdUser.verify_email(code)
        serializer = self.serializer_class(code, data=request.data)

        if serializer.is_valid(raise_exception=True):
            return Response({'Status': 'OK'}, status=status.HTTP_200_OK)


class VerifyPassUserAPIView(APIView):
    lookup_field = 'code'
    serializer_class = VerifyUserPassSerializer
    permission_classes = [AllowAny,]

    def post(self, request, **kwargs):
        code = kwargs.get('code')
        password = request.data.get('password')
        if StdUser.verify_password(code=code, password=password):
            serializer = self.serializer_class(code, data=request.data)

            if serializer.is_valid(raise_exception=True):
                return Response({'Status': 'OK'}, status=status.HTTP_200_OK)


class RecoveryAPIView(APIView):
    permission_classes = [AllowAny,]
    serializer_class = RecoverySerializer
    redirect_to = settings.LOGIN_REDIRECT_URL

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.post(data)

        if(serializer.is_valid(raise_exception=True)):
            new_data = serializer.data
            return Response(new_data, status=status.HTTP_200_OK)


class UserInactiveAPIView(APIView):

    def post(self, request, **kwargs):
        return Response({"Account inactive!"}, status=status.HTTP_400_BAD_REQUEST)


class SetModeratorAPIView(APIView):
    permission_classes = [AllowAny, ]
    queryset = User.objects.none()
    serializer_class = SetModeratorSerializer

    @permission('IsAdminUser')
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        user = get_user(id=request.data.get('id'))
        set_check = request.data.get('is_moderator')
        user.is_moderator = set_check
        user.save()
        return Response(data={"is_moderator": "{}".format(str(set_check))},
                    status=status.HTTP_200_OK)


class AdminUserAPIView(APIView):
    permission_classes = [AllowAny, ]
    queryset = User.objects.none()
    serializer_class = CreateUserSerializer

    #@permission("IsAdminUser")
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        user = StdUser()
        user.email = request.data.get('email')
        user.is_active = True
        password = request.data.get('password')
        user.set_password(password)
        serializer.is_valid(raise_exception=True)
        user.save()
        return Response(
                    data={"success": "User '{}' created successfully".format(str(request.data.get('email')))},
                    status=status.HTTP_201_CREATED)

    @permission("IsAdminUser")
    def delete(self, request, *args, **kwargs):
        self.serializer_class = SetModeratorSerializer
        serializer = SetModeratorSerializer(data=request.data)
        queryset = get_user(id=request.data.get('id'))
        user = queryset
        user.is_active = False
        user.save()
        return Response({'Status': 'OK'}, status=status.HTTP_200_OK)


class BanUserAPIView(APIView):
    permission_classes = [AllowAny, ]
    queryset = User.objects.none()
    serializer_class = SetModeratorSerializer

    @permission("IsModeratorUser")
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        queryset = get_user(id=request.data.get('id'))
        user = queryset
        user.is_active = False
        user.save()
        return Response({'Status': 'OK'}, status=status.HTTP_200_OK)


class NewsSubscriptionAPIView(APIView):
    queryset = User.objects.none()
    permission_classes = [AllowAny, ]
    serializer_class = NewsSubscriptionSerializer

    @permissions(["IsModeratorUser", "IsUser"],"args")
    def post(self, request, *args, **kwargs):
        user = get_user(id=request.data.get('id'))
        serializer = self.serializer_class(user, data=request.data)
        subscribe = request.data.get('news_subscription')
        user.news_subscription = subscribe
        user.save()
        if get_user(id=request.data.get('id')).news_subscription == True:
            subs = 'підписалися на розсилку новин'
        else:
            subs = 'відписалися від розсилки новин'
        if user.first_name == "":
            subject = 'Лист для тебе, користувач'
            body = 'Шановний користувач, вам надійшов цей лист, бо ви {}. Дякую за увагу.'.format(subs)
        else:
            subject = 'Лист для тебе, {}'.format(user.first_name)
            body = 'Шановний {}, вам надійшов цей лист, бо ви {}. Дякую за увагу.'.format(user.first_name, subs)
        send_mail(email=user.email,
                  subject = subject,
                  body = body)
        if serializer.is_valid(raise_exception=True):
            return Response(data={"news_subscription": "{}".format(str(subscribe))},
                    status=status.HTTP_200_OK)
        else:
            return Response(data={"User": "Not Found"},
                    status=status.HTTP_404_NOT_FOUND)
