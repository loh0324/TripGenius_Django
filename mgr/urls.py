from django.urls import path

from . import sign_in_out


urlpatterns = [
    path('signin', sign_in_out.signin),
    path('signout', sign_in_out.signout),
    path('register', sign_in_out.register),
]
