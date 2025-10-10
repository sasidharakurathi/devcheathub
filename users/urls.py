from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    # path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.profile, name='profile'),
]
