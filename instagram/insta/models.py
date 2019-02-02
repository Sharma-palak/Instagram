from django.db import models
#from __future__import unicode_literals

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    #owner = models.ForeignKey('auth.User', related_name='profiles', on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
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
    title = models.CharField(max_length=255,null=True,blank=True)
    caption=models.TextField(max_length=500, blank=True,null=True)
    picture=models.ImageField(upload_to='images',blank=True)
    files=models.FileField(upload_to='file',blank=True)
    date_created=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class Activity(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    like = models.BooleanField(default=True)
    like_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return (self.post.id)

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)


# class LikeDislike(models.Model):
#     # LIKE = 1
#     # DISLIKE = -1
#     #
#     # VOTES = (
#     #     (DISLIKE, 'Dislike'),
#     #     (LIKE, 'Like')
#     # )
#     # user = models.ForeignKey(User,on_delete=models.CASCADE)
#     # rating = models.PositiveIntegerField(default=0)
#     # post=models.ManyToManyField(Post)
#     # activity = models.CharField(max_length=10,choices=VOTES,
#     #     default=LIKE,)
#     #
#     # def __str__(self):
#     #     return (self.post)
#
#     user=models.ForeignKey(User,on_delete=models.CASCADE)
#     activity = models.ForeignKey(Post)
#     status = models.BooleanField()
#
#     def __str__(self):
#         return self.user







