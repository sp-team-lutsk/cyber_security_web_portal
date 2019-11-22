import nose.tools as nt

from django.test import TestCase

from int_news.models import NewsInt
from authentication.models import StdUser

from settings.tests import *

class TestIntNews(TestCase):

    ''' Setup test data '''
    @classmethod
    def setUpTestData(cls):
        cls.user = StdUser.objects.create_user(
                email=TEST_EMAIL, 
                password=TEST_PASSWORD,
                user_type=3)
        cls.int_news = NewsInt.objects.create(
                title=TEST_TITLE,
                author=cls.user)
    
    ''' Test publishing time '''
    def test_publish(self):
        time = self.int_news.publish()
        nt.assert_equal(time, self.int_news.published_date)
