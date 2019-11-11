from django.urls import path
from ext_news.views import PostUpd, Post 
from utils.views import MailingAPIView

urlpatterns = [
    path('<int:pk>/', PostUpd.as_view(), name='upd'),
    path('/', Post.as_view(), name=None),
    path('mailing/', MailingAPIView.as_view(), name='mailing'),
]
