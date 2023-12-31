# Generated by Django 4.1.4 on 2023-08-13 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0002_alter_board_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='BoardBookmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, null=True)),
                ('address', models.CharField(max_length=1000)),
                ('note', models.CharField(max_length=100000, null=True)),
                ('save_date', models.DateTimeField(auto_now_add=True)),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boards.board')),
            ],
        ),
    ]
