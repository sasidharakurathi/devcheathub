from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    
    path('home/', views.category_list, name='category_list'),
    path('category/<slug:category_slug>/', views.cheatsheet_list, name='cheatsheet_list'),
    path('cheatsheet/<slug:cheatsheet_slug>/', views.cheatsheet_detail, name='cheatsheet_detail'),

]