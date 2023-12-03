from django.db import models
from django.conf import settings

## protect object ID's
from django_hashids import HashidsField
from django.core.management.utils import get_random_secret_key

## compress uploaded files
from io import BytesIO
import sys
import os
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile

# Generate a random and secure salt
salt = get_random_secret_key()

def user_directory_path(instance, filename):
    # https://docs.djangoproject.com/en/4.2/ref/models/fields/#django.db.models.FileField
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "user_{0}/{1}".format(instance.author.id, filename)


class Board(models.Model):
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=1000, null=True, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='boards/board_images/')
    public = models.BooleanField(default=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    hashid = HashidsField(real_field_name="id", salt=salt, min_length=8)

    # https://stackoverflow.com/questions/52183975/how-to-compress-the-image-before-uploading-to-s3-in-django
    def save(self):
        
        if not os.path.isfile(self.image.path): # prevents generating duplicate images
            # Open uploaded image
            im = Image.open(self.image)
            output = BytesIO()

            # Resize/modify image - retaining height and width ratio
            original_width, original_height = im.size
            aspect_ratio = round(original_width / original_height)
            desired_height = 200 # Edit to add your desired height in pixels
            desired_width = desired_height * aspect_ratio
            im = im.resize((desired_width, desired_height))

            # Save modifications to output
            im.save(output, format='JPEG', quality=100)
            output.seek(0)

            # Update the imagefield value
            self.image = InMemoryUploadedFile(
                output, 
                'ImageField', 
                "%s.jpg" % self.image.name.split('.')[0], 
                'image/jpeg',
                sys.getsizeof(output), 
                None
            )

        super(Board, self).save()



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