from django.urls import re_path, include
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

from . import views

# Routers
# -------
# The required API urls are too different than the router/viewset defaults to
# make that combination convenient.
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
# UserPref POST?/PUT (and GET):
# /api/user/preferences/

urlpatterns = [
    # Rest Framework Auth
    #   This route seems to be a clone of the route in the base urls.py
    re_path(r'^api/user/login/$', obtain_auth_token, name="login-user"),
    #   Register user (available as a web view)
    re_path(r'^api/user/$',
            views.UserRegisterView.as_view(),
            name='register-user'),

    # Application
    re_path(r'^$',
            TemplateView.as_view(template_name='index.html'),
            name='index'),
    re_path(r'^favicon\.ico$',
            RedirectView.as_view(url='/static/icons/favicon.ico',
                                 permanent=True)),

    # API
    re_path(r'^api/dog/(?P<pk>[-\d]+)/(?P<status>\w+)/next/$',
            views.DogRetrieveUpdateAPIView.as_view(),
            name="next-dog"),
    re_path(r'^api/dog/(?P<pk>[-\d]+)/(?P<status>\w+)/$',
            views.DogRetrieveUpdateAPIView.as_view(),
            name="set-status"),
    re_path(r'^api/user/preferences/$',
            views.UserPrefRetrieveAPIView.as_view(),
            name="set-preferences"),

    re_path(r'^api/dog/random/$',
            views.RandomDogRetrieveAPIView.as_view(),
            name="random-dog"),
    re_path(r'^api/dog/needs-love/$',
            views.NeedMoreLoveDogRetrieveAPIView.as_view(),
            name="needs-love-dog"),

    # Additional App Views
    re_path(r'dog/add/$', views.add_dog, name='add_dog'),
    re_path(r'dog/delete/$', views.delete_list, name='delete_list'),
    re_path(r'dog/(?P<pk>[-\d]+)/delete/$',
            views.delete_dog,
            name='delete_dog'),
]

# Apply Format Suffixes
# https://www.django-rest-framework.org/api-guide/format-suffixes/
# (needed because we are not using DefaultRouter)
urlpatterns = format_suffix_patterns(urlpatterns)
