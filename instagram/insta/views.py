from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from rest_framework import generics

#from .serializers import LoginSerializer
from .serializers import UserCreateSerializer,LoginSerializer,ProfileSerializer,UserProfileSerializer
from django.shortcuts import redirect
#base_users.py
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.contrib.auth import login as django_login,logout as django_logout
from instagram.settings import EMAIL_HOST
from django.template.loader import render_to_string
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from instagram.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.core.mail import send_mail
from .models import Profile

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

    def post(self, request, *args, **kwargs,):
        username=request.data.get('username')
        password=request.data.get('password')
        email=request.data.get('email')
        first_name=request.data.get('first_name')
        last_name=request.data.get('last_name')
        temp_data = {
              'username': username,
              'password': password,
              'email': email,
              'first_name': first_name,
              'last_name': last_name,
          }
        #que=User.objects.get(id=pk)
        serializer=UserCreateSerializer(data=temp_data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        current_site = get_current_site(request)

        from_mail = EMAIL_HOST_USER
        mail_subject = 'Activate your instagram account.'
        message = render_to_string('insta/activation.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': account_activation_token.make_token(user),
        })
        # to_email = form.cleaned_data.get('email')
        to_email = [user.email]
        # print(to_email)
        # email = EmailMessage(
        #  mail_subject, message,from_mail, to=[to_email]
        #   )
        # email.send()
        send_mail(mail_subject, message, from_mail,to_email, fail_silently=False)
        messages.success(request, 'Confirm your email to complete registering with ONLINE-AUCTION.')
        return Response('Please confirm your email address to complete the registration')



class Activate(APIView):
    def get(self,request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            django_login(request, user)
            messages.success(request,"Email Verified")
            return redirect('login')
        else:
            messages.error(request, "Activation Email Link is Invalid.Please try again!!")
            return redirect('register')

'''
class ProfileView(APIView):
    serializer_class=ProfileSerializer
    def post(self, request,id ,*args, **kwargs):
        phone_no=request.data.get('phone_no')
        image=request.data.get('image')
        bio=request.data.get('bio')
        birth_date=request.data.get('birth_date')
        temp={
            # 'username':username,
            #  'email':email,
            #  'first_name':first_name,
            #  'last_name':last_name,
            'phone_no':phone_no,
             'image':image,
             'bio':bio,
             'birth_date':birth_date,
        }


        serializer=ProfileSerializer(data=temp)
        serializer.is_valid(raise_exception=True)
        serializer.save()
'''

class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

'''
class Profile_View(APIView):
    serializer_class = ProfileSerializer
    def get(self,request,id,*args,**kwargs):
        get_data=Profile.objects.get(id=id)
        context={
            "get_data":get_data
        }
        return Response(request,context)
'''




