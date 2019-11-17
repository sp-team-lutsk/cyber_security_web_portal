from django.urls import path
from .views import PostUpdInt, PostInt

urlpatterns = [
    path('<int:id>/', PostUpdInt.as_view(), name='update'),
    path('/', PostInt.as_view(), name='list'),
 ]
