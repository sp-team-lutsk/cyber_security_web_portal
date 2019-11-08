from django.conf import settings 
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView

from authentication.permissions import (IsAdminUser, 
                        IsAuthenticated, 
                        IsModeratorUser,
                        IsStaffUser,
                        AllowAny)

from rest_framework.response import Response

from authentication.models import StdUser
from utils.models import Mail
from utils.serializers import (
    SendMailSerializer,
   )

User = get_user_model()

class SendMailAPIView(APIView):
    """
    Send mail from admin to user
    """
    serializer_class = SendMailSerializer
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    
    def post(self, request):
        serializer = SendMailSerializer(data=request.data)
        user = self.queryset.get(email=request.data.get('email'))
        if user is not None:
            if serializer.is_valid(raise_exception=True):
                serializer.send(data=request.data)
                return Response({'Status': 'Mail Send'}, status=status.HTTP_200_OK)

class MailingAPIView(APIView):
    permission_classes = [AllowAny, ]
    queryset = StdUser.objects.filter(news_subscription = True)

    def get(self, request, **extra_kwargs):
        queryset = self.queryset
        for user in queryset.iterator():
            Mail.mailing(data=user)  
        return Response({'Status':'OK'},status=status.HTTP_200_OK)

def Mailing():
    queryset = StdUser.objects.filter(news_subscription = True)
    for user in queryset.iterator():
        News.mailing(data=user)
    return None
