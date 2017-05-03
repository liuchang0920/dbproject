from django import forms
from ckeditor_uploader.fields import RichTextUploadingField


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class ProjectProposeForm(forms.Form):
    category = forms.CharField()
    pname = forms.CharField()
    pdescription = forms.CharField()
    # likecount = forms.IntegerField()
    # backcount = forms.IntegerField()
    minbudget = forms.DecimalField()
    maxbudget = forms.DecimalField()
    # amountpledged = forms.DecimalField()
    # pstarttime = forms.DateTimeField()
    plancompletetime = forms.CharField()
    # actualcompletetime = forms.DateTimeField()
    # pstatus = forms.CharField()
    pbackgroundpic = forms.ImageField()
    # pcontentdetail = forms.CharField()