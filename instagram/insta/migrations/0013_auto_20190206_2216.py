# Generated by Django 2.1.1 on 2019-02-06 16:46

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('insta', '0012_auto_20190205_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_no',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128),
        ),
    ]