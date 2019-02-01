from django.urls import re_path
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

from .views import UserRegisterView


urlpatterns = [
    # Rest Framework Auth
    #   This route seems to be a clone of the route in the base urls.py
    re_path(r'^api/user/login/$', obtain_auth_token, name="login-user"),
    #   Register user (available as a web view)
    re_path(r'^api/user/$', UserRegisterView.as_view(), name='register-user'),

    # Application
    re_path(r'^$', TemplateView.as_view(template_name='index.html')),
    re_path(r'^favicon\.ico$', RedirectView.as_view(url='/static/icons/favicon.ico', permanent=True)),
]

# Apply Format Suffixes
# https://www.django-rest-framework.org/api-guide/format-suffixes/
urlpatterns = format_suffix_patterns(urlpatterns)