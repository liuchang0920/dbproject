from django.conf.urls import url

from . import views

app_name = 'kickstar'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^register$', views.register, name='register'),
    url(r'^activity$', views.activity, name='activity'),
    url(r'^profile', views.profile, name='profile'),
]