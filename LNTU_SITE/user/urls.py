from django.urls import path
from .views import CreateUserAPIView,UserListAPIView,home
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import include

urlpatterns = [
    path('login/', CreateUserAPIView.as_view()),    #login page
    path('signup/',include('allauth.urls')),
    path('token',TokenObtainPairView.as_view()),   #generate JWT token
    path('refreshtoken',TokenRefreshView.as_view()),   #refresh access token
    path ('list',UserListAPIView.as_view()),
    ]

