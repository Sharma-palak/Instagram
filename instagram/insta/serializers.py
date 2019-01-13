from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,login
from rest_framework import exceptions
from django.db.models import Q
from rest_framework.serializers import(ModelSerializer,EmailField,IntegerField)
from django.contrib.auth import get_user_model
from django import request
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from instagram.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.core.mail import send_mail

User=get_user_model()

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()
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
         email=data['email']
         username=data['username']
         query=User.objects.filter(username=username)
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
      user.save()
      #return user
      current_site = get_current_site(request)

      from_mail =EMAIL_HOST_USER
      mail_subject = 'Activate your blog account.'
      message = render_to_string('insta/activation.html',{
           'user': user,
           'domain': current_site.domain,
           'uid': urlsafe_base64_encode(force_bytes(user.pk)),
           'token': account_activation_token.make_token(user),
        })
        # to_email = form.cleaned_data.get('email')
      to_email = user.email
      # print(to_email)
      # email = EmailMessage(
      #  mail_subject, message,from_mail, to=[to_email]
      #   )
      #email.send()
      send_mail(mail_subject, message, from_mail, to_email, fail_silently=False)
      messages.success(request, 'Confirm your email to complete registering with ONLINE-AUCTION.')
      return Response('Please confirm your email address to complete the registration')






