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


def project(request):
    return render(request, 'kickstar/project.html', {})


def back_project(request):
    return render(request, 'kickstar/backproject.html', {})


def payment(request):
    return render(request, 'kickstar/payment.html', {})


def startproject(request):
    return render(request, 'kickstar/startproject.html', {})


def updateproject(reqeust):
    return render(reqeust, 'kickstar/updateproject.html', {})

