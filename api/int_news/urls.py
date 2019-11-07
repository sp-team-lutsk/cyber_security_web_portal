from django.urls import path
from .views import PostUpdInt, PostInt

urlpatterns = [
    path(r'<int:pk>/', PostUpdInt.as_view(), name='update'),
    path(r'', PostInt.as_view(), name='list'),
 ]
