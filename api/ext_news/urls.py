from django.urls import path, include
from .views import Post
from rest_framework import routers

router = routers.DefaultRouter()
router.register('post', Post)

urlpatterns = [
    path ('',include(router.urls))
]