# Generated by Django 2.1.1 on 2019-02-01 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insta', '0006_remove_post_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='like_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
