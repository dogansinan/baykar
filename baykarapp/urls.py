from django.urls import path
from .views import *
from baykarapp import views


urlpatterns=[
    path('', index , name='index'),
    path('login/' , login , name='login'),
    path('register/' , register , name='register'),
    path('logout/' , logout_request , name='logout'),
    path('iha-information/<str:ihaid>' , ihaDetay , name='iha-information'),
    path('profile/' , profil , name='profile'),
    path('rental/' , kiralama , name='rental'),
    path('delete/<int:id>' , deleteIha , name='deleteIha'),
    path('iha' , iha , name='iha'),
    path('management' , management , name='management'),
    # JSON Response
    path('json/' , views.kiralanan_iha_json, name='kiralanan_iha_json'),
    path('ihajson/' , views.iha_json, name='iha_json'),
    path('userjson/' , views.user_json, name='user_json'),
   

]