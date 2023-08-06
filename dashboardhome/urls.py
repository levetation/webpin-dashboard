"""dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from . import views
from users import views as user_views

urlpatterns = [
    path('', views.home, name='home'),
    
    # template
    path('sample', views.sample, name='sample'),
    path('alerts', views.alerts, name='alerts'),
    path('buttons', views.buttons, name='buttons'),
    path('cards', views.cards, name='cards'),
    path('forms', views.forms, name='forms'),
    path('typography', views.typography, name='typography'),

    # auth
    path('register_user', user_views.register_user, name='register_user'),
    path('logout_user', user_views.logout_user, name='logout_user'),
    path('login_user', user_views.login_user, name='login_user'),
    path('account', user_views.account, name='account'),

    # dev
    path('cardlist', views.cardlist, name='cardlist'),



]
