from django.urls import path
from boards import views

urlpatterns = [
    path('', views.boards, name='boards'),
    path('delete_board/<str:id>', views.delete_board, name='delete_board'),
]
