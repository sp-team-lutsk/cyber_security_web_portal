import json
import nose.tools as nt

from nose.tools import nottest
from nose.tools.nontrivial import raises

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from authentication.models import StdUser
from authentication.serializers import (
        UserSerializer,
        UpdateUserSerializer,
        BulkUpdateUserSerializer,)

from settings.tests import *


""" Tests admin access to api methonds """
class TestAdminPermsAPIViews(APITestCase):
    
    """ Setup test data """
    @classmethod
    def setUpTestData(cls):
        cls.user = StdUser.objects.create_user(
                email=TEST_ADMIN_EMAIL,
                password=TEST_PASSWORD,
                user_type=1)

    def setUp(self):
        self.t_user = StdUser.objects.create_user(
                email=TEST_EMAIL2,
                password=TEST_PASSWORD)
        self.get_token()

    """ This func helps to get jwt access token many times """
    @nottest
    def get_token(self):
        url = reverse('obtain_jwt')

        access_token = self.client.post(
                url,
                { "email": self.user.email, "password": TEST_PASSWORD },
                format='json').data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

    """ Test request to get users list """
    def test_get_all_users(self):
        url = reverse('users_list')
        
        response = self.client.get(url)
    
        users = StdUser.objects.all()
        serializer = UserSerializer(users, many=True)
        
        nt.assert_equal(response.data, serializer.data)
        nt.assert_equal(response.status_code, status.HTTP_200_OK)

    """ Test of creating user """
    def test_post_create_user(self):
        url = reverse('users_list')
        
        data = {
                "email": TEST_EMAIL3,
                "password": TEST_PASSWORD,
        }

        response = self.client.post(url, data, format='json') 
        user = StdUser.objects.get(email=TEST_EMAIL3)

        nt.assert_equal(response.status_code, status.HTTP_201_CREATED)
        nt.assert_not_equal(user, None)

    """ Test get one User """
    def test_get_one_user(self):
        url = reverse('user', args=[self.t_user.id,])
        
        response = self.client.get(url)
        
        serializer = UserSerializer(self.t_user)

        nt.assert_equal(response.data, serializer.data)
        nt.assert_equal(response.status_code, status.HTTP_200_OK)
        
    """ Test get one not existing User """
    def test_get_one_which_not_exist(self):
        url = reverse('user', args=[BAD_USER_ID,])
        
        response = self.client.get(url)
        
        nt.assert_equal(response.status_code, status.HTTP_404_NOT_FOUND)

    """ Test post one user """
    def test_post_one_user(self):
        url = reverse('user', args=[self.t_user.id],)

        response = self.client.post(url)

        nt.assert_equal(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


""" Test moderator access to api """
class TestModerPermsAPIViews(TestAdminPermsAPIViews):
    
    """ Setup test data """
    @classmethod
    def setUpTestData(cls):
        cls.user = StdUser.objects.create_user(
                email=TEST_MODER_EMAIL,
                password=TEST_PASSWORD,
                user_type=2)

    """ Tests users bulk update """
    def test_put_bulk_update_users(self):
        queryset = StdUser.objects.all()
        serializer = BulkUpdateUserSerializer(queryset, many=True)

        url = reverse('users_list')

        data = {
                "first_name": TEST_NAME,
                "last_name": TEST_SURNAME
        }
        
        response = self.client.put(url, data, format='json')

        nt.assert_equal(response.data, serializer.data)
        nt.assert_equal(response.status_code, status.HTTP_200_OK)

    """ Tests users bulk delete """
    def test_delete_bulk_users(self):
        url = reverse('users_list')

        response = self.client.delete(url)

        nt.assert_equal(response.status_code, status.HTTP_200_OK)

    """ Tests put update for one user """
    def test_put_one_user(self):
        url = reverse('user', args=[self.t_user.id])

        data = {
            "email": TEST_EMAIL3,
            "fist_name": TEST_NAME,
            "last_name": TEST_SURNAME,
            "patronymic": TEST_PATRONIM,
            "bio": TEST_BIO,
            "news_subscription": "true"
        }

        response = self.client.put(url, data, format='json')
        
        nt.assert_equal(response.status_code, status.HTTP_200_OK)


""" Tests active user access to api methonds """
class TestActiveUserPermsAPIViews(TestAdminPermsAPIViews):
    
    """ Setup test data """
    @classmethod
    def setUpTestData(cls):
        cls.user = StdUser.objects.create_user(
                email=TEST_EMAIL,
                password=TEST_PASSWORD,
                user_type=3)
        cls.user.is_active = True
        cls.user.save()
  
    def setUp(self):
        self.t_user = StdUser.objects.create_user(
                email=TEST_EMAIL2,
                password=TEST_PASSWORD)
        self.get_token()

    """ Standart user does not have such perms """
    def test_get_all_users(self):
        url = reverse('users_list')
        
        response = self.client.get(url)
    
        users = StdUser.objects.all()
        serializer = UserSerializer(users, many=True)
        
        nt.assert_equal(response.data, NO_SUCH_PERM)

    """ Standart user does not have such perms """
    def test_get_one_user(self):
        url = reverse('user', args=[self.t_user.id,])
        
        response = self.client.get(url)
        
        serializer = UserSerializer(self.t_user)

        nt.assert_equal(response.data, NO_SUCH_PERM)
    
    """ Standart user does not have such perms """
    def test_get_one_which_not_exist(self):
        url = reverse('user', args=[BAD_USER_ID,])
        
        response = self.client.get(url)

        nt.assert_equal(response.data, NO_SUCH_PERM)


""" Tests inactive users access to api methods """
class TestInactiveUserPermsAPIViews(TestAdminPermsAPIViews):
    
    """ Setup test data """
    @classmethod
    def setUpTestData(cls):
        cls.user = StdUser.objects.create_user(
                email=TEST_EMAIL,
                password=TEST_PASSWORD,)
    
    """ Turn off setup from parent """
    def setUp(self):
        self.t_user = StdUser.objects.create_user(
                email=TEST_EMAIL2,
                password=TEST_PASSWORD)

    """ Standart user does not have such perms, so it will raise KeyError """
    @raises(KeyError)
    def test_get_all_users(self):
        self.get_token()
        super().test_get_all_users()
    
    """ StdUser must be active """
    @raises(KeyError)
    def test_post_create_user(self):
        self.get_token()
        super().test_post_create_user()

    """ Must be active """
    @raises(KeyError)
    def test_get_one_user(self):
        self.get_token()
        super.test_get_one_user()

    """ Must be active """
    @raises(KeyError)
    def test_get_one_which_not_exist(self):
        self.get_token()
        super.test_get_one_which_not_exist()


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

