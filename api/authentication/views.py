import settings 
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.generics import (ListAPIView,
                                     DestroyAPIView,
                                     RetrieveAPIView,
                                     CreateAPIView,
                                     GenericAPIView)
from rest_framework.mixins import UpdateModelMixin
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
    StudentSerializer, 
    TeacherSerializer, 
    CreateUserSerializer,
    VerifyUserSerializer,
    VerifyUserPassSerializer,
    RecoverySerializer,
    UpdateUserSerializer,)

from .models import StdUser,Student, Teacher

User = get_user_model()

class FindUserAPIView(RetrieveAPIView):
    lookup_field = 'email'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class CreateUserAPIView(CreateAPIView):
    """
    Create user
    """
    # Allow any user (authenticated or not) to access this url
    permission_classes = (AllowAny,)
    serializer_class = CreateUserSerializer
    queryset = ''

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
       
        if serializer.is_valid(raise_exception=True):

            user_saved = serializer.save()
        
        return Response(
            data={"success": "User '{}' created successfully".format(str(user_saved))},
            status=status.HTTP_201_CREATED)

class VerifyUserAPIView(APIView):
    """
    Verify User by email
    """
    lookup_field = 'code'
    #queryset = User.objects.all()
    serializer_class = VerifyUserSerializer
    permission_classes = (AllowAny,)
    
    def get(self,request,**kwargs):
        code = kwargs.get('code')
        #user = User.objects.get(code=code)
        StdUser.verify_email(code)
        serializer = self.serializer_class(code,data=request.data)                                
                                 
        if serializer.is_valid(raise_exception=True):
            return Response({'Status':'OK'},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_200_OK)

class VerifyPassUserAPIView(APIView):
    lookup_field = 'code'
    #queryset = User.objects.all()
    serializer_class = VerifyUserPassSerializer
    permission_classes = (AllowAny,)
    
    def post(self,request,**kwargs):
        code = kwargs.get('code')
        #user = User.objects.get(code=code)
        if StdUser.verify_password(code,password) is False:
            return Response(serializer.errors,status=status.HTTP_200_OK)

        serializer = self.serializer_class(code,data=request.data)                                

        if serializer.is_valid(raise_exception=True):
            return Response({'Status':'OK'},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_200_OK)
        
class RecoveryAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RecoverySerializer
    redirect_to = settings.base.LOGIN_REDIRECT_URL

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.post(data)
        #StdUser.send_recovery_password(email)

        if(serializer.is_valid(raise_exception=True)):
            new_data = serializer.data
            return Response(new_data, status=status.HTTP_200_OK)                                
                                 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        

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


class UpdateUserAPIView(GenericAPIView, UpdateModelMixin):
    """
    Update User
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer
    queryset = User.objects.all()

    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        serializer = self.serializer_class(request.user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.partial_update(request, *args, **kwargs) 
            return Response({'Status': 'Update success'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        self.update(request, *args, **kwargs)
        return Response({'Status': 'Update success'}, status=status.HTTP_200_OK)


class DeleteUserAPIView(DestroyAPIView):
    """
    Delete User
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = DeleteUserSerializer

    def post(self, request):

        serializer = self.serializer_class(request.user,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.delete(request)

        return Response({'Status':'OK'},status=status.HTTP_200_OK)
