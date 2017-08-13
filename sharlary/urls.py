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
from django.contrib.auth.views import login, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='index'),
    url(r'^language/$', set_lang, name='set_lang'),
    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),
    url(r'^accounts/register/$', register, name='register'),
    url(r'^accounts/update/$', user_update, name='user_update'),
    url(r'^accounts/password_change/$', MyPasswordChangeView.as_view(), name='password_change'),
    url(r'^accounts/password_reset/$', PasswordResetView.as_view(template_name="registration/user_password_reset.html", email_template_name="components/user_password_reset_email.html", subject_template_name="components/user_password_reset_subject.txt"), name='password_reset'),
    url(r'^accounts/password_reset/done/$', PasswordResetDoneView.as_view(template_name="registration/user_password_reset_done.html"), name='password_reset_done'),
    url(r'^accounts/reset/done/$', PasswordResetCompleteView.as_view(template_name="registration/user_password_reset_complete.html"), name='password_reset_complete'),
    url(r'^accounts/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', PasswordResetConfirmView.as_view(template_name="registration/user_password_reset_confirm.html"), name='password_reset_confirm'),
    url(r'^company_info/(?P<company_id>[0-9]+)$', company_info, name='company_info'),
    url(r'^user_save_company/$', user_save_company, name='user_save_company'),
    url(r'^user_saved_list/$', user_saved_list, name='user_saved_list'),
    url(r'^add_company/$', add_company, name='add_company'),
    url(r'^search_company/$', search_company, name='search_company'),
    url(r'^share_salary/(?P<company_id>[0-9]+)$', share_salary, name='share_salary'),
    url(r'^user_salary/$', user_salary, name='user_salary'),
    url(r'^user_salary_update/(?P<salary_id>[0-9]+)$', user_salary_update, name='user_salary_update'),
]
