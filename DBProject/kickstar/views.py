from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'kickstar/index.html', {})


def login(request):
    return render(request, 'kickstar/login.html', {})


def register(request):
    return render(request, 'kickstar/register.html', {})


def activity(request):
    return render(request, 'kickstar/activity.html', {})


# should be post
def profile(request):
    return render(request, 'kickstar/profile.html', {})