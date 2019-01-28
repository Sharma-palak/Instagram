from django.db import models
#from __future__import unicode_literals

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    #owner = models.ForeignKey('auth.User', related_name='profiles', on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE,)
    image=models.ImageField(upload_to='profile_images',blank=True)
    bio = models.TextField(max_length=500, blank=True)
    phone_no =models.CharField(max_length=10,blank=True)
    #birth_date = models.DateField(null=True,blank=True)
    def __str__(self):
        return self.user.username


    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_profile(sender, instance, **kwargs):
        instance.profile.save()


class Post(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255,default=None,blank=True)
    caption=models.TextField(max_length=500, blank=True,default=None)
    picture=models.ImageField(upload_to='images',blank=True)
    files=models.FileField(upload_to='file',blank=True)
    date_created=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
