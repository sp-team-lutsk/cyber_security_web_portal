import json
import nose.tools as nt

from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from authentication.models import StdUser
from authentication.serializers import UserSerializer

from settings.tests import *


""" Tests API of all user list """
class TestGetAllUsers(APITestCase):

    """ Setup database """
    def setUp(self):
        StdUser.objects.create_user(
                email=TEST_EMAIL, 
                password=TEST_PASSWORD,)

    """ Get all users """
    def test_get_all_users(self): 
        response = self.client.get(reverse('users'), format='json')
        users = StdUser.objects.all()
        serializer = UserSerializer(users, many=True)
       
        nt.assert_equal(response.status_code, status.HTTP_200_OK)
        nt.assert_equal(response.data, serializer.data)
