from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import views as auth_views
from .views import (
    UserListAPIView,
    CreateUserAPIView, 
    LoginUserAPIView,
    StudentListAPIView, 
    TeacherListAPIView, 
    UpdateUserAPIView,
    DeleteUserAPIView,)

urlpatterns = [
    
        #user api
    path('register/', CreateUserAPIView.as_view(), name='register'),    # register page
    path('login/', LoginUserAPIView.as_view(), name='login'),           # login page
    path('social/', include('social_django.urls', namespace='social')), # social authentication pages
    path('update/', UpdateUserAPIView.as_view(),name='update'),
    path('delete/', DeleteUserAPIView.as_view(),name='delete'),
        #admin api
    path('user_list/', UserListAPIView.as_view(), name='user_list'), # user list page
    path('student_list/', StudentListAPIView.as_view(), name='slist'),
    path('teacher_list/', TeacherListAPIView.as_view(), name='tlist'),
    
        #garbage
    path('refreshtoken/', TokenRefreshView.as_view(), name='refresh-token'),   # refresh access token
]
