# Generated by Django 2.1.1 on 2019-02-01 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('insta', '0005_post_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
    ]