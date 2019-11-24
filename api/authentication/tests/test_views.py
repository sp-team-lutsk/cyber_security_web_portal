import json
import nose.tools as nt

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from authentication.models import StdUser
from authentication.serializers import UserSerializer

from settings.tests import *


""" Tests all UserAPIView methonds """
class TestUsersAPIView(APITestCase):
    
    """ Setup test data """
    @classmethod
    def setUpTestData(cls):
        cls.admin = StdUser.objects.create_user(
                email=TEST_ADMIN_EMAIL,
                password=TEST_PASSWORD,
                user_type=1)
        cls.moderator = StdUser.objects.create_user(
                email=TEST_MODER_EMAIL,
                password=TEST_PASSWORD,
                user_type=2)
        cls.user = StdUser.objects.create_user(
                email=TEST_EMAIL,
                password=TEST_PASSWORD,
                user_type=3)

    """ Test admin request to get users list """
    def test_get_all_users_admin(self):
        url = reverse('obtain_jwt')

        access_admin = self.client.post(
                url, 
                { "email": TEST_ADMIN_EMAIL, "password": TEST_PASSWORD },
                format='json').data['access']


        url = reverse('users_list')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_admin)
        response = self.client.get(url)
    
        users = StdUser.objects.all()
        serializer = UserSerializer(users, many=True)
        
        nt.assert_equal(response.data, serializer.data)
        nt.assert_equal(response.status_code, status.HTTP_200_OK)
        


""" Tests API of all user list """
class TestJWTToken(APITestCase):

    """ Setup test data """
    @classmethod
    def setUpTestData(cls):
        cls.admin = StdUser.objects.create_user(
                email=TEST_ADMIN_EMAIL,
                password=TEST_PASSWORD,
                user_type=1)

    """ Test jwt obtain """
    def test_obtain_refresh_jwt_token(self):
        url = reverse('obtain_jwt')
        
        data = {
            "email": TEST_ADMIN_EMAIL,
            "password": TEST_PASSWORD,
        }

        response = self.client.post(url, data, format='json')

        """ Testing if token in response """
        nt.assert_equal(response.status_code, status.HTTP_200_OK)
        nt.assert_true('access' in response.data)
        nt.assert_true('refresh' in response.data)
        
        access_token = response.data['access']
        refresh_token = response.data['refresh']
        
        data = {
            "refresh": refresh_token
        }

        url = reverse('refresh_jwt')

        response = self.client.post(url, data, format='json')

        """ Testing for new access token getting """
        nt.assert_equal(response.status_code, status.HTTP_200_OK)
        nt.assert_true('access' in response.data)

