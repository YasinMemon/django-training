from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerUser, name='register'),
    path('logout/', views.logoutUser, name='logout'),

    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<str:pk>/', views.updateRoom, name='update-room'),
    path('delete-room/<str:pk>/', views.deleteRoom, name='delete-room'),

    path('delete_msg/<str:pk>/', views.delete_msg, name='delete_msg'),

    path('profile/<str:pk>/', views.userProfile, name='profile'),
    path('update-profile/', views.updateProfile, name='update_profile'),
]