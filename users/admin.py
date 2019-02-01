# Details of 4.4 from Custom User Model Implementation
# (see users.models for full outline)
#
# We need to do this because Admin is highly coupled to the default User model
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import PugUghUserChangeForm, PugUghUserCreationForm
from .models import PugUghUser


class PugUghUserAdmin(UserAdmin):
    add_form = PugUghUserCreationForm
    form = PugUghUserChangeForm
    model = PugUghUser
    list_display = ['username', 'email', 'first_name', 'last_name',]


admin.site.register(PugUghUser, PugUghUserAdmin)
