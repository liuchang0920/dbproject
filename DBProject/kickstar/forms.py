from django import forms
from ckeditor_uploader.fields import RichTextUploadingField


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class ProjectProposeForm(forms.Form):
    category = forms.CharField()
    pname = forms.CharField()
    pdescription = forms.CharField()
    minbudget = forms.DecimalField()
    maxbudget = forms.DecimalField()
    plancompletetime = forms.CharField()
    pbackgroundpic = forms.ImageField()
