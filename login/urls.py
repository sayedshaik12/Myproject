from django.urls import path
from .  import views

urlpatterns=[
    path('',views.home,name='home'),
    path('about',views.about,name='about'),
    path('login',views.login,name='login'),
    path('signup',views.signup,name='signup'),
    path('progress',views.progress,name='progress'),
    path('logout',views.logout,name='logout'),
    path('delete/<int:id>',views.delete,name='delete'),
    path('password_reset',views.password_reset,name='password_reset'),
    path('generate_otp',views.generate_otp,name='generate_otp'),
    #path('validate_otp',views.validate_otp,name='validate_otp')
 
   
   
] 