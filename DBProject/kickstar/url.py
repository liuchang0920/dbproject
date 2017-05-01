from django.conf.urls import url

from . import views

app_name = 'kickstar'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^register$', views.register, name='register'),
    url(r'^activity$', views.activity, name='activity'),
    url(r'^profile', views.profile, name='profile'),
    url(r'^project', views.project, name='project'),
    url(r'^backproject', views.back_project, name='backproject'),
    url(r'^payment', views.payment, name='payment'),
    url(r'^startproject', views.startproject, name='startproject'),
    url(r'^updateproject', views.updateproject, name='updateproject'),
    url(r'^test/', views.test, name='test'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^category/$', views.category, name='category'),
    url(r'^category/(?P<categoryid>[a-zA-Z0-9]+)/$', views.category_detail, name='categorydetail'),
]