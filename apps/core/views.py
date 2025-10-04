from django.shortcuts import render

# Create your views here.
def home(request):
    """
    View function for the homepage.
    """
    return render(request, 'home.html')