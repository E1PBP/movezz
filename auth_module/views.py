from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import LoginForm, RegisterForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def login_view(request):
    """This view handles user login.
    If the user is already authenticated, they are redirected to the main view.
    If the request method is POST, it processes the login form.
    If the form is valid, the user is logged in and redirected to the main view.
    If the request method is GET, it displays an empty login form.
    
    Returns:
        HttpResponse : Rendered registration page or redirect to main view.
    """
    if request.user.is_authenticated:
        return redirect('feeds_module:main_view')
    if request.method == "POST":
        form = LoginForm(data=request.POST or None)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('feeds_module:main_view')

    else:
        form = LoginForm()
    context = {
        'form': form,
    }
    return render(request, 'login.html', context)

def register_view(request):
    """ This view handles user registration.
    If the user is already authenticated, they are redirected to the main view.
    If the request method is POST, it processes the registration form.
    If the form is valid, a new user is created, logged in, and redirected to the main view.
    If the request method is GET, it displays an empty registration form.
    Args:
        request : Django HttpRequest object.
    Returns:
        HttpResponse : Rendered registration page or redirect to main view.
    
    """
    if request.user.is_authenticated:
        return redirect('feeds_module:main_view')
    if request.method == "POST":
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feeds_module:main_view')

    else:
        form = RegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'register.html', context)

@login_required
def logout_user(request):
    """ This view handles user logout.
    It logs out the user and redirects them to the login page.
    Args:
        request : Django HttpRequest object.
    Returns:
        HttpResponse : Redirect to login page.
    """
    logout(request)
    return redirect("auth_module:login")