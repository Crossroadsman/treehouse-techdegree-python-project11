from django.contrib.auth import get_user_model
from django.shortcuts import render

from rest_framework import permissions
from rest_framework.generics import CreateAPIView

from . import serializers


class UserRegisterView(CreateAPIView):
    
    # Override the restrictive permissions specified in settings.py
    permission_classes = (permissions.AllowAny,)
    
    model = get_user_model()
    serializer_class = serializers.UserSerializer
