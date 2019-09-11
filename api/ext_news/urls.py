from django.urls import path
from .views import Post, News_Details



urlpatterns = [
    path('', Post.as_view()),
    path('<int:pk>/', News_Details.as_view()),
]