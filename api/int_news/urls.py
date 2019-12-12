from django.urls import path
from .views import PostUpdInt, News_Bulk

urlpatterns = [
    path('<int:id>/', PostUpdInt.as_view(), name='update'),
    path('', News_Bulk.as_view(), name='bulk_update'),
 ]
