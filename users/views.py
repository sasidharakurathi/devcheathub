from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from core.models import CheatSheet
from django.core.paginator import Paginator

def register(request):
    
    if request.user.is_authenticated:
        return redirect("category_list")
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('category_list')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    cheatsheet_list = CheatSheet.objects.filter(author=request.user).order_by('-updated_at')
    
    paginator = Paginator(cheatsheet_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Prepare the query parameters here as well
    query_params = request.GET.copy()
    if 'page' in query_params:
        del query_params['page']
    
    context = {
        'page_obj': page_obj,
        'query_params': query_params.urlencode(), # Add this to context
    }
    return render(request, 'users/profile.html', context)