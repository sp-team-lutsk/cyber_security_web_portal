from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import *
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework import generics
from user.serializers import UserSerializer



#create user
class CreateUserAPIView(APIView):
    # Allow any user (authenticed or not) to access this url 
    permission_classes = (AllowAny,)
 
    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

#all users in db (for test)
class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

