from django.urls import path, include
from importlib import import_module
from allauth.socialaccount import providers

from rest_framework_simplejwt.views import token_obtain_pair,token_refresh
from django.contrib.auth import views as auth_views
from .views import (
    UserAPIView,
    FindUserAPIView,
    CreateUserAPIView,
    StudentListAPIView, 
    TeacherListAPIView,
    SendMailAPIView,
    UpdateUserAPIView,
    DeleteUserAPIView,
    VerifyUserAPIView,
    RecoveryAPIView,
    VerifyPassUserAPIView,
    UserInactiveAPIView)

urlpatterns = [
    
    #user api
    path('users/', CreateUserAPIView.as_view(), name='register'),    # register page
    path('users/', DeleteUserAPIView.as_view(), name='delete'),         # delete user
    path('users/', ListUserAPIView.as_view(), name='users'),            # all activated user list page
    path('users/login/', token_obtain_pair, name='login'),           # login page with obtain token
    path('users/inactive/', UserInactiveAPIView.as_view(), name='account_inactive'),
    path('users/send_mail/', SendMailAPIView.as_view(), name='sendmail'),
    path('users/recover_pass/', RecoveryAPIView.as_view(), name='recover'),
    path('users/token/refresh/', token_refresh, name='refresh'),               # refresh token
    path('users/verify/<str:code>/', VerifyUserAPIView.as_view(), name='verify'),
    path('users/recovery/<str:code>/', VerifyPassUserAPIView.as_view(), name='completerecover'),
    

    path('users/<str:email>/',FindUserAPIView.as_view(), name='user'),   # info about user by email search
    path('users/update/<int:pk>/', UpdateUserAPIView.as_view(), name='update'),

    path('register/', CreateUserAPIView.as_view(), name='socialaccount_signup'),
    
    path('students/', StudentListAPIView.as_view(), name='slist'),  # students list page
    path('teachers/', TeacherListAPIView.as_view(), name='tlist'),  # teachers list page
    
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
