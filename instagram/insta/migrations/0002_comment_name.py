# Generated by Django 2.1.1 on 2019-02-13 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insta', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='name',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
