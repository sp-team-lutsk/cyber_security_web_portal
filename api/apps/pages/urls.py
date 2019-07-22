from django.urls import path
from apps.pages.views import HomePageView


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
]