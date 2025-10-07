from django.urls import path, re_path
from django.conf import settings
from . import views


urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    
    path('home/', views.category_list, name='category_list'),
    path('category/<slug:category_slug>/', views.category_detail, name='category_detail'),
    path('cheatsheet/<slug:cheatsheet_slug>/', views.cheatsheet_detail, name='cheatsheet_detail'),
    path('search/', views.search_results, name='search_results'),
    path('contribute/', views.contribute, name='contribute'),
    path('about/', views.about_page, name='about'),
    
    path('under-development/', views.under_development, name='under_development'),
    

]

if settings.DEBUG:
    urlpatterns += [
        # this is for developement only
        re_path(r'^.*$', views.custom_page_not_found_view, kwargs={'exception': Exception('Page Not Found')}),
    ]