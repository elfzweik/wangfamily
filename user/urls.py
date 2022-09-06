from django.urls import path
from . import views


urlpatterns = [
    path('login_for_medal/', views.login_for_medal, name='login_for_medal'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('user_info/', views.user_info, name='user_info'),
    path('change_name/', views.change_name, name='change_name'),
    path('bind_email/', views.bind_email, name='bind_email'),
    path('change_avatar/', views.change_avatar, name='change_avatar'),
     path('change_password/', views.change_password, name='change_password'),
]