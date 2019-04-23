from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')


def login(request):
    if request.user.is_authenticated:
        messages.error(request, 'You are already loged in')
        return redirect('profile')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                messages.success(request, 'You are successfuly loged in')

                return redirect('profile')
            else:
                messages.error(request, 'Invalid credentials')
                return redirect('login')
        else:
            return render(request, 'account/login.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'User is already taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(
                        request, 'Email is already being used')
                    return redirect('register')
                else:
                    user = User.objects.create_user(
                        username=username, email=email, password=password, first_name=first_name, last_name=last_name)
                    user.save()
                    messages.success(
                        request, 'You are now register and can login')
                    return redirect('login')
        else:
            messages.error(request, 'Password don\'t match')
            return redirect('register')

    else:
        return render(request, 'account/register.html')


# @login_required
def profile(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Login required')
        return redirect('login')
    else:
        return render(request, 'account/profile.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are successfuly loged out')
        return redirect('index')
# Create your views here.
