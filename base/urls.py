
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="Home-Page"),
    path('room/<str:pk>/', views.room, name="Room-Page"),
    path('create-room/', views.create_room, name="create-room"),
    path('update-room/<str:pk>/', views.update_room, name='update-room'),
    path('register/', views.register, name='register'),
    path('delete-message/<str:pk>/', views.delete_message, name='delete-message'),
    path('login/', auth_views.LoginView.as_view(template_name = 'base/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'base/logout.html'), name='logout'),
    path('user-profile/<str:pk>/', views.user_profile, name='user-profile'),
    path('delete-room/<str:pk>/', views.delete_room, name='delete-room'),


]


