"""sharlary URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from theme.views import *
from django.contrib.auth.views import login

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='index'),
    url(r'^language/$', set_lang, name='set_lang'),
    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),
    url(r'^accounts/register/$', register, name='register'),
    url(r'^accounts/update/$', user_update, name='user_update'),
    url(r'^company_info/(?P<company_id>[0-9]+)$', company_info, name='company_info'),
    url(r'^user_save_company/$', user_save_company, name='user_save_company'),
    url(r'^user_saved_list/$', user_saved_list, name='user_saved_list'),
    url(r'^add_company/$', add_company, name='add_company'),
]
