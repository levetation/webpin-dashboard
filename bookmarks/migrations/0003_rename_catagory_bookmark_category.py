# Generated by Django 4.1.4 on 2023-08-06 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0002_rename_bookmarks_bookmark'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookmark',
            old_name='catagory',
            new_name='category',
        ),
    ]
