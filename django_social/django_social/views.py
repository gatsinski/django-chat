from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def home_page(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('users:profile'))
    else:
        return render(request, "django_social/home.html")