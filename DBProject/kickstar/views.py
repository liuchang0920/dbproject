from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .models import *
# from .forms import *
from django.contrib import messages
import datetime


def index(request):
    # fetch featured five projects
    newest_project = Projectpropose.objects.order_by('-pstarttime')[:6]
    popular_project = Projectpropose.objects.order_by('-likecount')[:6]

    return render(request, 'kickstar/index.html', {'newest_project': newest_project, 'popular_project': popular_project})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print username, password
        if username == '' or password == '':
            message = "username or password cannot be empty"
            messages.add_message(request, messages.INFO, message)
            return render(request, 'kickstar/login.html')
        else:
            try:
                user = User.objects.get(username=username)
                login = Logon.objects.get(user=user, password=password)
                #put into session
                print "success"
                request.session["username"] = username
                request.session['user'] = user
                message = "successfully login"
                messages.add_message(request, messages.INFO, message)
                return redirect("kickstar:index")
            except:
                message = "username or password wrong"
                messages.add_message(request, messages.INFO, message)
                return render(request, 'kickstar/login.html', {'message': message})

    else:
        print "get"
        return render(request, 'kickstar/login.html', {})


def logout(request):
    request.session["username"] = None
    request.session["user"] = None
    message = "successfully logout"
    messages.add_message(request, messages.INFO, message)
    return redirect("kickstar:index")


def register(request):
    if request.method == 'POST':
        # get parameters

        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        username = request.POST.get("username")
        email = request.POST.get("email")
        hometown = request.POST.get("hometown")
        interests = request.POST.get("interests")
        password = request.POST.get("password")
        passwordR = request.POST.get("passwordR")
        message = ''
        if password != passwordR:
            message = 'two password not identical'
            messages.add_message(request, messages.INFO, message)
            return redirect('kickstar:register')
        elif firstname == '' or lastname == '' or username == '' or email == '' or hometown == '' or interests == '':
            message = 'all fields must be filled'
            messages.add_message(request, messages.INFO, message)
            return redirect('kickstar:register')
        else:
            try:
                email_exist = User.objects.filter(email=email)
                username_exist = User.objects.filter(username=username)
                if email_exist or username_exist:
                    print "exist result"
                    message = 'sorry, username or email already exists, please choose another'
                    messages.add_message(request, messages.INFO, message)
                    return redirect('kickstar:register')
                else:
                    #save info
                    user_to_save = User()
                    user_to_save.username = username
                    user_to_save.firstname = firstname
                    user_to_save.lastname = lastname
                    user_to_save.email = email
                    user_to_save.hometown = hometown
                    user_to_save.interests = interests
                    user_to_save.registertime = datetime.datetime.now()
                    user_to_save.save()
                    login_to_save = Logon()
                    login_to_save.user = user_to_save
                    login_to_save.password = password
                    login_to_save.save()
                    request.session["user"] = user_to_save
                    message = 'user created successfully'
                    messages.add_message(request, messages.INFO, message)
                    return redirect('kickstar:index')
            except:
                message = 'unexpected error'
                messages.add_message(request, messages.INFO, message)
                return redirect('kickstar:index')
    else:
        return render(request, 'kickstar/register.html', {})


def activity(request):
    return render(request, 'kickstar/activity.html', {})


def profile(request):
    user = request.session.get("user")
    # user creditcard info
    creditcards = Usercreditcardinfo.objects.filter(user=user)
    # check follow info
    followers = Follow.objects.filter(followee=user)
    # check following
    following = Follow.objects.filter(follower=user)
    return render(request, 'kickstar/profile.html', {'user': user, 'creditcards': creditcards, 'followers': followers, 'following': following})


def project(request, pk):
    project = get_object_or_404(Projectpropose, pk=pk)
    project_updates = Projectupdate.objects.filter(project = project).order_by('-postdate')
    project_comments = Comment.objects.filter(project=project).order_by('-commenttime')
    like_project = False
    pledge_project = False

    if request.session["user"]:
        like = Projectlike.objects.filter(project=project, user=request.session["user"])
        if like and like[0].value == 1:
            like_project = True

    if Projectpledge.objects.filter(project=project, user=request.session["user"]):
        pledge_project = True

    is_rate_project = False
    try:
        rate_project = Projectrate.objects.filter(project=project, user=request.session["user"])
        is_rate_project = True
    except:
        pass
    print "like project:", like_project
    context = {'project': project, 'project_updates': project_updates, 'project_comments': project_comments, 'likeproject': like_project, 'pledge_project': pledge_project}

    # if is_rate_project:
    #     context["rate_project"] = rate_project
    if len(rate_project)>0:
        print "exsit rating"
        context["rate_project"] = rate_project[0]
    return render(request, 'kickstar/project.html', context)


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
    user = request.session["user"]
    creditcards = Usercreditcardinfo.objects.filter(user=user)
    return render(request, 'kickstar/payment.html', {'projectname': projectname, 'projectfunder': projectfunder,'projectid': projectid, 'amount': amount,'creditcards':creditcards})


def confirm_payment(request, status):
    print status
    pk = request.POST.get("pk")
    user = request.session.get("user")
    creditno = request.POST.get("creditno")
    print "creditnumber:", creditno
    creditcard_info = Usercreditcardinfo()
    if status == "exist":
        creditcard_info = Usercreditcardinfo.objects.get(creditno=creditno, user=user)
    else:
        creditname = request.POST["creditname"]
        validdate_str = request.POST["validdate"].split("/")
        print validdate_str
        validdate = datetime.date(year=int(validdate_str[1]), month=int(validdate_str[0]), day=1)
        securitycode = request.POST["securitycode"]
        creditcard_info = Usercreditcardinfo()
        creditcard_info.user = user
        creditcard_info.creditno = creditno
        creditcard_info.creditname = creditname
        creditcard_info.securitycode = securitycode
        creditcard_info.validdate = validdate
        creditcard_info.save()
        print "save new card"

    amount = request.POST["amount"]
    pledge = Projectpledge()
    project = Projectpropose.objects.get(pk=pk)
    pledge.project = project
    pledge.uciid = creditcard_info
    pledge.user = user
    pledge.amount = amount
    pledge.pledgetime = datetime.datetime.now()
    pledge.pledgestatus = 'pending'
    previous_pledge = Projectpledge.objects.filter(project=project, user=user)
    if not previous_pledge:
        project.backcount += 1
        project.save()

    pledge.save()
    import decimal
    project.amountpledged += decimal.Decimal(float(amount))
    project.save()
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
            print "get everhting except category"
            category = Category.objects.get(categoryid=request.POST["category"])
        except:
            message = 'need to fill every field.'
            category = Category.objects.all()
            return render(request, 'kickstar/startproject.html', {'message': message, 'category':category})
        else:
            # save
            project_to_save = Projectpropose()
            project_to_save.category = category
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
            message = 'project successfully founded.'
            messages.add_message(request, messages.INFO, message)
            redirecturl = 'kickstar:project'
            return redirect(redirecturl, pk=project_to_save.pk)

    else:
        message = ''
        if not request.session.get("username"):
            message = 'you need to login first before start a project.'
            messages.add_message(request, messages.INFO, message)
            return redirect("kickstar:index")
        else:
            # category information
            category = Category.objects.all()
            return render(request, 'kickstar/startproject.html',{'category':category})


def update_project(request):
    pk = request.POST.get("pk")
    title = request.POST.get("title")
    content = request.POST.get("content")
    if title == '' or content == '':
        messages.add_message(request, messages.INFO, 'all fields must be filled')
    else:
        project = Projectpropose.objects.get(pk=pk)
        update = Projectupdate()
        update.project = project
        update.postdate = datetime.datetime.now()
        update.title = title
        update.body = content
        update.save()
        messages.add_message(request, messages.INFO, 'update successfully')
    return redirect('kickstar:project', pk=pk)


def test(request):
    return render(request, 'kickstar/test.html', {"message":"this is a test"})


# def search(request):
#     return render(request, 'kickstar/test.html', {"message":"this is a test"})


def category(request):
    category = Category.objects.all()
    return render(request, 'kickstar/cateogry.html', {'category': category})


def category_detail(request, categoryid):
    category = get_object_or_404(Category, categoryid=categoryid)
    related_project = Projectpropose.objects.filter(category=category)
    return render(request, 'kickstar/cateogrydetail.html', {'related_project': related_project, 'category': category})


def save_profile(request):
    email = request.POST.get('email')
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    hometown = request.POST['hometown']
    interests = request.POST['interests']
    user = request.session.get("user")
    message = 'update succesfully'

    if email != '' and firstname != '' and lastname != '' and hometown != '' and interests != '':
        user.email = email
        user.firstname = firstname
        user.lastname = lastname
        user.hometown = hometown
        user.interests = interests
        user.save()
        request.session["user"] = user
    else:
        message = 'input fields cannot be empty'
    messages.add_message(request, messages.INFO, message)
    creditcards = Usercreditcardinfo.objects.filter(user=user)
    return redirect("kickstar:profile")


def project_comment(request):
    if request.method == 'POST':
        # username = request.session['username']
        # print username
        user = request.session.get("user")
        content = request.POST.get("content")
        print content
        pk = request.POST["pk"]
        project = Projectpropose.objects.get(pk=pk)
        comment = Comment(project=project, username=user, content=content, commenttime=datetime.datetime.now())
        comment.save()
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
        messages.add_message(request, messages.INFO, message)
        username = request.session['username']
        user = User.objects.get(username=username)
        return redirect("kickstar:profile")


def save_creditcard_info(request):
    # create user
    user = request.session['user']
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
        messages.add_message(request, messages.INFO, message)
        return redirect("kickstar:profile")


def project_like(request, pk, value):
    if not request.session['user']:
        message = 'you need to login first before like a project.'
        messages.add_message(request, messages.INFO, message)

        return redirect("kickstar:project", pk=pk)
    else:
        # save info and dispatch to project page
        user = request.session["user"]
        project = Projectpropose.objects.get(pk=pk)
        projectlike = Projectlike.objects.filter(user=request.session['user'], project=project)
        if projectlike:
            to_modify = projectlike
            to_modify.update(value=value)
            if value == "1":
                project.likecount += 1
                project.save()
            else:
                project.likecount -= 1
                project.save()
        else:
            #new record
            projectlike = Projectlike()
            projectlike.user = user
            projectlike.project = project
            projectlike.value = value
            projectlike.save()
            project.likecount += 1
            project.save()
        print "value: ", value
        if value == "1":
            messages.add_message(request, messages.INFO, 'liked this project')
        else:
            messages.add_message(request, messages.INFO, 'disliked this project')
        return redirect('kickstar:project', pk=pk)


def search(request):
    keyword = request.POST.get("keyword")
    project_name = Projectpropose.objects.filter(pname__icontains=keyword)
    project_desciption = Projectpropose.objects.filter(pdescription__icontains=keyword)
    searchresult = project_name | project_desciption
    searchresult = searchresult.distinct().order_by('-pstarttime')
    return render(request, 'kickstar/search.html',{'searchresult': searchresult})


def rate_project(request):
    rate = request.POST.get("rate")
    pk = request.POST.get("pk")
    project = Projectpropose.objects.get(pk=pk)
    projectrate = Projectrate()
    projectrate.user = request.session["user"]
    projectrate.project = project
    projectrate.rate = rate
    projectrate.ratetime = datetime.datetime.now()
    projectrate.save()

    messages.add_message(request, messages.INFO, 'rate successfully')
    return redirect('kickstar:project', pk=pk)


def follow(request,  followeeusername):
    following_user = User.objects.get(username=followeeusername)
    message = 'follow successful'
    try:
        follow = Follow.objects.get(followee=following_user, follower=request.session["user"])
        message = 'already followed'
    except:
        new_follow = Follow()
        new_follow.followee = following_user
        new_follow.follower = request.session["user"]
        new_follow.save()

    messages.add_message(request, messages.INFO, message)
    return redirect('kickstar:profile')


def unfollow(request, followingusername):
    following_user = User.objects.get(username=followingusername)
    follow = Follow.objects.get(followee=following_user, follower=request.session["user"])
    follow.delete()
    message = 'unfollow successful'
    messages.add_message(request, messages.INFO, message)
    return redirect('kickstar:profile')