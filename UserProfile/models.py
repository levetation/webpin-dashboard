from django.db import models
from django.conf import settings

class UserProfileModel(models.Model):
    name = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='UserProfile/profile_pictures/')
    account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
