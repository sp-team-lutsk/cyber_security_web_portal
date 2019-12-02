from django.urls import path
from .views import PostUpdInt, PostInt, News_Bulk

urlpatterns = [
    path('int_news/<int:pk>/', PostUpdInt.as_view(), name='update'),
    path('', PostInt.as_view(), name='list'),
    path('int_news/', News_Bulk.as_view(), name='bulk_update'),
 ]
