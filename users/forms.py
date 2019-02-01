# Details of 4.3 from Custom User Model Implementation
# (see users.models for full outline)
#
# We're mostly just subclassing existing forms
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import PugUghUser


class PugUghUserCreationForm(UserCreationForm):

    class Meta:
        model = PugUghUser
        fields = ('username', 'email',)


class PugUghUserChangeForm(UserChangeForm):

    class Meta:
        model = PugUghUser
        fields = ('username', 'email',)
