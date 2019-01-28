from django.conf.urls import url
from django.urls import path,include
from .import views
from django.conf import settings
from rest_framework_jwt.views import obtain_jwt_token

from django.conf.urls import url

#from .views import(LoginView,LogoutView,register,ChangePassword,UserCreateAPIView)
from .views import(UserCreateAPIView,LoginView,LogoutView,Activate,ProfileEdit,Profile_View,PostView,Post_Detail)

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('post', PostView)
urlpatterns = [
    path('',include(router.urls)),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view()),
    #('register/',register.as_view()),
    #path('loginin/',view=views.obtain_auth_token),
    #path('changepassword/',ChangePassword.as_view()),
   # url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^register/$', UserCreateAPIView.as_view(),name='register'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    Activate.as_view(), name='activate'),
    #url(r'^profile/(?P<id>[0-9]+)/$',ProfileView.as_view(), name='profile'),
    #re_path(r'^profile/<int:pk>/$',ProfileEdit.as_view(),name='profile'),
    path('profile/<int:pk>/',ProfileEdit.as_view(),name='profile'),
    path('profile_view/',Profile_View.as_view(),name='profile_view'),
    #path('post/(?P<id>[0-9]+)/',Post_View.as_view(),name='post'),
    # path('post/',Post_View.as_view(),name='post'),
    # path('post_video/<int:id>/',Post_Video.as_view(),name='post_video'),
    # path('post_list/',Post_List.as_view(),name='post_list'),
    path('post_detail/<int:pk>/',Post_Detail.as_view())
]
