from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    UserListAPIView,
    CreateUserAPIView, 
    LoginUserAPIView,
    StudentListAPIView, 
    TeacherListAPIView, 
    FacebookLogin
)

urlpatterns = [
    path('user_list/', UserListAPIView.as_view(), name='user_list'), # user list page
    path('register/', CreateUserAPIView.as_view(), name='register'), # register page
    path('login/', LoginUserAPIView.as_view(), name='login'),        # login page


    path('token/', TokenObtainPairView.as_view(), name='token'),     # generate JWT token
    path('refreshtoken/', TokenRefreshView.as_view(), name='refresh-token'),   # refresh access token
    
    
    path('student_list/', StudentListAPIView.as_view(), name='slist'),
    path('teacher_list/', TeacherListAPIView.as_view(), name='tlist'),
    path('authentication/', FacebookLogin.as_view(), name='fb_login'),
]
