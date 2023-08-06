from django.db import models
from django.conf import settings

class Bookmark(models.Model):
    title = models.CharField(max_length=500, null=True, blank=False)
    address = models.CharField(max_length=1_000)
    notes = models.CharField(max_length=100_000, null=True, blank=False)
    category = models.CharField(max_length=250, null=True, blank=False)
    save_date = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title