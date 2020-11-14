from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [

	path('login/' , views.MyLoginView.as_view(), name='login'),
	path('logout/' , auth_views.LogoutView.as_view() , name='logout'),
	path('register/' , views.user_register , name='register'),
	path('' , views.home , name='home'),


]