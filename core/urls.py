from django.urls import path, re_path
from django.conf import settings
from . import views


urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    
    path('home/', views.category_list, name='category_list'),
    path('category/<slug:category_slug>/', views.cheatsheet_list, name='cheatsheet_list'),
    path('cheatsheet/<slug:cheatsheet_slug>/', views.cheatsheet_detail, name='cheatsheet_detail'),
    
    # path('login/', views.login, name="login"),
    # path('register/',views.register, name="register"),
    # path('logout/',views.logout, name="logout"),
    
    path('login/', views.under_development, name="login"),
    path('register/',views.under_development, name="register"),
    path('logout/',views.under_development, name="logout"),
    path('profile/',views.under_development, name="profile"),
    
    path('under-development/', views.under_development, name='under_development'),
    

]

if not settings.DEBUG:
    urlpatterns += [
        # this is for developement only
        re_path(r'^.*$', views.custom_page_not_found_view, kwargs={'exception': Exception('Page Not Found')}),
    ]