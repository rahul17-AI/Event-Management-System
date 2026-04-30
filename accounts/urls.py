from django.urls import path
from accounts import views


urlpatterns=[
    path('',views.register, name='register'),
    path('login',views.user_login, name='login'),
    path('home',views.home, name='home'),
    path('logout',views.user_logout, name='logout'),
    path('profile',views.userprofile, name='profile'),
    path('update',views.userUpdate,name='update')   
]