from django.urls import path
from UserProfile import views

urlpatterns = [
    path('', views.user_profile, name='user_profile'),
    
]