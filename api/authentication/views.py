import settings

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter

from .serializers import (
    UserSerializer, 
    StudentSerializer, 
    TeacherSerializer, 
    SocialSerializer,
    CreateUserSerializer,
    LoginUserSerializer
)

from .models import Student, Teacher

User = get_user_model()

class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class CreateUserAPIView(APIView):
    """
    Create user
    """
    # Allow any user (authenticated or not) to access this url
    permission_classes = (AllowAny,)
    serializer_class = CreateUserSerializer

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        
        if serializer.is_valid(raise_exception=True):
            user_saved = serializer.save()
        
        return Response(
            data={"success": "User '{}' created successfully".format(str(user_saved))},
            status=status.HTTP_201_CREATED)

class LoginUserAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginUserSerializer
    
    def post(self, request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class StudentListAPIView(ListAPIView):
    """
    All students in db (for test)
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdminUser]

class TeacherListAPIView(ListAPIView):
    """
    All teachers in db (for test)
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAdminUser]

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    access_token = settings.base.FACEBOOK_ACCESS_TOKEN
