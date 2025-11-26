from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import LoginForm, RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import json

from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
from django.contrib.auth import logout as auth_logout

logger = logging.getLogger(__name__)


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
        logger.info(f"User {request.user.username} is already authenticated, redirecting to main view.")
        return redirect('feeds_module:main_view')
    if request.method == "POST":
        form = LoginForm(data=request.POST or None)
        if form.is_valid():
            user = form.get_user()
            logger.info(f"User {user.username} logged in successfully.")
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
        logger.info(f"User {request.user.username} is already authenticated, redirecting to main view.")
        return redirect('feeds_module:main_view')
    if request.method == "POST":
        
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            logger.info(f"New user {form.cleaned_data.get('username')} registered successfully.")
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
    logger.info(f"User {request.user.username} is logging out.")
    logout(request)
    return redirect("auth_module:login")



@csrf_exempt
def logout_api(request):
    """ This view handles user logout for API requests.
    Args:
        request : Django HttpRequest object.
    Returns:
        JsonResponse : JSON response indicating logout status.
    """
    username = request.user.username
    try:
        auth_logout(request)
        logger.info(f"User {username} logged out successfully.")
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logged out successfully!"
        }, status=200)
    except Exception as e:
        logger.error(f"Logout failed for user {username}: {e}")
        return JsonResponse({
            "status": False,
            "message": "Logout failed."
        }, status=401)
        
        
@csrf_exempt
def login_api(request):
    """ This view handles user login for API requests.
    Args:
        request: Django HttpRequest object.
    Returns:
        JsonResponse: JSON response indicating login status.
    """
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            # Login status successful.
            return JsonResponse({
                "username": user.username,
                "status": True,
                "message": "Login successful!"
                # Add other data if you want to send data to Flutter.
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login failed, account is disabled."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login failed, please check your username or password."
        }, status=401)
        
        
@csrf_exempt
def register_api(request):
    """ This view handles user registration for API requests.
    Args:
        request: Django HttpRequest object.
    Returns:
        JsonResponse: JSON response indicating registration status.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password1 = data['password1']
        password2 = data['password2']

        # Check if the passwords match
        if password1 != password2:
            logger.warning(f"Password mismatch for username: {username}")
            return JsonResponse({
                "status": False,
                "message": "Passwords do not match."
            }, status=400)
            
        
        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            logger.warning(f"Attempt to register with existing username: {username}")
            return JsonResponse({
                "status": False,
                "message": "Username already exists."
            }, status=400)
            
        
        # Create the new user
        user = User.objects.create_user(username=username, password=password1)
        user.save()
        logger.info(f"New user registered successfully: {username}")
        auth_login(request, user)
        
        return JsonResponse({
            "username": user.username,
            "status": 'success',
            "message": "User created successfully!"
        }, status=200)
    
    else:
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=400)

