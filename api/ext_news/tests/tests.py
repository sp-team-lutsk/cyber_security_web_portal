import nose.tools as nt

from django.test import TestCase, Client
from django.urls import reverse

import ext_news.models as models
import authentication.models as a_models

client = Client()

# Create your tests here.
class TestNews(TestCase):

    @classmethod
    def setUpTestData(self):
        admin = a_models.StdUser.objects.create_superuser(
                email='admin@example.cwv', 
                password='Admin123!')
        self.news = models.News.objects.create(
            title="TestTitle")
        
    def test_str(self):
        nt.assert_equal("TestTitle", str(self.news))

    def test_news_upd(self):
        client.login(email='admin@example.cwv', password='Admin123!')
        response = client.put(reverse('upd', kwargs={"pk": self.news.pk}), {"title": "Fuck"}, content_type='application/json')
        nt.assert_equal(response.data.get('title'), 'Fuck')

        response = client.get(reverse('upd', kwargs={'pk': self.news.pk}))
        nt.assert_equal(response.data.get('title'), 'Fuck')

        response = client.delete(reverse('upd', kwargs={'pk': self.news.pk}))
        nt.assert_equal(response.data, None)
