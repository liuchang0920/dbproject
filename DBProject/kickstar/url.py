from django.conf.urls import url

from . import views

app_name = 'kickstar'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^register$', views.register, name='register'),
    url(r'^activity$', views.activity, name='activity'),
    url(r'^profile', views.profile, name='profile'),
    url(r'^project/(?P<pk>[0-9]+)/$', views.project, name='project'),
    url(r'^backproject', views.back_project, name='backproject'),
    url(r'^payment', views.payment, name='payment'),
    url(r'^startproject', views.startproject, name='startproject'),
    url(r'^test/', views.test, name='test'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^category/$', views.category, name='category'),
    url(r'^category/(?P<categoryid>[a-zA-Z0-9]+)/$', views.category_detail, name='categorydetail'),
    url(r'^saveprofile/$', views.save_profile, name='saveprofile'),
    url(r'^projectcomment/&', views.project_comment, name='projectcomment'),
    url(r'^savepassword/$', views.save_password, name='savepassword'),
    url(r'^savecreditcard/$', views.save_creditcard_info, name='savecreditcard'),
    url(r'^confirmpayment/$', views.confirm_payment, name='confirmpayment'),
    url(r'^projectlike/(?P<pk>[0-9]+)/(?P<value>[0-9]+)/$', views.project_like, name="projectlike"),
    url(r'^search/$', views.search, name='search'),
    url(r'^rateproject/$', views.rate_project, name="rateproject"),
    url(r'^updateproject/$', views.update_project, name="updateproject"),
]