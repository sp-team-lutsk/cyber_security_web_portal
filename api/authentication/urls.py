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
    path('social/', include('social_django.urls', namespace='social')), # authentication and login pages for social networks ('facebook','google-oauth2')
    path('update/', UpdateUserAPIView.as_view(),name='update'),         # update user information
    path('delete/', DeleteUserAPIView.as_view(),name='delete'),         # delete user
        #admin api
    path('users/', UserListAPIView.as_view(), name='users'),            # all activated user list page
    path('users/<str:email>/',FindUserAPIView.as_view(),name='user'),   # info about user by email search
    path('student_list/', StudentListAPIView.as_view(), name='slist'),  # students list page
    path('teacher_list/', TeacherListAPIView.as_view(), name='tlist'),  # teachers list page
    
        #garbage
    path('refreshtoken/', TokenRefreshView.as_view(), name='refresh-token'),   # refresh access token
]
