import json
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, CheatSheet
from django.db.models import Q, Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from .forms import JSONContributionForm 
from .models import Category, CheatSheet, CodeSnippet
from django.core.paginator import Paginator

def landing_page(request):
    
    return render(request, 'landing.html')


def category_list(request):
    categories = Category.objects.filter(parent=None).annotate(
        cheatsheet_count=Count('cheatsheets', filter=Q(cheatsheets__status='APPROVED'))
    )
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
        cheatsheet_list = CheatSheet.objects.filter(category=category, status='APPROVED')
        
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

# def cheatsheet_list(request, category_slug):
#     category = get_object_or_404(Category, slug=category_slug)
#     cheatsheets = CheatSheet.objects.filter(category=category)
#     context = {
#         'category': category,
#         'cheatsheets': cheatsheets
#     }
#     return render(request, 'core/cheatsheet_list.html', context)

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
            (Q(title__icontains=query) | Q(description__icontains=query))
        )
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


@login_required
def contribute(request):
    if request.method == 'POST':
        form = JSONContributionForm(request.POST)
        if form.is_valid():
            json_string = form.cleaned_data['json_data']
            try:
                data = json.loads(json_string)

                # --- Basic Validation of the JSON structure ---
                if not all(k in data for k in ['category', 'title', 'description', 'snippets']):
                    raise ValueError("JSON is missing required keys: category, title, description, or snippets.")

                # Get or create the category
                category, _ = Category.objects.get_or_create(name=data['category'])
                
                # Create the CheatSheet, setting author and status
                cheatsheet = CheatSheet.objects.create(
                    author=request.user,
                    category=category,
                    title=data['title'],
                    description=data['description'],
                    status='PENDING' # Explicitly set to PENDING for review
                )

                # Create the associated CodeSnippets
                for snippet_data in data['snippets']:
                    if not all(k in snippet_data for k in ['title', 'language', 'code']):
                        raise ValueError("A snippet is missing required keys: title, language, or code.")
                    
                    CodeSnippet.objects.create(
                        cheatsheet=cheatsheet,
                        title=snippet_data['title'],
                        language=snippet_data['language'],
                        code=snippet_data['code'],
                        output=snippet_data.get('output') # Safely get output
                    )
                
                messages.success(request, 'Thank you! Your JSON has been submitted for review.')
                return redirect('category_list')

            except json.JSONDecodeError:
                messages.error(request, 'Invalid JSON format. Please check your syntax.')
            except ValueError as e:
                messages.error(request, f'Invalid data structure: {e}')
            except Exception as e:
                messages.error(request, f'An unexpected error occurred: {e}')

    else:
        form = JSONContributionForm()

    context = {
        'form': form,
    }
    return render(request, 'core/contribute.html', context)


def about_page(request):
    """Renders the about page."""
    return render(request, 'core/about.html')


def under_development(request):
    return render(request, 'core/under_development.html')



def custom_page_not_found_view(request, exception):
    
    return render(request, "404.html", status=404)