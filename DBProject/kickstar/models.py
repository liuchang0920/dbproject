from __future__ import unicode_literals
from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    categoryid = models.CharField( max_length=50)
    cname = models.CharField(max_length=50)
    cdescription = models.CharField(max_length=200)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.cname


class Comment(models.Model):
    project = models.ForeignKey('Projectpropose', on_delete=models.CASCADE)
    commenttime = models.DateTimeField()
    replyusername = models.ForeignKey('User', models.DO_NOTHING, db_column='replyusername', blank=True, null=True, related_name='%(class)s_requests_created')
    username = models.ForeignKey('User', models.DO_NOTHING, db_column='username')
    content = models.CharField(max_length=200)

    class Meta:
        db_table = 'comment'
        unique_together = (('project', 'commenttime', 'username'), )


class Follow(models.Model):
    followee = models.ForeignKey('User', on_delete=models.CASCADE, related_name='followee')
    follower = models.ForeignKey('User', on_delete=models.CASCADE, related_name='follower')

    class Meta:
        db_table = 'follow'
        unique_together = (('followee', 'follower'),)

    def __str__(self):
        return self.followee.username + " " + self.follower.username


class Logon(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    password = models.CharField(max_length=50)

    class Meta:
        db_table = 'logon'
        unique_together = (('user'),)

    def __str__(self):
        return self.user.username




class Projectlike(models.Model):
    project = models.ForeignKey('Projectpropose', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    value = models.IntegerField()

    class Meta:
        db_table = 'projectLike'
        unique_together = (('project', 'user'),)

    def __str__(self):
        return self.project.pname + ", " + self.user.username


class Projectpledge(models.Model):
    project = models.ForeignKey('Projectpropose', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    uciid = models.ForeignKey('Usercreditcardinfo',on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    pledgetime = models.DateTimeField()
    pledgestatus = models.CharField(max_length=10)

    class Meta:
        db_table = 'projectPledge'
        unique_together = (('project', 'user', 'pledgetime'),)

    def __str__(self):
        return self.user.username + " " + self.project.pname + " " + str(self.amount)


class Projectpropose(models.Model):
    # pid = models.CharField(primary_key=True, max_length=255)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    pname = models.CharField(max_length=50)
    pdescription = models.CharField(max_length=200, blank=True, null=True)
    likecount = models.IntegerField(blank=True, null=True)
    backcount = models.IntegerField(blank=True, null=True)
    minbudget = models.DecimalField(max_digits=10, decimal_places=0)
    maxbudget = models.DecimalField(max_digits=10, decimal_places=0)
    amountpledged = models.DecimalField(max_digits=10, decimal_places=0)
    pstarttime = models.DateTimeField()
    plancompletetime = models.DateTimeField()
    actualcompletetime = models.DateTimeField(blank=True, null=True)
    pstatus = models.CharField(max_length=10)
    pbackgroundpic = models.ImageField(upload_to='kickstar/images/', blank=True, null=True)
    pcontentdetail = RichTextField(blank=True, null=True)
    pmovieurl = models.CharField(max_length=200, blank=True, null=True)
    class Meta:
        db_table = 'projectPropose'

    def __str__(self):
        return self.pname


class Projectrate(models.Model):
    project = models.ForeignKey('Projectpropose', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    ratetime = models.DateTimeField()
    rate = models.IntegerField()

    class Meta:
        db_table = 'projectRate'
        unique_together = (('project', 'user'),)

    def __str__(self):
        return self.user.username + " " + self.project.pname + " " + str( self.rate)


class Projectsample(models.Model):
    project = models.ForeignKey('Projectpropose', on_delete=models.CASCADE)
    type = models.CharField(max_length=10)
    url = models.CharField(max_length=100)

    class Meta:
        db_table = 'projectSample'
        unique_together = (('project', 'url'),)

    def __str__(self):
        return self.project.pname+ "/"+ self.type + "/" + self.url


class Projectupdate(models.Model):
    project = models.ForeignKey('Projectpropose', on_delete=models.CASCADE)
    # updatenumber = models.IntegerField(blank=True, null=True)
    postdate = models.DateTimeField()
    title = models.CharField(max_length=50)
    body = models.CharField(max_length=500)

    class Meta:
        db_table = 'projectUpdate'
        unique_together = (('project', 'postdate'),)

    def __str__(self):
        return self.project.pname + " " + str(self.postdate)


class User(models.Model):
    username = models.CharField(primary_key=True, max_length=50)
    firstname = models.CharField(max_length=20, blank=True, null=True)
    lastname = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=20, blank=True, null=True)
    hometown = models.CharField(max_length=20, blank=True, null=True)
    interests = models.CharField(max_length=200, blank=True, null=True)
    registertime = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.username


class Usercreditcardinfo(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    creditname = models.CharField(max_length=50, blank=True, null=True)
    creditno = models.CharField(max_length=50)
    validdate = models.DateField()
    securitycode = models.CharField(max_length=10)

    class Meta:
        db_table = 'userCreditcardInfo'
        unique_together = (('user', 'creditno'),)

    def __str__(self):
        return self.user.username + " " + self.creditno