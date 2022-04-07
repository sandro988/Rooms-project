from django.urls import path 
from . import views 

urlpatterns = [ 
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),


    path('create-room/', views.createRoom, name='create-room'),
    path('edit-room/<str:pk>/', views.editRoom, name='edit-room'),
    path('delete-room/<str:pk>/', views.deleteRoom, name='delete-room'),
    path('join-room/<str:pk>/', views.joinRoom, name='join-room'),
    path('leave-room/<str:pk>/', views.leaveRoom, name='leave-room'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('register/', views.registerPage, name='register'),

    path('delete-comment/<str:pk>/', views.deleteMessage, name='delete-message'),
    path('edit-comment/<str:pk>/', views.editMessage, name='edit-message'),
    path('add-comment/<str:pk>/', views.addMessage, name='add-message'),

    path('edit-user/<str:pk>/', views.editUser, name='edit-user')
]