from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import views as auth_views
from .views import (
    FindUserAPIView,
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
    path('info/',FindUserAPIView.as_view(),name='info'),
        #admin api
        path('users/', UserListAPIView.as_view(), name='users'), # user list page
    path('users/<str:email>/',FindUserAPIView.as_view(),name='user'),
    path('student_list/', StudentListAPIView.as_view(), name='slist'),
    path('teacher_list/', TeacherListAPIView.as_view(), name='tlist'),
    
        #garbage
    path('refreshtoken/', TokenRefreshView.as_view(), name='refresh-token'),   # refresh access token
]
