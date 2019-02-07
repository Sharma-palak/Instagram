from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from rest_framework import generics

#from .serializers import LoginSerializer
from django.shortcuts import get_object_or_404
from .filters import UserFilter
from rest_framework import filters
from .serializers import *
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.parsers import MultiPartParser,FormParser,JSONParser,FileUploadParser
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
        #password=serializer.validated_data['password']
        django_login(request,user)

        #token,created=Token.objects.get_or_create(user=user)
        return Response({'user_id': user.id}, status=status.HTTP_201_CREATED)









class LogoutView(APIView):
    permission_classes = [permissions.AllowAny, ]
    #authentication_classes=(TokenAuthentication,)

    def get(self,request):

        django_logout(request)
        return Response({'detail':'logged out successfully!!'},status=status.HTTP_200_OK)






class UserCreateAPIView(generics.CreateAPIView):
    permission_classes=(permissions.AllowAny,)

    serializer_class=UserCreateSerializer


    queryset= User.objects.all()
    model = User

    # def get(self,request,*args,**kwargs):
    #     que=User.objects.get(id=id)
    #     print(que)
    #     return Response(que)

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

class ProfileEdit(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly)
    queryset = User.objects.all()
    # parser_classes = (MultiPartParser, FormParser, JSONParser,FileUploadParser)
    serializer_class = UserProfileSerializer


class Profile_View(APIView):
    serializer_class = ProfileViewSerializer
    def get(self,request,*args,**kwargs):
        get_data=Profile.objects.get(id=request.user.id)
        serializer=ProfileViewSerializer(get_data)
        return Response(serializer.data)


class Post_View(generics.RetrieveUpdateDestroyAPIView):
    queryset=Post.objects.all()
    serializer_class=PostSerializer

'''


class PostView(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsPostOrReadOnly)
    #parser_classes = (MultiPartParser, FormParser, JSONParser, FileUploadParser)
    # @action(detail=False, methods=['post'])
    # def list1(self,request,*args,**kwargs):
    #     serializer = PostSerializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         return Response({'detail':serializer.data})

    def perform_create(self, serializer):
        user_obj = self.request.user.username
        print(user_obj)
        serializer.save(user=self.request.user,name=user_obj)

# class LikeView(viewsets.ModelViewSet):
#     serializer_class = LikeSerializer
#     queryset = Post.objects.all()
#     def perform_create(self, serializer):
#         serializer.save(likes=self.request.user)

    # def get_user(self, obj):
    #     return str(obj.user.username)

# class LikeView(viewsets.ModelViewSet):
#     serializer_class = LikeSerializer
#     queryset = Activity.objects.all()
#     permission_classes = (permissions.IsAuthenticated,)
#
#     @action(detail=False, methods=['post','get'])
#     def get_like(self,request,*args,**kwargs):
#         post =










    # def perform_update(self, serializer):
    #     instance=serializer.save(user=self.request.user)
    #     instance.save()

    # @action(methods=['post'],detail=True)
    # def create_post(self, request):
    #     serializer = PostSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(user=request.user.id)
    #         return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








class ProfileView(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
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



# class ProfileView(viewsets.ModelViewSet):
#     serializer_class = ProfileSerializer
#     queryset = User.objects.all()
#     permission_classes = (permissions.IsAuthenticated,)
#     parser_classes = (MultiPartParser, FormParser, JSONParser, FileUploadParser)
#
#     # def perform_update(self, serializer):
#     #     user_obj = self.request.username
#     #     print(user_obj)
#     #     serializer.save(user=self.request.user,name=user_obj)


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
    
    # @action(method=['GET'],detail=True)
    # def list_comment(self,request,*args,**kwargs):
    #     post_id = self.kwargs['postid']
    #     comment = Comment.objects.get(id=post_id)
    #     serializer = CommentSerializer(comment)
    #     return Response({'detail':serializer.data})

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
        print(post)

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
    #serializer_class = user_filter()
    filter_backends = (filters.SearchFilter,)
    #new_friend = ('username',)

    def get(self,request,*args,**kwargs):
        user_list = User.objects.all()
        user_filter = UserFilter(request.GET, queryset=user_list)
        serializer = UserCreateSerializer(user_filter)
        return Response({'detail':serializer.data})















        # try:
        #     like = Activity.objects.filter(user=self.request.user)
        # except (Activity.DoesNotExist):
        #     like = None
        # if like is None:
        #     Activity.objects.create(post=postid,user=request.user)
        #     return Response("Liked")
        # else:
        #     like=Activity.objects.filter(post=postid,user=request.user)
        #     like.delete()
        #     return Response("Disliked")
















# #
# class Post_View(APIView):
#
#     serializer_class=PostSerializer
#     def get(self,request,*args,**kwargs):
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
#
#
#     def post(self,request,*args,**kwargs):
#
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response({'data':serializer.data}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class Post_Video(APIView):
#     serializer_class = PostSerializer2
#     def post(self, request, *args, **kwargs):
#         data = {
#             'id': id,
#             'user': request.user.id,
#             'title': request.data.get('title'),
#             'caption': request.data.get('caption'),
#             'files': request.data.get('files'),
#             # 'files':request.data.get('files'),
#         }
#         serializer = PostSerializer2(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# class Post_List(APIView):
#     serializer_class=PostSerializer2,PostSerializer
#     def get(self, request, *args, **kwargs):
#         posts = Post.objects.filter(picture='')
#         posts1=Post.objects.filter(files='')
#         serializer = PostSerializer(posts1, many=True)
#         serializer2=PostSerializer2(posts,many=True)
#         response=serializer.data+serializer2.data
#         return Response(response)
# '''
# class Post_Detail(APIView):
#     permission_classes = (permissions.IsAuthenticated, IsPostOrReadOnly)
#     def get_object(self, pk,):
#         try:
#             return Post.objects.get(pk=pk)
#         except Post.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         post1 = self.get_object(pk)
#         post_image = PostSerializer(post1)
#         post_video=PostSerializer2(post1)
#         response=post_image.data
#         return Response(response)
#
#     def delete(self, request, pk, format=None):
#         post = self.get_object(pk)
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#
# class Post_Detail(generics.DestroyAPIView):
#     permission_classes = (permissions.IsAuthenticated,IsPostOrReadOnly)
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
