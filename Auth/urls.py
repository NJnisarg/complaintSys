from django.urls import path
from .views import user_create, resolver_create, user_login

urlpatterns = [
    path('register/user/', user_create),
    path('register/resolver/', resolver_create),
    path('login/', user_login),
]
