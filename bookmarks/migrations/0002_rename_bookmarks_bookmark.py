# Generated by Django 4.1.4 on 2023-08-05 11:19

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bookmarks', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Bookmarks',
            new_name='Bookmark',
        ),
    ]
