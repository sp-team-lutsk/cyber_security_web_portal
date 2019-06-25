from django.urls import path 
from .views import CreateUserAPIView,UserListAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', CreateUserAPIView.as_view(),name = 'field.html'),    #login page    
    path('token',TokenObtainPairView.as_view()),   #generate JWT token
    path('refreshtoken',TokenRefreshView.as_view()),   #refresh access token
    path ('list',UserListAPIView.as_view()),
    ]

