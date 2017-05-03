from django.shortcuts import render, redirect, get_object_or_404
from .models import *
# from .forms import *
import datetime


def index(request):
    # fetch featured five projects
    newest_project = Projectpropose.objects.order_by('-pstarttime')[:5]
    popular_project = Projectpropose.objects.order_by('-pstarttime')[:5]
    print len(newest_project)

    return render(request, 'kickstar/index.html', {'newest_project': newest_project, 'popular_project': popular_project})


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
    user = User.objects.get(username = username)
    # user creditcard info
    creditcards = Usercreditcardinfo.objects.filter(user=user)
    print "credit card size:%d" % (len(creditcards))

    return render(request, 'kickstar/profile.html', {'user': user, 'creditcards': creditcards})


def project(request, pk):
    project = get_object_or_404(Projectpropose, pk=pk)
    project_updates = Projectupdate.objects.filter(project = project).order_by('-updatenumber')
    project_comments = Comment.objects.filter(project=project).order_by('-commenttime')

    return render(request, 'kickstar/project.html', {'project': project, 'project_updates': project_updates, 'project_comments': project_comments})


def back_project(request):
    projectname = request.POST.get("projectname")
    projectfunder = request.POST.get("projectfunder")
    projectid = request.POST.get("projectid")
    return render(request, 'kickstar/backproject.html', {'projectname':projectname, 'projectfunder': projectfunder, 'projectid': projectid})


def payment(request):
    # 'projectname':projectname, 'projectfunder': projectfunder, 'projectid': projectid
    projectname = request.POST.get("projectname")
    projectfunder = request.POST.get("projectfunder")
    projectid = request.POST.get("projectid")
    amount = request.POST.get("amount")
    # fetch creditcard info
    username = request.session.get("username")
    user = User.objects.get(username=username)
    creditcards = Usercreditcardinfo.objects.filter(user=user)
    return render(request, 'kickstar/payment.html', {'projectname': projectname, 'projectfunder': projectfunder,'projectid': projectid, 'amount': amount,'creditcards':creditcards})


def confirm_payment(request):
    return render(request, 'kickstar/confirmpayment.html', {'message':'sucessfully pledged.<br>you can check in pledge project page'})


def startproject(request):
    if request.method == "POST":
        #get field
        # error check

        # category = Category.objects.get(cname = request.POST["category"])
        try:
            pname = request.POST['pname']
            pdescription = request.POST['pdescription']
            minbudget = request.POST['minbudget']
            maxbudget = request.POST['maxbudget']
            pbackgroundpic = request.FILES['pbackgroundpic']
            pcontentdetail = request.POST['pcontentdetail']
                        #           if not pname or not pdescription or not minbudget or not maxbudget or not pbackgroundpic or not pcontentdetail:
        except:
            message = 'need to fill every field.'
            return render(request, 'kickstar/startproject.html', {'message': message})
        else:
            # save
            project_to_save = Projectpropose()
            project_to_save.category = Category.objects.get(pk=1)
            project_to_save.user = User.objects.get(username=request.session["username"])
            project_to_save.pname = pname
            project_to_save.pdescription = pdescription
            project_to_save.likecount = 0
            project_to_save.backcount = 0
            project_to_save.minbudget = minbudget
            project_to_save.maxbudget = maxbudget
            project_to_save.amountpledged = 0
            project_to_save.pstarttime = datetime.datetime.now()
            project_to_save.plancompletetime = datetime.datetime.now() # not sure format correct
            project_to_save.pstatus = "funding"
            project_to_save.pbackgroundpic = pbackgroundpic
            project_to_save.pcontentdetail = pcontentdetail
            project_to_save.save()
            message = 'successfully founded.'
            return render(request, 'kickstar/index.html', {'message': message})

    else:
        message = ''
        if not request.session.get("username"):
            message = 'you need to login first before start a project.'
            return render(request, 'kickstar/index.html', {'message': message})
        else:
            return render(request, 'kickstar/startproject.html')


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


def save_profile(request):
    return render(request, 'kickstar/test.html', {})


def project_comment(request):
    if request.method == 'POST':
        username = request.session['username']
        print username
        user = User.objects.get(username=username)
        content = request.POST.get("content")
        print content
        pk = request.POST["pk"]
        project = Projectpropose.objects.get(pk=pk)
        comment = Comment(project=project, username=user, content=content, commenttime=datetime.datetime.now())
        comment.save()
        #return render(request, 'kickstar/test.html', {})
        return redirect('kickstar:project', pk=pk)


def save_password(request):
    # check password correct or not
    username = request.session.get("username")
    originalpassword = request.POST.get("originalpassword")
    print originalpassword
    message = 'password successfully updated'
    try:
        user = User.objects.get(username=username)
        loginuser = Logon.objects.get(user=user, password=originalpassword)
        newpassword = request.POST.get("password")
        newpasswordR = request.POST.get("passwordR")

        if newpassword == newpasswordR:
            #update
            loginuser.password = newpassword
            loginuser.save()
        else:
            # error message
            message = "new password doesn't match"
    except:
        message = 'original password not correct'
    finally:
        username = request.session['username']
        user = User.objects.get(username=username)
        creditcards = Usercreditcardinfo.objects.filter(user=user)
        context = {'user': user, 'creditcards': creditcards}
        if message != '':
            context['message'] = message
        return render(request, 'kickstar/profile.html', context)


def save_creditcard_info(request):
    # create user
    username = request.session['username']
    user = User.objects.get(username=username)
    message = ''
    try:
        pk = request.POST['pk']
        cardnumber = request.POST['cardnumber']
        cardname = request.POST['cardname']
        validthrough = str(request.POST['validthrough'])
        print "valid: ", validthrough
        month = int(validthrough.split('/')[0])

        year = int(validthrough.split('/')[1])
        validdate = datetime.datetime(year, month, 1)
        print validthrough
        securitycode = request.POST['securitycode']

        if cardnumber == '' or cardname == '' or validthrough == '' or securitycode == '':
            message = 'all the fields must not be empty'

        if pk != 'newcard':
            # modification
            creditcarinfo = Usercreditcardinfo.objects.get(pk=pk)
            creditcarinfo.creditno = cardnumber
            creditcarinfo.creditname = cardname
            creditcarinfo.validdate = validdate  # date???
            creditcarinfo.securitycode = securitycode
            creditcarinfo.save()
            message = 'creditcard info updated successfully'
        else:
            creditcarinfo = Usercreditcardinfo()
            creditcarinfo.user = user
            creditcarinfo.creditno = cardnumber
            creditcarinfo.creditname = cardname
            creditcarinfo.validdate = validdate
            creditcarinfo.securitycode = securitycode
            creditcarinfo.save()
            message = 'creditcard info created successfully'
    except:
        message = 'error occurrd, do not leave blank'
    finally:
        creditcards = Usercreditcardinfo.objects.filter(user=user)
        context = {'user': user, 'creditcards': creditcards}
        if message != '':
            context['message'] = message
        return render(request, 'kickstar/profile.html', context)

