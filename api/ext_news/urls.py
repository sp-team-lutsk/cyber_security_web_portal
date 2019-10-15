from django.urls import path
from .views import PostUpd, Post

urlpatterns = [
    path('upd/<int:pk>/', PostUpd.as_view(), name='upd'),
    path('post/', Post.as_view(), name=None),
]
