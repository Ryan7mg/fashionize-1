from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserEditForm
from django.views.decorators.csrf import requires_csrf_token

@requires_csrf_token
def login_view(request):
    if request.method == 'POST':
        # TODO: change here when edit login html
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session.set_expiry(1209600)
            return redirect(f'/{user.username}/dashboard/')
        else:
            return render(request, 'account/login.html', {'error': 'Invalid username or password'})
    return render(request, 'account/login.html')


def signup_view(request):
    if request.method == 'POST':
        #TODO: change here when edit signup html
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            return render(request, 'account/signup.html', {'error': 'Username already exists'})
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect(f'/{user.username}/dashboard/')
    return render(request, 'account/signup.html')

def home_view(request):
    return render(request, 'account/home.html')
@login_required
def manage_account(request, username):
    if request.user.username != username:
        return redirect('some_error_page')

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect(f'/{request.user.username}/myaccount/')
    else:
        form = UserEditForm(instance=request.user)

    return render(request, 'account/manage_account.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')

