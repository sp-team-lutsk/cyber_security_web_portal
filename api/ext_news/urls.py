from django.urls import path
from .views import NewsAPIView, SingleNewsView

urlpatterns = [
  path('list/', NewsAPIView.as_view()),
  path('ext/<int:pk>', SingleNewsView.as_view()),

]