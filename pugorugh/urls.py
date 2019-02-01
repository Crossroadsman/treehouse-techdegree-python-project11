from django.urls import re_path, include
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from rest_framework import routers
#from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

from .views import UserRegisterView, DogViewSet, UserPrefViewSet

# Routers
# -------
# Do we need to put the router in the root URLs.py if we include
# pugorugh's urls at `r'^'`?
#
# The API has the following format:
# Dog detail GET:
# /api/dog/<pk>/liked/next/
# /api/dog/<pk>/disliked/next/
# /api/dog/<pk>/undecided/next/
#
# UserDog POST/PUT:
# /api/dog/<pk>/liked/
# /api/dog/<pk>/disliked/
# /api/dog/<pk>/undecided/
#
# UserPref POST/PUT (and GET?):
# /api/user/preferences/
router = routers.DefaultRouter()
# router.register(<regex>, <view/viewset>)
router.register(r'dog', DogViewSet)
router.register(r'user', UserPrefViewSet)

# I don't think we need to use format_suffix_patterns if we use
# DefaultRouter, since it provides `.json` suffix URLs OOB.
urlpatterns = [
    # Rest Framework Auth
    #   This route seems to be a clone of the route in the base urls.py
    re_path(r'^api/user/login/$', obtain_auth_token, name="login-user"),
    #   Register user (available as a web view)
    re_path(r'^api/user/$', UserRegisterView.as_view(), name='register-user'),

    # Application
    re_path(r'^$', TemplateView.as_view(template_name='index.html')),
    re_path(r'^favicon\.ico$', RedirectView.as_view(url='/static/icons/favicon.ico', permanent=True)),

    # API
    re_path(r'^api/', include(router.urls)),
]

'''Disable to see if not needed when using DefaultRouter
# Apply Format Suffixes
# https://www.django-rest-framework.org/api-guide/format-suffixes/
urlpatterns = format_suffix_patterns(urlpatterns)
'''