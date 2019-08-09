from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import CreateUserAPIView, UserListAPIView


urlpatterns = [
    path('login/', CreateUserAPIView.as_view(), name='login'),    # login page
    path('token/', TokenObtainPairView.as_view(), name='token'),   # generate JWT token
    path('refreshtoken/', TokenRefreshView.as_view(), name='refresh-token'),   # refresh access token
    path('list/', UserListAPIView.as_view(), name='list'),

]

