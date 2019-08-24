#/usr/local/lib/python3.6/site-packages/
"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from myapp import views as my_views
from django.views.generic import TemplateView

#from . import views

urlpatterns = [
#    url(r'^$', my_views.index, name='index'),
    url(r'^form/$', my_views.form, name='form'),
    url(r'^adduser/$', my_views.adduser, name='adduser'),
    url(r'^signup/$', my_views.signup, name='signup'),
    url(r'^create/',TemplateView.as_view(template_name = 'myapp/signup.html')),
#    url(r'^$',TemplateView.as_view(template_name = 'myapp/index.html')),
    url(r'^$',my_views.sformView,name='index'),
    url(r'^login/',my_views.login,name = 'login'),
    url(r'^sent/',my_views.sent,name = 'sent'),
    url(r'^logout/',my_views.logout,name = 'logout'),
    url(r'^approval/',my_views.approval,name = 'approval'),
    url(r'^approved/',my_views.approved,name = 'approved'),
#    url(r'^message/',TemplateView.as_view(template_name = 'myapp/message.html')),
    url(r'^message/',my_views.Messagescls.messagemet,name = 'message'),
    url(r'^sendmessage/',my_views.Messagescls.sendmessage,name = 'sendmessage'),
    url(r'^delmesgs/',my_views.Messagescls.delmesgs,name = 'delmesgs'),
    url(r'^frndreq/',my_views.Messagescls.frndreq,name = 'frndreq'),
#    url(r'^contact/',my_views.myFirstChart,name = 'contact'),
]
