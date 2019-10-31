from django.urls import path
from .views import PostUpd_int, Post_int

urlpatterns = [
    path('upd_int/<int:pk>/', PostUpd_int.as_view(), name=None),
    path('post_int/', Post_int.as_view(), name=None),
 ]
