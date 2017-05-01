from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *


def index(request):
    # fetch featured five projects
    newest_project = Projectpropose.objects.order_by('-pstarttime')[:5]
    print len(newest_project)

    return render(request, 'kickstar/index.html', {'newest_project': newest_project})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print username, password
        if username == '' or password == '':
            message = "username or password cannot be empty"
            return render(request, 'kickstar/login.html', {'message': message})
        else:
            try:
                user = User.objects.get(username=username)
                login = Logon.objects.get(user=user, password=password)
                #put into session
                print "success"
                request.session["username"] = username
                message = "login Successful"
                return render(request, 'kickstar/index.html', {'message': message})
            except:
                message = "username or password wrong"
                return render(request, 'kickstar/login.html', {'message': message})

    else:
        print "get"
        return render(request, 'kickstar/login.html', {})


def logout(request):
    request.session["username"] = None
    message = "successfully logout"
    return render(request, 'kickstar/index.html', {'message': message})


def register(request):
    return render(request, 'kickstar/register.html', {})


def activity(request):
    return render(request, 'kickstar/activity.html', {})


# should be post
def profile(request):
    username = request.session['username']
    print username
    user = User.objects.get(username = username)

    return render(request, 'kickstar/profile.html', {'user': user})


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


def test(request):
    return render(request, 'kickstar/test.html', {"message":"this is a test"})


def search(request):
    return render(request, 'kickstar/test.html', {"message":"this is a test"})


def category(request):
    category = Category.objects.all()
    return render(request, 'kickstar/cateogry.html', {'category': category})


def category_detail(request, categoryid):
    category = get_object_or_404(Category, categoryid=categoryid)
    related_project = Projectpropose.objects.filter(category=category)
    return render(request, 'kickstar/cateogrydetail.html', {'related_project': related_project, 'category': category})


# def save_profile(request):
#     pass