from django.db import models
from django.conf import settings

def user_directory_path(instance, filename):
    # https://docs.djangoproject.com/en/4.2/ref/models/fields/#django.db.models.FileField
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "user_{0}/{1}".format(instance.author.id, filename)


class Board(models.Model):
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=1000, null=True, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='boards/board_images/')

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class BoardBookmark(models.Model):
    title = models.CharField(max_length=500, null=True, blank=False)
    address = models.CharField(max_length=1_000)
    note = models.CharField(max_length=100_000, null=True, blank=False)
    save_date = models.DateTimeField(auto_now_add=True)

    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    def __str__(self):
        return self.title