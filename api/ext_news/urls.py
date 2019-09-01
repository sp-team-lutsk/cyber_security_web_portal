from django.urls import path
from .views import NewsAPIView

urlpatterns = [
  path('list/', NewsAPIView.as_view()),

]