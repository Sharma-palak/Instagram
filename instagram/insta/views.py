from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

#from .serializers import LoginSerializer
from .serializers import UserCreateSerializer,LoginSerializer
#base_users.py
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.contrib.auth import login as django_login,logout as django_logout
from instagram.settings import EMAIL_HOST
from django.template.loader import render_to_string
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView
from rest_framework import generics,permissions
from .import models
from .import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
#User=get_user_model()

class LoginView(APIView):
    permission_classes=[permissions.AllowAny,]
    serializer_class = LoginSerializer



    #model=User
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data["user"]
        #password=serializer.validated_data['password']
        django_login(request,user)
        #token,created=Token.objects.get_or_create(user=user)
        return Response({'detail':'logged in successfully!!'},status=200)


class ActivateAccount(APIView):
    def activate(request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            # return redirect('home')
            return Response('Thank you for your email confirmation. Now you can login your account.')
        else:
            return Response('Activation link is invalid!')






class LogoutView(APIView):
    #authentication_classes=(TokenAuthentication,)

    def get(self,request):

        django_logout(request)
        return Response({'detail':'logged out successfully!!'},status=204)




'''
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

    queryset= User.objects.all()
    model = User
    permission_classes = [
        permissions.AllowAny,
    ]

    print("hello")
    # def get(self,request,*args,**kwargs):
    #     que=User.objects.get(id=id)
    #     print(que)
    #     return Response(que)
'''
    def post(self, request, *args, **kwargs,):
        #que=User.objects.get(id=pk)
        serializer=UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        print(serializer.data)

        #current_site = get_current_site(data.request)
        current_site=EMAIL_HOST
        mail_subject = 'Activate your blog account.'
        message =render_to_string('insta/activation.html',{
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        #to_email = form.cleaned_data.get('email')
        to_email=que['email']
        print(to_email)
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return Response('Please confirm your email address to complete the registration')
'''
class Activate(APIView):
    def get(request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            django_login(request, user)
            # return redirect('home')
            return Response('Thank you for your email confirmation. Now you can login your account.')
        else:
            return Response('Activation link is invalid!')











