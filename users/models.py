# Based on the guide here:
# https://wsvincent.com/django-custom-user-model-tutorial/
#
# This creates a custom user that is almost identical to the default user
# except it uses email as the string representation.
#
# The sequence is:
#
# (note, we can run the Django server before this process is complete, we just
# mustn't create or run migrations)
#
# 1. Create the Django Project
# 2. Create a `users` app
# 3. Decide whether to subclass `AbstractUser` or `AbstractBaseUser`
#    (this guide uses the former, which is much, much easier)
# 4. Create initial custom user model:
#    4.1 update `settings.py` (see `settings.py` for more details)
#    4.2 create a replacement `User` model (see below)
#    4.3 create new user forms (see `forms.py`)
#    4.4 customise Django admin (see `admin.py`)
# 5. Run `makemigrations` for `users`
# 6. Run `migrate` for `users`
# 7. Create a superuser
#
# Note, this is an API-only project so no templates/views are created.
#
#
# Referencing the Custom User Model
# ---------------------------------
# See generally: https://docs.djangoproject.com/en/2.1/topics/auth/customizing/#referencing-the-user-model
#
# Either:
# - `get_user_model()` (from `django.contrib.auth`); or
# - `settings.AUTH_USER_MODEL` (`from django.conf import settings`).
#
# Use the latter when:
# - defining FK/MTM relations in models;
# - connecting to signals sent by the user model
#
# Apparently (see https://wsvincent.com/django-referencing-the-user-model/),
# since v1.11, we can now use `get_user_model` anywhere we once needed to use
# AUTH_USER_MODEL (but note that the statements above re using AUTH_USER_MODEL
# come directly from the Django 2.2 docs).
# `get_user_model` is preferable where available because apparently, it will 
# work whether the installed user model is built-in or custom. 
# `AUTH_USER_MODEL` only works for custom models.
from django.contrib.auth.models import AbstractUser
from django.db import models


class PugUghUser(AbstractUser):
    pass

    '''
    def __str__(self):
        return self.email
    '''
