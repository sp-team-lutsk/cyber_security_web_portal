from django.urls import path
from .views import PostUpd, Post, MailingAPIView

urlpatterns = [
    path('upd/<int:pk>/', PostUpd.as_view(), name='upd'),
    path('post/', Post.as_view(), name=None),
    path('mailing/', MailingAPIView.as_view(), name='mailing'),
]
