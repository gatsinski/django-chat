from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, LoginForm


def register_view(request):
    if not request.user.is_authenticated():
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('users:login'))
        else:
            form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})
    else:
        return HttpResponseRedirect(reverse('users:profile'))


def login_view(request):
    if not request.user.is_authenticated():
        if request.method == "POST":
            form = LoginForm(request.POST)
            user = authenticate(username=request.POST.get('username'),
                                password=request.POST.get('password'))
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('users:profile'))
        else:
            form = LoginForm()
        return render(request, 'users/login.html', {'form': form})
    return HttpResponseRedirect(reverse('users:profile'))


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))


@login_required
def profile_view(request):
    return render(request, 'users/profile.html')
