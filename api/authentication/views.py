﻿from django.conf import settings 
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAdminUser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.generics import (RetrieveUpdateAPIView,
                                     RetrieveAPIView,
                                     ListAPIView,
                                     DestroyAPIView,
                                     RetrieveAPIView,
                                     CreateAPIView,
                                     GenericAPIView)
from rest_framework.mixins import UpdateModelMixin, ListModelMixin
from rest_framework.response import Response

from allauth.socialaccount import app_settings, providers
from allauth.socialaccount.providers.facebook.provider import GRAPH_API_URL, GRAPH_API_VERSION, FacebookProvider
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
    )
from allauth.socialaccount.models import SocialLogin, SocialToken
from allauth.socialaccount.providers.facebook.forms import FacebookConnectForm
from .serializers import (
    UserSerializer,
    DeleteUserSerializer,
    FindUserSerializer,
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
    SendMailSerializer,
   )

from .models import StdUser,Student, Teacher

User = get_user_model()


class UserAPIView(ListAPIView,ListModelMixin,DestroyAPIView):
    lookup_field = 'id'
    #permission_classes = [IsAuthenticated, ]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    def get(self,request,*args,**kwargs):
        number = kwargs.get('id')
        queryset = User.objects.filter(id=number)
        if queryset:
            serializer = self.get_serializer(queryset, many =True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'Status':'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self,request,*args,**kwargs):
        return Response({'Status':'Method not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def put(self, request, *args, **kwargs):
        self.serializer_class = UpdateUserSerializer
        number = kwargs.get('id')
        queryset = User.objects.filter(id=number)
        serializer = UpdateUserSerializer(queryset[0],  data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response({'Status': 'Update success'}, status=status.HTTP_200_OK)
        
    
    def delete(self,request,*args,**kwargs):
        #self.serializer_class = DeleteUserSerializer
        number = kwargs.get('id')
        queryset = User.objects.filter(id=number)
        user = queryset[0]
        user.is_active = False
        user.save()
        return Response({'Status':'OK'},status=status.HTTP_200_OK)

class UsersAPIView(ListAPIView,CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request):
        self.serializer_class = CreateUserSerializer    
        serializer = self.serializer_class(data=request.data)
       
        serializer.is_valid(raise_exception=True)
        user_saved = serializer.save()
        
        return Response(
                data={"success": "User '{}' created successfully".format(str(user_saved))},
                status=status.HTTP_201_CREATED)

    def put(self,request,*args,**kwargs):
        self.serializer_class = UpdateUserSerializer
        queryset = User.objects.all()
        
        for user in list(queryset):
            serializer = UpdateUserSerializer(user,  data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        
            return Response(serializer.errors)

    def delete(self,request):
        self.serializer_class=DeleteAllSerializer
        q = list(queryset)
        for u in q:
            serializer = self.serializer_class(request.user, data=request.data)
            serializer.delete(request)
        return Response({'Status':'OK'},status=status.HTTP_200_OK)

class TeacherAPIView(ListAPIView,ListModelMixin,DestroyAPIView):
    lookup_field = 'id'
    #permission_classes = [IsAuthenticated, ]
    serializer_class = UserSerializer
    queryset = Teacher.objects.all()
    
    def get(self,request,*args,**kwargs):
        number = kwargs.get('id')
        queryset = User.objects.filter(id=number,is_teacher=True)
        if queryset:
            serializer = self.get_serializer(queryset, many =True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'Status':'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self,request,*args,**kwargs):
        return Response({'Status':'Method not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def put(self, request, *args, **kwargs):
        self.serializer_class = UpdateTeacherSerializer
        number = kwargs.get('id')
        queryset = Teacher.objects.filter(user=number)
        serializer = UpdateTeacherSerializer(queryset[0],  data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Status': 'Update success'}, status=status.HTTP_200_OK)
        
    
    def delete(self,request,*args,**kwargs):
        #self.serializer_class = DeleteUserSerializer
        number = kwargs.get('id')
        queryset = User.objects.filter(id=number,is_teacher=True)
        user = queryset[0]
        user.teacher = None
        user.is_teacher = False
        user.save()
        return Response({'Status':'OK'},status=status.HTTP_200_OK)

class TeachersAPIView(ListAPIView):
    """
    All teachers in db (for test)
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAdminUser]

    def post(self, request):
        self.serializer_class = CreateTeacherSerializer    
        serializer = self.serializer_class(data=request.data)
       
        serializer.is_valid(raise_exception=True)
        user_saved = serializer.save()
        
        return Response(
                data={"success": "User '{}' created successfully".format(str(user_saved))},
                status=status.HTTP_201_CREATED)

    def put(self,request,*args,**kwargs):
        self.serializer_class = UpdateTeacherSerializer
        queryset = Teacher.objects.all()
        
        for user in list(queryset):
            serializer = UpdateTeacherSerializer(user,  data=request.data)
            if serializer.is_valid():
                serializer.save()
        return Response(data={ "200" : "OK"},status=status.HTTP_200_OK)

    def delete(self,request):
        self.serializer_class=DeleteAllSerializer
        q = User.objects.filter(is_teacher=True)
        for u in q:
            u.is_teacher = False
            u.teacher = None
            u.save()
        return Response({'Status':'OK'},status=status.HTTP_200_OK)


class StudentAPIView(ListAPIView,ListModelMixin,DestroyAPIView):
    lookup_field = 'id'
    #permission_classes = [IsAuthenticated, ]
    serializer_class = UserSerializer
    queryset = Student.objects.all()
    
    def get(self,request,*args,**kwargs):
        number = kwargs.get('id')
        queryset = User.objects.filter(id=number,is_student=True)
        if queryset:
            serializer = self.get_serializer(queryset, many =True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'Status':'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self,request,*args,**kwargs):
        return Response({'Status':'Method not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def put(self, request, *args, **kwargs):
        self.serializer_class = UpdateStudentSerializer
        number = kwargs.get('id')
        queryset = Student.objects.filter(user=number)
        serializer = UpdateStudentSerializer(queryset[0],  data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Status': 'Update success'}, status=status.HTTP_200_OK)

    def delete(self,request,*args,**kwargs):
        #self.serializer_class = DeleteUserSerializer
        number = kwargs.get('id')
        queryset = User.objects.filter(id=number,is_student=True)
        user = queryset[0]
        user.student = None
        user.is_student = False
        user.save()
        return Response({'Status':'OK'},status=status.HTTP_200_OK)

class StudentsAPIView(ListAPIView):
    """
    All teachers in db (for test)
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]

    def post(self, request):
        self.serializer_class = CreateStudentSerializer    
        serializer = self.serializer_class(data=request.data)
       
        serializer.is_valid(raise_exception=True)
        user_saved = serializer.save()
        
        return Response(
                data={"success": "User '{}' created successfully".format(str(user_saved))},
                status=status.HTTP_201_CREATED)

    def put(self,request,*args,**kwargs):
        self.serializer_class = UpdateStudentSerializer
        queryset = Student.objects.all()
        
        for user in list(queryset):
            serializer = UpdateStudentSerializer(user,  data=request.data)
            if serializer.is_valid():
                serializer.save()
        return Response(data={ "200" : "OK"},status=status.HTTP_200_OK)

    def delete(self,request):
        self.serializer_class=DeleteAllSerializer
        q = User.objects.filter(is_student=True)
        for u in q:
            u.is_student = False
            u.student = None
            u.save()
        return Response({'Status':'OK'},status=status.HTTP_200_OK)


class SendMailAPIView(APIView):
    """
    Send mail from admin to user
    """
    serializer_class = SendMailSerializer
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    
    def post(self, request):
        serializer = SendMailSerializer(data=request.data)
        user = self.queryset.get(email=request.data.get('email'))
        if user is not None:
            if serializer.is_valid(raise_exception=True):
                serializer.send(data=request.data)
                return Response({'Status': 'Mail Send'}, status=status.HTTP_200_OK)

class VerifyUserAPIView(APIView):
    """
    Verify User by email
    """
    lookup_field = 'code'
    queryset = User.objects.all()
    serializer_class = VerifyUserSerializer
    permission_classes = (AllowAny,)
    
    def get(self, request, **kwargs):
        code = kwargs.get('code')
        StdUser.verify_email(code)
        serializer = self.serializer_class(code, data=request.data)

        if serializer.is_valid(raise_exception=True):
            return Response({'Status':'OK'}, status=status.HTTP_200_OK)

class VerifyPassUserAPIView(APIView):
    lookup_field = 'code'
    serializer_class = VerifyUserPassSerializer
    permission_classes = (AllowAny,)
    
    def post(self, request, **kwargs):
        code = kwargs.get('code')
        password = request.data.get('password')
        if StdUser.verify_password(code=code, password=password):
            serializer = self.serializer_class(code, data=request.data)

            if serializer.is_valid(raise_exception=True):
                return Response({'Status':'OK'}, status=status.HTTP_200_OK)
        
class RecoveryAPIView(APIView):
    permission_classes = (AllowAny,)
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
