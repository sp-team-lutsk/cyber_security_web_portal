import nose.tools as nt

from django.test import TestCase
import ext_news.models as models

# Create your tests here.
class TestNews(TestCase):

    @classmethod
    def setUpTestData(self):
        self.news = models.News.objects.create(
            title="TestTitle")
        
    def test_str(self):
        nt.assert_equal("TestTitle", str(self.news))
