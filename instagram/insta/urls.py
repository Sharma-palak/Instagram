from django.conf.urls import url
from django.urls import path, re_path
from .import views
from django.conf import settings
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token
from django.conf.urls import url

#from .views import(LoginView,LogoutView,register,ChangePassword,UserCreateAPIView)
from .views import(UserCreateAPIView)

urlpatterns = [
    #path('login/',LoginView.as_view()),
   # path('logout/',LogoutView.as_view()),
    #('register/',register.as_view()),
    #path('loginin/',view=views.obtain_auth_token),
    #path('changepassword/',ChangePassword.as_view()),
   # url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^register/$',UserCreateAPIView.as_view(),name='register'),
    #url(r'^auth-jwt/', obtain_jwt_token),
    #url(r'^auth-jwt-refresh/', refresh_jwt_token),
    #url(r'^auth-jwt-verify/', verify_jwt_token),



]