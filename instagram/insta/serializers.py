from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,login
from rest_framework import exceptions
from django.db.models import Q
from rest_framework.serializers import(ModelSerializer,EmailField,IntegerField)
from django.contrib.auth import get_user_model
from rest_framework import request
from rest_framework.serializers import ValidationError

from .models import (Post,Activity,Comment,Profile)


User=get_user_model()

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField(style={'input_type': 'password'},required=True)
    print("1")

    class Meta:
        print("6")
        model = User
        fields = ['username','password',]
        extra_kwargs = {"password": {"write_only": True}
                       }

    def validate(self,data):
        username=data['username']
        password=data['password']
        print("2")

        #username=data.get("username","")
        #password=data.get("password","")
        if username and password:
            print("3")
            user=authenticate(username=username,password=password)
            if user:
                if user.is_active:
                    data["user"]=user
                else:
                    msg="User is deactivated"
                    raise exceptions.ValidationError(msg)
            else:
                print("4")
                msg="Unable to login with given credentials"
                raise exceptions.ValidationError(msg)
        else:
            msg="Must provide username and password both"
            raise exceptions.ValidationError(msg)


        return data

User=get_user_model()
class UserCreateSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(label='Email Address')
    password = serializers.CharField(style={'input_type': 'password'},required=True)
    username=serializers.CharField()
    first_name=serializers.CharField()
    last_name=serializers.CharField()
    class Meta:
        model = User
        write_only_fields = ('password',)
        read_only_fields = ('id',)
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name',]

        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, data):
         k=0
         email=data['email']
         username=data['username']
         password=data['password']
         validLetters = "abcdefghijklmnopqrstuvwxyz"

         query=User.objects.filter(username=username)
         for char in username.lower():
             if (char in validLetters):
                 k=1
         if (k==0):
             raise ValidationError("Must contain alphabets")


         if (len(username)<=4):
             raise ValidationError("Username is too short")
         if (len(password)<=4):
             raise ValidationError("password is too short")
         if query.exists():
             raise ValidationError("User with this name already exists!!")
         user_qs=User.objects.filter(email=email)
         if user_qs.exists():
              raise ValidationError("This email has already been registered!!")
         return data


    def create(self, validated_data):
      user = User.objects.create(
          username=validated_data['username'],
          email=validated_data['email'],
          first_name=validated_data['first_name'],
          last_name=validated_data['last_name'],
          password=validated_data['password'],
      )
      user.set_password(validated_data['password'])
      user.is_active=False
      user.save()
      return user





'''

class ProfileSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(source='user.username')
    # email=serializers.EmailField(source='user.email')
    # first_name=serializers.CharField(source='user.first_name')
    # last_name=serializers.CharField(source='user.last_name')
    user=UserCreateSerializer()
    bio = serializers.CharField(source='profile',allow_blank=True, required=False)
    phone_no = serializers.CharField(source='profile')
    birth_date = serializers.DateField(source='profile')
    image = serializers.ImageField(source='profile')

    class Meta:
        model = Profile
        fields = ('user', 'bio', 'image','phone_no',
                  'birth_date',)

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        profile_data=Profile.objects.create(
            user_data=user_data,
            bio=validated_data['bio'],
            phone_no=validated_data['phone_no'],
            birth_date=validated_data['birth_date'],
            image=validated_data['image']
        )
        return profile_data

'''

# class ProfileSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Profile
#         fields = ('image', 'bio', 'phone_no',)
#
#
# class ProfileViewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Profile
#         fields=('id','image','bio')
#
#
# class UserProfileSerializer(serializers.ModelSerializer):
#     profile=ProfileSerializer(required=False)
#
#     class Meta:
#         model=User
#         fields=['id','username','first_name','last_name','email','profile']
#
#     def create(self, validated_data):
#         profile_data = validated_data.pop('profile')
#         user = User.objects.create(**validated_data)
#         Profile.objects.create(user=user, **profile_data)
#         return user
#
#     def update(self, instance, validated_data):
#         profile_data = validated_data.pop('profile')
#         profile = instance.profile
#
#         instance.username = validated_data.get('username', instance.username)
#         instance.email = validated_data.get('email', instance.email)
#         instance.first_name=validated_data.get('first_name',instance.first_name)
#         instance.last_name=validated_data.get('last_name',instance.last_name)
#         instance.save()
#
#         profile.image = profile_data.get('image',profile.image)
#         profile.bio=profile_data.get('bio',profile.bio)
#         profile.phone_no=profile_data.get('phone_no',profile.phone_no)
#         #profile.birth_date=profile_data.get('birth_date',profile.birth_date)
#         profile.save()
#         return instance
#
# class PostSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = ('id','caption','title', 'picture','date_created',)
#         read_only_fields = ('user',)
#
#     def create(self, validated_data):
#         post1 = Post.objects.create(**validated_data)
#         return post1


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id','title','caption','picture','files','date_created','name','user')
        read_only_fields = ('id','name','user')

    # def create(self, validated_data):
    #     profile_data = validated_data.pop('profile')
    #     user = User.objects.create(**validated_data)
    #     Profile.objects.create(user=user, **profile_data)
    #     return user
    #
    # def update(self, instance, validated_data):
    #     profile_data = validated_data.pop('profile')
    #     profile = instance.profile
    #
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.caption = validated_data.get('caption', instance.caption)
    #     instance.pictures=validated_data.get('pictures',instance.pictures)
    #     instance.files=validated_data.get('last_name',instance.files)
    #     instance.save()
    #
    #     profile.image = profile_data.get('image',profile.image)
    #     profile.bio=profile_data.get('bio',profile.bio)
    #     profile.phone_no=profile_data.get('phone_no',profile.phone_no)
    #     #profile.birth_date=profile_data.get('birth_date',profile.birth_date)
    #     profile.save()
    #     return instance



class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('id','image','bio','phone_no','name','user')
        read_only_fields = ('user','name',)

# class ProfileSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = User
#         fields = ('image','bio','phone_no','name')
#         read_only_fields = ('name')

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Activity
        fields = ('user', 'post', 'like')
        read_only_fields = ('user', 'post')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('user','post','text')
        read_only_fields = ('user','post')


