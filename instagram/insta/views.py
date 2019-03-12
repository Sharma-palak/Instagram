
from rest_framework import generics
from django.shortcuts import get_object_or_404
#from .filters import UserFilter
from django.db.models import Q
from django.contrib.auth import get_user_model
User=get_user_model()
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
from .permissions import IsPostOrReadOnly,IsCommentOrReadOnly,IsOwnerOrReadOnly
from rest_framework import viewsets
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView
from rest_framework import generics,permissions
# from .import models
# from .serializers import *
#from django.contrib.auth.models import User
#from django.contrib.auth import get_user_model

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
    def get_queryset(self):
        if self.action == 'users_Post':
            return Post.objects.filter(user=self.request.user)
        else:
            return Post.objects.all()
    # def list(self,request,*args,**kwargs):
    #     k=Post.objects.all()
    #     list=[]
    #     for j in k:
    #         print("hii")
    #         print(j.user.id)
    #         post_user=Friend.objects.filter(current_user=request.user.id)
    #         if(post_user.user.filter(id=j.user.id)):
    #             print(post_user)
    #             p= Post.objects.filter(user=j.user.id)
    #             list.append(p)
    #     serializer=PostSerializer(list,many=True)
    #     print(serializer.data)
    #     return Response({'detail':serializer.data})



    @action(methods=['GET',],detail=False)
    def users_Post(self,*args,**kwargs):
        list = Post.objects.filter(user = self.request.user)
        serializer = PostSerializer(list,many=True)
        return Response({'detail':serializer.data})

class ProfileView(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly)
    lookup_field = 'id'
    def perform_update(self, serializer):
        user_obj = self.request.user.username
        print(user_obj)
        serializer.save(name=user_obj)

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
        postid = self.kwargs['postid']
        post = Post.objects.get(id=postid)

        comment = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comment,many=True)
        print(serializer.data)
        return Response({'detail':serializer.data})

    def post(self,request,*args,**kwargs):
        postid = self.kwargs['postid']
        post = Post.objects.get(id=postid)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user,post=post,name=request.user.username)
            return Response({'detail':serializer.data})

class Comment_Edit(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsCommentOrReadOnly)

    def perform_create(self, serializer):
        user_obj = self.request.user.username
        print(user_obj)
        serializer.save(user=self.request.user,name=user_obj)

# class Add_Friend(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserCreateSerializer
#     filter_backends = (filters.SearchFilter,)
#     search_fields = ('username',)
#     def get_queryset(self,*args,**kwargs):
#          operation = self.kwargs['operation']
#          print(type(operation))
#          queryset_list = User.objects.all()
#          query = self.request.GET.get("search")
#          if query:
#              queryset_list = queryset_list.filter(Q(username__icontains=query)).distinct()
#              user_name = User.objects.get(username=query)
#              new_friend = User.objects.get(username=user_name)
#
#              if operation == str(1):
#                  print("entered")
#                  Friend.make_friend(self.request.user,new_friend)
#              if operation == str(2):
#                  Friend.lose_friend(self.request.user,new_friend)
#
#          return queryset_list
class Add_Friend(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    def get_queryset(self,*args,**kwargs):
        queryset_list = User.objects.all().exclude(id=self.request.user.id)
        query = self.request.GET.get("search")
        if query :
            queryset_list = queryset_list.filter(Q(username__startswith=query)).distinct()
        return queryset_list

    def retrieve(self,request,*args,**kwargs):
        query = self.request.GET.get("search")
        p=User.objects.get(pk=kwargs['pk'],username__icontains=query)
        #new_friend=User.objects.filter(username=p)
        friend,created=Friend.objects.get_or_create(current_user=self.request.user)
        if (p in friend.user.all()):
            friend.user.remove(p)
            print(friend.user.all())
            return Response({'detail':'removed'})
        elif(p != self.request.user):
            friend.user.add(p)
            print(friend.user.all())
            return Response({'detail':'added'})
        elif (p==self.request.user):
            return Response({'detail':'cannot add or remove'})
    @action(methods=['GET'],detail=False)
    def list_friend(self,request,*args,**kwargs):
        friend_list=Friend.objects.filter(current_user=self.request.user)
        list=[]
        for i in friend_list:
            for j in i.user.all():
                for k in User.objects.filter(username=j):
                    print(k)
                    list.append(k)
        serializer = ProfileSerializer(list,many=True)
        return Response({'detail':serializer.data})

        # if query:
        #      queryset_list = queryset_list.filter(Q(username__icontains=query)).distinct()
        #      user_name = User.objects.get(username=query)
        #      new_friend = User.objects.get(username=user_name)
        #      if self.action == 'add':
        #          friend= Friend.objects.get_or_create(current_user=self.request.user)
        #          friend.user.add(new_friend)
        #          print('hello')
        #          print(friend.user.all())
        #      if self.action == 'remove':
        #          friend= Friend.objects.get_or_create(current_user=self.request.user)
        #          friend.user.remove(new_friend)
        #
        # return queryset_list





    # @action(methods=['GET'], detail=False)
    # def add(self,*args,**kwargs):
    #     query=self.get_queryset()
    #     print(query)
    #     print(Friend.objects.get(current_user=self.request.user))
    #     return Response({'detail':"added"})









class Friend_List(generics.ListAPIView):
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer
    def get(self,*args,**kwargs):
        current_id = self.kwargs['userid']
        list = Friend.objects.filter(current_user=current_id)
        print(list)
        serializer = FriendSerializer(list,many=True)

        return Response({'detail':serializer.data})

class DeleteAccount(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def destroy(self, request, *args, **kwargs):
        q=User.objects.filter(id=self.request.user.id)
        q.delete()
        serializer=UserCreateSerializer(q)
        return Response({'detail':'your account is deleted successfully'})
















