from django.conf import settings 
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView

from authentication.permissions import (IsAdminUser, 
                        IsAuthenticated, 
                        IsModeratorUser,
                        IsStaffUser,
                        AllowAny)

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
from authentication.serializers import (
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
    SetModeratorSerializer,
    )

from authentication.models import StdUser, Student, Teacher
from utils.decorators import permission, permissions, object_permission

import authentication.logger
User = get_user_model()

class UserAPIView(ListAPIView,ListModelMixin,DestroyAPIView):
    lookup_field = 'id'
    serializer_class = UserSerializer
    permission_classes = [AllowAny,]
    queryset = User.objects.all()
    
    @permission("IsStaffUser")
    def get(self,request,*args,**kwargs):
        number = args[0]
        queryset = User.objects.filter(id=number.get('id'))
        if queryset:
            serializer = self.get_serializer(queryset, many =True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'Status':'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @permission("IsStaffUser")
    def post(self,request,*args,**kwargs):
        return Response({'Status':'Method not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    @permissions(["IsModeratorUser","IsUser"])
    def put(self, request, *args, **kwargs):
        self.serializer_class = UpdateUserSerializer
        number = args[0]
        queryset = User.objects.filter(id=number.get('id'))
        serializer = UpdateUserSerializer(queryset[0],  data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response({'Status': 'Update success'}, status=status.HTTP_200_OK)
        
    @permissions(["IsModeratorUser","IsUser"]) 
    def delete(self,request,*args,**kwargs):
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
    
    @permission("IsModeratorUser")
    def put(self,request,*args,**kwargs):
        self.serializer_class = UpdateUserSerializer
        queryset = User.objects.all()
        
        for user in list(queryset):
            serializer = BulkUpdateUserSerializer(user,  data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        
            return Response(serializer.errors)
    
    @permission("IsModeratorUser")
    def delete(self,request):
        self.serializer_class=DeleteAllSerializer
        q = list(self.queryset)
        for u in q:
            serializer = self.serializer_class(request.user, data=request.data)
            serializer.delete(request)
        return Response({'Status':'OK'},status=status.HTTP_200_OK)

class TeacherAPIView(ListAPIView,ListModelMixin,DestroyAPIView):
    lookup_field = 'id'
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    @permissions(["IsStaffUser","IsUser"]) 
    def get(self,request,*args,**kwargs):
        number = kwargs.get('id')
        queryset = User.objects.filter(id=number,is_teacher=True)
        if queryset:
            serializer = self.get_serializer(queryset, many =True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'Status':'User not found'}, status=status.HTTP_404_NOT_FOUND)
     
    @permissions(["IsModeratorUser","IsUser"]) 
    def post(self,request,*args,**kwargs):
        return Response({'Status':'Method not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @permissions(["IsModeratorUser","IsUser"]) 
    def put(self, request, *args, **kwargs):
        self.serializer_class = UpdateTeacherSerializer
        number = kwargs.get('id')
        queryset = Teacher.objects.filter(user=number)
        serializer = UpdateTeacherSerializer(queryset[0],  data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Status': 'Update success'}, status=status.HTTP_200_OK)
    
    @permissions(["IsModeratorUser","IsUser"]) 
    def delete(self,request,*args,**kwargs):
        number = kwargs.get('id')
        queryset = User.objects.filter(id=number,is_teacher=True)
        user = queryset[0]
        t = Teacher.objects.filter(id=user.teacher.id)
        t.delete()
        user.is_teacher = False
        user.save()
        return Response({'Status':'OK'},status=status.HTTP_200_OK)

class TeachersAPIView(ListAPIView):
    """
    All teachers in db (for test)
    """
    permission_classes = [AllowAny,]
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def post(self, request):
        self.serializer_class = CreateTeacherSerializer    
        serializer = self.serializer_class(data=request.data)
       
        serializer.is_valid(raise_exception=True)
        user_saved = serializer.save()
        
        return Response(
                data={"success": "User '{}' created successfully".format(str(user_saved))},
                status=status.HTTP_201_CREATED)
    
    @permission("IsModeratorUser")
    def put(self,request,*args,**kwargs):
        self.serializer_class = BulkUpdateTeacherSerializer
        queryset = Teacher.objects.all()
        
        for user in list(queryset):
            serializer = UpdateTeacherSerializer(user,  data=request.data)
            if serializer.is_valid():
                serializer.save()
        return Response(data={ "200" : "OK"},status=status.HTTP_200_OK)

    @permission("IsModeratorUser")
    def delete(self,request):
        q = User.objects.filter(is_teacher=True)
        for u in q:
            u.is_teacher = False
            t = Teacher.objects.filter(id=u.teacher.id)
            t.delete()
            u.save()
        return Response({'Status':'OK'},status=status.HTTP_200_OK)


class StudentAPIView(ListAPIView,ListModelMixin,DestroyAPIView):
    lookup_field = 'id'
    serializer_class = UserSerializer
    queryset = Student.objects.all()
    
    @permissions(["IsStaffUser","IsUser"])
    def get(self,request,*args,**kwargs):
        number = kwargs.get('id')
        queryset = User.objects.filter(id=number,is_student=True)
        if queryset:
            serializer = self.get_serializer(queryset, many =True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'Status':'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @permissions(["IsModeratorUser","IsUser"])
    def post(self,request,*args,**kwargs):
        return Response({'Status':'Method not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @permissions(["IsModeratorUser","IsUser"])
    def put(self, request, *args, **kwargs):
        self.serializer_class = UpdateStudentSerializer
        number = kwargs.get('id')
        queryset = Student.objects.filter(user=number)
        serializer = UpdateStudentSerializer(queryset[0],  data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Status': 'Update success'}, status=status.HTTP_200_OK)

    @permissions(["IsModeratorUser","IsUser"])
    def delete(self,request,*args,**kwargs):
        #self.serializer_class = DeleteUserSerializer
        number = kwargs.get('id')
        queryset = User.objects.filter(id=number,is_student=True)
        user = queryset[0]
        
        s = Student.objects.filter(id=user.student.id)
        s.delete()

        user.is_student = False
        user.save()
        return Response({'Status':'OK'},status=status.HTTP_200_OK)

class StudentsAPIView(ListAPIView):
    """
    All teachers in db (for test)
    """
    permission_classes = [AllowAny,]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def post(self, request):
        self.serializer_class = CreateStudentSerializer    
        serializer = self.serializer_class(data=request.data)
       
        serializer.is_valid(raise_exception=True)
        user_saved = serializer.save()
        
        return Response(
                data={"success": "User '{}' created successfully".format(str(user_saved))},
                status=status.HTTP_201_CREATED)

    @permission("IsModeratorUser")
    def put(self,request,*args,**kwargs):
        self.serializer_class = BulkUpdateStudentSerializer
        queryset = Student.objects.all()
        
        for user in list(queryset):
            serializer = BulkUpdateStudentSerializer(user,  data=request.data)
            if serializer.is_valid():
                serializer.save()
        return Response(data={ "200" : "OK"},status=status.HTTP_200_OK)

    @permission("IsModeratorUser")
    def delete(self,request):
        q = User.objects.filter(is_student=True)
        for u in q:
            u.is_student = False
            
            s = Student.objects.filter(id=u.student.id)
            s.delete()
            
            u.save()
        return Response({'Status':'OK'},status=status.HTTP_200_OK)

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
            return Response({'Status':'OK'}, status=status.HTTP_200_OK)

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
                return Response({'Status':'OK'}, status=status.HTTP_200_OK)
        
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
        user = User.objects.get(id=request.data.get('id'))
        user.is_moderator = True
        user.save()
        return Response(data={"success": "User with id {} moderator now".format(str(request.data.get('id')))},
                    status=status.HTTP_200_OK)

class AdminUserAPIView(APIView):
    permission_classes = [AllowAny, ]
    queryset = User.objects.none()
    serializer_class = CreateUserSerializer 

    @permission("IsAdminUser")
    def post(self, request,*args,**kwargs):
        serializer = self.serializer_class(data=request.data)
        user = StdUser()
        user.email = request.data.get('email')
        user.is_active = True
        password = request.data.get('password') 
        user.set_password(password)
        user.save()
        serializer.is_valid(raise_exception=True)
        
        return Response(
                data={"success": "User '{}' created successfully".format(str(request.data.get('email')))},
                status=status.HTTP_201_CREATED)
   
    @permission("IsAdminUser")
    def delete(self,request,*args,**kwargs):
        self.serializer_class = SetModeratorSerializer
        serializer = SetModeratorSerializer(data=request.data)
        queryset = User.objects.get(id=request.data.get('id'))
        user = queryset
        user.is_active = False
        user.save()
        return Response({'Status':'OK'},status=status.HTTP_200_OK)

class BanUserAPIView(APIView):
    permission_classes = [AllowAny, ]
    queryset = User.objects.none()
    serializer_class = SetModeratorSerializer

    @permission("IsModeratorUser")
    def post(self,request,*args,**kwargs): 
        serializer = self.serializer_class(data=request.data)
        queryset = User.objects.get(id=request.data.get('id'))
        user = queryset
        user.is_active = False
        user.save()
        return Response({'Status':'OK'},status=status.HTTP_200_OK)



