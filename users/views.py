from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from core.models import CheatSheet
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm

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
    if request.method == 'POST':
        # Process submitted data
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile') # Redirect to the same page
    else:
        # Display the current profile data
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    # We'll also keep the list of submissions from our last step
    user_cheatsheets = CheatSheet.objects.filter(author=request.user).order_by('-updated_at')
    
    paginator = Paginator(user_cheatsheets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    query_params = request.GET.copy()
    if 'page' in query_params:
        del query_params['page']
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'page_obj': page_obj,
        'query_params': query_params.urlencode(),
    }
    return render(request, 'users/profile.html', context)