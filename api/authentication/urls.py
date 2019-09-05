from django.urls import path, include
from importlib import import_module
from allauth.socialaccount import providers

from rest_framework_simplejwt.views import token_obtain_pair,token_refresh
from django.contrib.auth import views as auth_views
from .views import (
    FindUserAPIView,
    UserListAPIView,
    CreateUserAPIView, 
    LoginUserAPIView,
    StudentListAPIView, 
    TeacherListAPIView, 
    UpdateUserAPIView,
    DeleteUserAPIView,
    VerifyUserAPIView,
    RecoveryAPIView,)

urlpatterns = [
    
    #user api
    path('register/', CreateUserAPIView.as_view(), name='register'),    # register page
    path('login/', LoginUserAPIView.as_view(), name='login'),           # login page with obtain token
    path('delete/', DeleteUserAPIView.as_view(),name='delete'),         # delete user
    path('verify/<str:code>/', VerifyUserAPIView.as_view(),name='verify'),
    path('recover_pass/', RecoveryAPIView.as_view(),name='recover'),
    #admin api
    path('users/', UserListAPIView.as_view(), name='users'),            # all activated user list page
    path('users/<str:email>/',FindUserAPIView.as_view(), name='user'),   # info about user by email search
    path('update/<int:pk>/', UpdateUserAPIView.as_view(), name='update'),
    path('student_list/', StudentListAPIView.as_view(), name='slist'),  # students list page
    path('teacher_list/', TeacherListAPIView.as_view(), name='tlist'),  # teachers list page
   
    path('token/obtain/', token_obtain_pair, name='obtain'),            # obtain token 
    path('token/refresh/',token_refresh, name='refresh'),               # refresh token
]

# This is for social auth 
provider_urlpatterns = []
for provider in providers.registry.get_list():
    try:
        prov_mod = import_module(provider.get_package() + '.urls')
    except ImportError:
        continue
    prov_urlpatterns = getattr(prov_mod, 'urlpatterns', None)
    if prov_urlpatterns:
        provider_urlpatterns += prov_urlpatterns
urlpatterns += provider_urlpatterns
