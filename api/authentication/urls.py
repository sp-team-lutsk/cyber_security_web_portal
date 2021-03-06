from django.urls import path
from importlib import import_module
from allauth.socialaccount import providers

from rest_framework_simplejwt.views import token_obtain_pair, token_refresh
from authentication.views import (
        UserAPIView,
    UsersAPIView,
    VerifyPassUserAPIView,
    UserInactiveAPIView,
    VerifyUserAPIView,
    RecoveryAPIView,
    TeachersAPIView,
    TeacherAPIView,
    StudentAPIView,
    StudentsAPIView,
    SetModeratorAPIView,
    AdminUserAPIView,
    BanUserAPIView,
    NewsSubscriptionAPIView,
   )
from ext_news.views import ModeratorCheckNewsAPIView
from utils.views import SendMailAPIView, ModeratorMailAPIView

urlpatterns = [
    
    # user api
    path('users/', UsersAPIView.as_view(), name='users_list'),   
    path('users/<int:id>/', UserAPIView.as_view(), name='user'),
    path('users/token_obtain/', token_obtain_pair, name='obtain_jwt'),    
    path('users/inactive/', UserInactiveAPIView.as_view(), name='account_inactive'),
    path('users/recover_pass/', RecoveryAPIView.as_view(), name='recover'),
    path('users/token_refresh/', token_refresh, name='refresh_jwt'),
    path('users/verify/<str:code>/', VerifyUserAPIView.as_view(), name='verify'),
    path('users/recovery/<str:code>/', VerifyPassUserAPIView.as_view(), name='completerecover'),
    path('users/send_mail/', SendMailAPIView.as_view(), name='send_mail'),
    #mailing api
    path('mailing/subscribe/', NewsSubscriptionAPIView.as_view(), name='set_subscribe'),
    path('mailing/unsubscribe/', NewsSubscriptionAPIView.as_view(), name='unset_subscribe'),
    # teacher api
    path('teachers/', TeachersAPIView.as_view(), name='teahers'),
    path('teachers/<int:id>/', TeacherAPIView.as_view(), name='teacher'),
    # students api
    path('students/', StudentsAPIView.as_view(), name='students'),
    path('students/<int:id>/', StudentAPIView.as_view(), name='student'),
    # moderator api
    path('moderator/ban_user/', BanUserAPIView.as_view(), name='ban_user'),
    path('moderator/mass_mail/', ModeratorMailAPIView.as_view(), name='mass_mail'),
    path('moderator/check/', ModeratorCheckNewsAPIView.as_view(), name='set_news'),
    path('moderator/uncheck/',ModeratorCheckNewsAPIView.as_view(), name='unset_news'),
    # admin api
    path('admin/set_moder/', SetModeratorAPIView.as_view(), name='set_moder'),
    path('admin/user/', AdminUserAPIView.as_view(), name='admin_user'),
]

# This is for social auth 
provider_urlpatterns = []
for provider in providers.registry.get_list():
    try:
        prov_mod = import_module(provider.get_package() + '.urls')
    except ImportError:
        continue
    prov_urlpatterns = getattr(prov_mod, 'urlpatterns', None)
    if prov_urlpatterns:
        provider_urlpatterns += prov_urlpatterns
urlpatterns += provider_urlpatterns
