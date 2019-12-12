from django.urls import path
from ext_news.views import PostUpd, News_Bulk
from utils.views import MailingAPIView

urlpatterns = [
    path('<int:id>/', PostUpd.as_view(), name='upd'),
    path('', News_Bulk.as_view(), name=None),
    path('mailing/', MailingAPIView.as_view(), name='mailing'),
]
