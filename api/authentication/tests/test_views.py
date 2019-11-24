import json
import nose.tools as nt

from nose.tools.nontrivial import raises

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from authentication.models import StdUser
from authentication.serializers import UserSerializer

from settings.tests import *


""" Tests user access to api methonds """
class TestAdminPermsAPIViews(APITestCase):
    
    """ Setup test data """
    @classmethod
    def setUpTestData(cls):
        cls.user = StdUser.objects.create_user(
                email=TEST_ADMIN_EMAIL,
                password=TEST_PASSWORD,
                user_type=1)
    
    """ Test request to get users list """
    def test_get_all_users(self):
        url = reverse('obtain_jwt')

        access_token = self.client.post(
                url, 
                { "email": self.user.email, "password": TEST_PASSWORD },
                format='json').data['access']


        url = reverse('users_list')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        response = self.client.get(url)
    
        users = StdUser.objects.all()
        serializer = UserSerializer(users, many=True)
        
        nt.assert_equal(response.data, serializer.data)
        nt.assert_equal(response.status_code, status.HTTP_200_OK)


""" Tests admin access to api methonds """
class TestUserPermsAPIViews(TestAdminPermsAPIViews):
    
    """ Setup test data """
    @classmethod
    def setUpTestData(cls):
        cls.user = StdUser.objects.create_user(
                email=TEST_EMAIL,
                password=TEST_PASSWORD,
                user_type=3)
    
    """ Standart user does not have such perms, so it will raise KeyError """
    @raises(KeyError)
    def test_get_all_users(self):
        super().test_get_all_users()


""" Test moderator access to api """
class TestModerPermsAPIViews(TestAdminPermsAPIViews):
    
    """ Setup test data """
    @classmethod
    def setUpTestData(cls):
        cls.user = StdUser.objects.create_user(
                email=TEST_MODER_EMAIL,
                password=TEST_PASSWORD,
                user_type=2)


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

