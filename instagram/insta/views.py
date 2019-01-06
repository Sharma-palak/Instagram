from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

#from .serializers import LoginSerializer
from .serializers import UserCreateSerializer,LoginSerializer
from django.contrib.auth import login as django_login,logout as django_logout
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework import generics,permissions
from .import models
from .import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User=get_user_model()
'''
class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """
    # This permission class will overide the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            serializer = LoginSerializer(data={
                "username":""
            })
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
'''
class LoginView(APIView):
    permission_classes=[permissions.AllowAny,]

    #model=User
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data["user"]
        #password=serializer.validated_data['password']
        django_login(request,user)
        #token,created=Token.objects.get_or_create(user=user)
        return Response({'detail':'logged in successfully!!'},status=200)
'''

class LoginView(APIView):
    permission_classes=[permissions.AllowAny,]
    #serializer_class=UserLoginSerializer
    def post(self,request,*args,**kwargs):
        data=request.data
        serializer = LoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)
            user = serializer.validated_data["user"]
            django_login(request, user)
            return Response(user,status=HTTP_200_OK)
        return Response(serializers.errors,status=HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes=[permissions.AllowAny]
    def post(self,request,*args,**kwargs):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        serializer = LoginSerializer(data=request.data)
        if not username and not password:
            return Response({'detail':'No credentials are provided'})
        elif username is None:
            return Response ({'detail':'Username is required'})
        elif password is None:
            return Response({'detail': 'Password is required '})
        elif serializer.is_valid(raise_exception=True):
            user=serializer.validated_data["user"]
            django_login(request,user)
            return Response(user,status=HTTP_200_OK)
        else:
            return Response(serializers.errors,status=HTTP_400_BAD_REQUEST)


'''






class LogoutView(APIView):
    authentication_classes=(TokenAuthentication,)

    def post(self,request):
        django_logout(request)
        return Response({'detail':'logged out successfully!!'},status=204)

'''
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
    model = User
    permission_classes = [
        permissions.AllowAny  # Or anon users can't register
    ]
'''
class LoginView(APIView):
    permission_classes=[permissions.AllowAny]

    def post(self,request,*args,**kwargs):
        data=request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data=serializer.data
            return Response(new_data,status=HTTP_200_OK)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)

'''









