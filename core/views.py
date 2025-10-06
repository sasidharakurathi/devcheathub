from django.shortcuts import render, get_object_or_404
from .models import Category, CheatSheet

def landing_page(request):
    
    return render(request, 'landing.html')


def category_list(request):
    categories = Category.objects.all().order_by('name')
    context = {
        'categories': categories,
    }
    return render(request, 'core/category_list.html', context)

def cheatsheet_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    cheatsheets = CheatSheet.objects.filter(category=category)
    context = {
        'category': category,
        'cheatsheets': cheatsheets
    }
    return render(request, 'core/cheatsheet_list.html', context)

def cheatsheet_detail(request, cheatsheet_slug):
    cheatsheet = get_object_or_404(CheatSheet, slug=cheatsheet_slug)
    context = {
        'cheatsheet': cheatsheet
    }
    return render(request, 'core/cheatsheet_detail.html', context)

def under_development(request):
    return render(request, 'core/under_development.html')


def register(request):
    pass

def login(request):
    pass

def logout(request):
    pass


def custom_page_not_found_view(request, exception):
    
    return render(request, "404.html", status=404)