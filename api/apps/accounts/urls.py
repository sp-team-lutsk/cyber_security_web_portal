from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import CreateUserAPIView, UserListAPIView, StudentListAPIView, TeacherListAPIView


urlpatterns = [
    path('login/', CreateUserAPIView.as_view(), name='login'),    # login page
    
    path('token/', TokenObtainPairView.as_view(), name='token'),   # generate JWT token
    path('refreshtoken/', TokenRefreshView.as_view(), name='refresh-token'),   # refresh access token
    path('user_list/', UserListAPIView.as_view(), name='list'),
    path('student_list/', StudentListAPIView.as_view(), name='slist'),
    path('teacher_list/', TeacherListAPIView.as_view(), name='tlist'),

]
