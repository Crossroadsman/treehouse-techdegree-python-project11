from django.contrib import admin
from django.urls import path, re_path, include

from rest_framework.authtoken import views


# URL Patterns
# ------------
urlpatterns = [
    # Django
    path('admin/', admin.site.urls),
    
    # Rest Framework
    #   Browsable API - Login/Logout views
    #   `api-auth/` itself is not browsable, but this provides `.../login/`
    #   and `.../logout/` views that are browsable directly and work with
    #   the browsable API.
    re_path(r'^api-auth/', include('rest_framework.urls')),
    #   Built-in view for getting a token from a username/password
    #   (will return a JSON response when a valid username/password are POSTed)
    re_path(r'^api-token-auth/', views.obtain_auth_token),

    # Pug Or Ugh
    re_path(r'^', include('pugorugh.urls')),    
]
