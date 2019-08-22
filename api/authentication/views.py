from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
import settings
from rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from django.contrib.auth import get_user_model

from .serializers import UserSerializer, StudentSerializer, TeacherSerializer, SocialSerializer
from .models import Student, Teacher

User = get_user_model()

class CreateUserAPIView(APIView):
    """
    Create user
    """
    # Allow any user (authenticated or not) to access this url
    permission_classes = (AllowAny,)
 
    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserListAPIView(ListAPIView):
    """
    All users in db (for test)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class StudentListAPIView(ListAPIView):
    """
    All students in db (for test)
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class TeacherListAPIView(UserListAPIView):
    """
    All teachers in db (for test)
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    access_token = settings.base.FACEBOOK_ACCESS_TOKEN
