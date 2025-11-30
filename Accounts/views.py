from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserEditForm
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
User = get_user_model()
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .models import User
from schools.models import School
from django.http import JsonResponse


def user_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('Accounts:login')
        return view_func(request, *args, **kwargs)
    return wrapper

def public_profile_view(request, username):
    alumni = get_object_or_404(User, username=username)
    return render(request, "Accounts/profile_view.html", {"alumni": alumni})


def directory_view(request):
    query = request.GET.get("q")
    year = request.GET.get("year")
    alumni_list = User.objects.filter(school=request.user.school).order_by("last_name")

    if query:
        alumni_list = alumni_list.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(occupation__icontains=query)
        )

    if year:
        alumni_list = alumni_list.filter(graduation_year=year)

    return render(request, "Accounts/directory.html", {"alumni_list": alumni_list})


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('Accounts:profile')
    else:
        form = UserEditForm(instance=request.user)
    context = {
        "form": form,
        "username": request.user.username,
    }
    return render(request, 'Accounts/edit_profile.html', context)

def privacy(request):
    return render(request, 'Accounts/privacy.html')

@login_required
def download_data(request):
    user = request.user
    data = {
        "username": user.username,
        "email": user.email,
        "occupation": user.occupation,
        "bio": user.bio,
        "date_joined": user.date_joined,
        "last_login": user.last_login,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_active": user.is_active,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
        "school": user.school.name if user.school else None,
    }
    return JsonResponse(data)

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        gdpr_consent = request.POST.get('gdpr_consent')

        if not gdpr_consent:
            messages.error(request, "You must consent to proceed.")

        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect('Accounts:login')
        
    elif request.method == "GET":
        form = CustomUserCreationForm()
        
    return render(request, 'accounts/create_account.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('Main:homepage')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@user_login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('Accounts:login')


@user_login_required
def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('Accounts:login')
    return render(request, 'accounts/profile.html', {'user': request.user})