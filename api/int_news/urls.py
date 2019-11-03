from django.urls import path
from .views import PostUpdInt, PostInt

urlpatterns = [
    path('upd_int/<int:pk>/', PostUpdInt.as_view(), name=None),
    path('post_int/', PostInt.as_view(), name=None),
 ]
