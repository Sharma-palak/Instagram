from django.conf.urls import url
from django.urls import path, re_path
from .import views
from django.conf import settings
from rest_framework_jwt.views import obtain_jwt_token
from django.conf.urls import url

from .views import(LoginView,LogoutView,register,ChangePassword)
urlpatterns = [
    path('login/',LoginView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('register/',register.as_view()),
    #path('loginin/',view=views.obtain_auth_token),
    path('changepassword/',ChangePassword.as_view()),
    url(r'^api-token-auth/', obtain_jwt_token),


]