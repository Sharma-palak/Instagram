
from rest_framework import generics
from django.shortcuts import get_object_or_404
#from .filters import UserFilter
from django.db.models import Q
from rest_framework import filters
from .serializers import *
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.parsers import MultiPartParser,FormParser,JSONParser,FileUploadParser
from django.contrib.auth import login as django_login,logout as django_logout
from rest_framework.response import Response
from instagram.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.core.mail import send_mail
from .models import *
from django.http import Http404
from .permissions import IsOwnerOrReadOnly,IsPostOrReadOnly
from rest_framework import viewsets
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView
from rest_framework import generics,permissions
# from .import models
# from .serializers import *
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from rest_framework.decorators import action
#User=get_user_model()


class LoginView(APIView):
    permission_classes=[permissions.AllowAny,]
    serializer_class = LoginSerializer

    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data["user"]
        django_login(request,user)
        return Response({'user_id': user.id}, status=status.HTTP_201_CREATED)









class LogoutView(APIView):
    permission_classes = [permissions.AllowAny, ]

    def get(self,request):

        django_logout(request)
        return Response({'detail':'logged out successfully!!'},status=status.HTTP_200_OK)






class UserCreateAPIView(generics.CreateAPIView):
    permission_classes=(permissions.AllowAny,)
    serializer_class=UserCreateSerializer
    queryset= User.objects.all()
    model = User

    def post(self, request, *args, **kwargs,):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        temp_data = {
              'username': username,
              'password': password,
              'email': email,
              'first_name': first_name,
              'last_name': last_name,
          }
        #que=User.objects.get(id=pk)
        serializer = UserCreateSerializer(data=temp_data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            current_site = get_current_site(request)
            from_mail = EMAIL_HOST_USER
            mail_subject = 'Activate your instagram account.'
            message = render_to_string('insta/activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })

            to_email = [user.email]

            send_mail(mail_subject, message, from_mail, to_email, fail_silently=False)
            messages.success(request, 'Confirm your email to complete registering with Instagram.')
            return Response({'message': 'Please confirm your email address to complete the registration',},
                            status=status.HTTP_201_CREATED)
        return Response("bad attempt", status=status.HTTP_400_BAD_REQUEST)


class Activate(APIView):
    permission_classes = (permissions.AllowAny,)
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
            return Response({'detail':'email verified'})
        else:
            messages.error(request, "Activation Email Link is Invalid.Please try again!!")
            return redirect('register')




class PostView(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsPostOrReadOnly)

    def perform_create(self, serializer):
        user_obj = self.request.user.username
        print(user_obj)
        serializer.save(user=self.request.user,name=user_obj)


class ProfileView(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly)
    #parser_classes = (MultiPartParser, FormParser, JSONParser, FileUploadParser)
    # def perform_create(self, serializer):
    #     user_obj = self.request.user.username
    #     serializer.save(user=self.request.user,name=user_obj)
    #
    # #@action(methods=['GET'], detail=True)
    # def update(self,*args, **kwargs):
    #     user = self.kwargs['pk']
    #     profile = Profile.objects.filter(user_id=user)
    #     serializer = ProfileSerializer(data=profile,many=True)
    #     serializer.is_valid()
    #     serializer.save()
    #     return Response(serializer.data)
    # #
    # #@action(methods=['POST'],detail=True)
    # def post(self, request, *args, **kwargs):
    #     user_id = self.kwargs['pk']
    #     profile = Profile.objects.get(user_id=user_id)
    #     serializer = ProfileSerializer(data=request.data,instance=profile)
    #     serializer.is_valid()
    #     serializer.save()
    #     return Response(serializer.data)

    # def perform_create(self, serializer):
    #     user_obj = self.request.user.username
    #     print(user_obj)
    #     serializer.save(user=self.request.user,name=user_obj)





class LikeView(APIView):
    def get(self, request, *args, **kwargs):
        postid = self.kwargs['postid']
        post = Post.objects.get(id=postid)

        if(Activity.objects.filter(user=request.user, post=post).exists()):

            like=Activity.objects.filter(user=request.user,post=post).delete()
        else :
            like=Activity.objects.create(user=request.user,post=post)

        result= Activity.objects.filter(post=post).count()
        return Response({'detail':result})

class CommentView(APIView):
    serializer_class = CommentSerializer

    def get(self,request,*args,**kwargs):
        post_id = self.kwargs['postid']
        post = Post.objects.get(id=post_id)

        comment = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comment,many=True)
        print(serializer.data)
        return Response({'detail':serializer.data})

    def post(self,request,*args,**kwargs):
        post_id = self.kwargs['postid']
        post = Post.objects.get(id=post_id)

        # try:
        #    comment = Comment.objects.get(user=self.request.user, id=post_id)
        # except (Comment.DoesNotExist):
        #     comment = None
        # if comment is None:
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user,post=post)
            return Response({'detail':serializer.data})


class Add_Friend(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    def get_queryset(self,*args,**kwargs):
         operation = self.kwargs['operation']
         print(type(operation))
         queryset_list = User.objects.all()
         query = self.request.GET.get("search")
         if query:
             queryset_list = queryset_list.filter(Q(username__icontains=query)).distinct()
             user_name = User.objects.get(username=query)
             new_friend = User.objects.get(username=user_name)

             if operation == str(1):
                 print("entered")
                 Friend.make_friend(self.request.user,new_friend)
             if operation == str(2):
                 Friend.lose_friend(self.request.user,new_friend)
         return queryset_list














