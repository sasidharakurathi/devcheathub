from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from core.models import CheatSheet
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User

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

def profile(request, username):
    
     # Get the user object for the profile being viewed
    profile_user = get_object_or_404(User, username=username)
    
    if not profile_user:
        redirect("/page-not-found")
    
    # Check if the person viewing the page is the owner of the profile
    is_own_profile = (request.user == profile_user)
    
    
    if request.method == 'POST' and is_own_profile:
        # Process submitted data
        u_form = UserUpdateForm(request.POST, instance=profile_user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile_user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile', username=profile_user.username) # Redirect to the same page
    else:
        # Display the current profile data
        u_form = UserUpdateForm(instance=profile_user)
        p_form = ProfileUpdateForm(instance=profile_user.profile)
        
    # Filter cheatsheets based on who is viewing the page
    if is_own_profile:
        # The owner sees all their submissions (pending, approved, etc.)
        user_cheatsheets = CheatSheet.objects.filter(author=profile_user).order_by('-updated_at')
    else:
        # Other users only see the 'APPROVED' submissions
        user_cheatsheets = CheatSheet.objects.filter(author=profile_user, status='APPROVED').order_by('-updated_at')

    
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
        'profile_user': profile_user,
        'is_own_profile': is_own_profile,
    }
    return render(request, 'users/profile.html', context)


def custom_page_not_found_view(request, exception):
    
    return render(request, "404.html", status=404)