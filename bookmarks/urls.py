from django.urls import path
from bookmarks import views
from bookmarks import bookmark_functions

urlpatterns = [
    path('bookmark_gallery', views.bookmark_gallery, name='bookmark_gallery'),
    path('get_favicon', bookmark_functions.get_favicon, name='get_favicon'),
    path('delete_bookmark/<str:id>', views.delete_bookmark, name='delete_bookmark'),
]
