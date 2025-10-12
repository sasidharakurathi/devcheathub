import json
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, CheatSheet
from django.http import JsonResponse
from django.db.models import Q, Count
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from .forms import JSONContributionForm 
from .models import Category, CheatSheet#, CodeSnippet
from django.core.paginator import Paginator

def landing_page(request):
    
    return render(request, 'landing.html')

def category_list(request):
    categories = Category.objects.filter(parent=None).annotate(
        cheatsheet_count=Count('cheatsheets', filter=Q(cheatsheets__status='APPROVED'))
    ).order_by('order')
    context = {
        'categories': categories
    }
    return render(request, 'core/category_list.html', context)

def category_detail(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    
    if category.subcategories.exists():
        context = {
            'category': category,
            'subcategories': category.subcategories.all()
        }
        return render(request, 'core/subcategory_list.html', context)
    else:
        # Get all cheatsheets for the category first
        cheatsheet_list = CheatSheet.objects.filter(category=category, status='APPROVED').order_by('id')
        
        # Create a Paginator object
        paginator = Paginator(cheatsheet_list, 10) # Show 10 cheatsheets per page
        
        # Get the page number from the URL (e.g., ?page=2)
        page_number = request.GET.get('page')
        
        # Get the Page object for the requested page number
        page_obj = paginator.get_page(page_number)
        
        context = {
            'category': category,
            'page_obj': page_obj, # Pass the Page object to the template
        }
        return render(request, 'core/cheatsheet_list.html', context)

def cheatsheet_detail(request, cheatsheet_slug):
    cheatsheet = get_object_or_404(CheatSheet, slug=cheatsheet_slug)
    context = {
        'cheatsheet': cheatsheet
    }
    return render(request, 'core/cheatsheet_detail.html', context)

def search_results(request):
    query = request.GET.get('q', '')
    
    if query:
        result_list = CheatSheet.objects.filter(
            Q(status='APPROVED') & 
            (Q(title__icontains=query) | Q(description__icontains=query) | Q(content__icontains=query))
        ).order_by('id')
    else:
        result_list = []

    paginator = Paginator(result_list, 10) # Show 10 results per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    query_params = request.GET.copy()
    if 'page' in query_params:
        del query_params['page']
    
    context = {
        'query': query,
        'page_obj': page_obj, # Pass page_obj instead of results
        'query_params': query_params.urlencode(),
    }
    return render(request, 'core/search_results.html', context)

# In core/views.py

@login_required
def contribute(request):
    if request.method == 'POST':
        form = JSONContributionForm(request.POST)
        if form.is_valid():
            json_string = form.cleaned_data['json_data']
            try:
                with transaction.atomic():
                    data_list = json.loads(json_string)

                    if not isinstance(data_list, list):
                        raise ValueError("The provided JSON must be a list of cheatsheet objects.")

                    for item in data_list:
                        # This is the corrected validation line
                        if not all(k in item for k in ['category', 'title', 'content']):
                            raise ValueError("A cheatsheet object is missing required keys: 'category', 'title', or 'content'.")

                        parent_category_name = item.get('parent_category')
                        category_name = item['category']
                        
                        final_category = None
                        if parent_category_name:
                            parent_cat, _ = Category.objects.get_or_create(name=parent_category_name, parent=None)
                            child_cat, _ = Category.objects.get_or_create(name=category_name, parent=parent_cat)
                            final_category = child_cat
                        else:
                            top_level_cat, _ = Category.objects.get_or_create(name=category_name, parent=None)
                            final_category = top_level_cat
                        
                        CheatSheet.objects.create(
                            author=request.user,
                            category=final_category,
                            title=item.get('title', 'No Title'),
                            description=item.get('description', ''),
                            content=item.get('content', {}),
                            status='PENDING'
                        )
                
                messages.success(request, f'Thank you! Your submission of {len(data_list)} cheatsheet(s) is awaiting review.')
                return redirect('category_list')

            except json.JSONDecodeError:
                messages.error(request, 'Invalid JSON format. Please check your syntax.')
            except ValueError as e:
                messages.error(request, f'Invalid data structure: {e}')
            except Exception as e:
                messages.error(request, f'An unexpected error occurred: {e}')

    else:
        form = JSONContributionForm()

    context = {'form': form}
    return render(request, 'core/contribute.html', context)

def about_page(request):
    """Renders the about page."""
    return render(request, 'core/about.html')

def under_development(request):
    return render(request, 'core/under_development.html')

def custom_page_not_found_view(request, exception):
    
    return render(request, "404.html", status=404)

def live_search(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        search_results = CheatSheet.objects.filter(
            Q(status='APPROVED') & 
            (Q(title__icontains=query) | Q(description__icontains=query) | Q(content__icontains=query))
        ).order_by('id').select_related('category')[:15]

        for result in search_results:
            # Get sections and tags from the new model method
            parsed_content = result.get_sections_and_tags()
            
            icon_url = ''
            if result.category.parent and result.category.parent.icon:
                icon_url = result.category.parent.icon.url
            elif result.category.icon:
                icon_url = result.category.icon.url
            
            results.append({
                'id': result.id, # Add ID for potential future use
                'title': result.title,
                'description': result.description, # Add description
                'url': result.get_absolute_url(),
                'category_name': result.category.name, # Rename for clarity
                'category_icon_url': icon_url,
                'sections': parsed_content['sections'], # Add structured sections
                'tags': parsed_content['all_tags'] # Add all unique tags
            })
    
    return JsonResponse({'results': results})



