from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

#from .serializers import LoginSerializer
from .serializers import UserCreateSerializer
from django.contrib.auth import login as django_login,logout as django_logout
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import generics,permissions
from .import models
from .import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User=get_user_model()
'''
class LoginView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data["user"]
        django_login(request,user)
        #token,created=Token.objects.get_or_create(user=user)
        return Response(status=200)


class LogoutView(APIView):
    authentication_classes=(TokenAuthentication,)

    def post(self,request):
        django_logout(request)
        return Response(status=204)

class register(generics.CreateAPIView):
    permissions_classes=(permissions.AllowAny,)
    def post(self,request,*args,**kwargs):
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')

        user=User.objects.create_user(username,email,password)
        user.first_name=first_name
        user.last_name=last_name
        user.save()
        #generating token for users
        #token=Token.objects.create(user=user)
        return Response({'detail':'User has been created with Token:'+token.key})

class ChangePassword(generics.CreateAPIView):
    permission_classes=(permissions.IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        user=get_object_or_404(User,username=request.user)
        user.set_password(request.POST.get('new_password'))
        user.save()
        return Response({'detail':'Password has been saved.'})

'''


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class=UserCreateSerializer

    queryset=User.objects.all()
    # model = User
    permission_classes = [
        permissions.AllowAny  # Or anon users can't register
    ]













