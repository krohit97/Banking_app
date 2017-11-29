"""fcsproject URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from . import  views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^home/', include('home.urls')),
    url(r'^emp_reg/', include('emp_reg.urls')),
    url(r'^emp_login/', include('emp_login.urls')),
    url(r'^cust_reg/', include('cust_reg.urls')),
    url(r'^cust_login/', include('cust_login.urls')),
    url(r'^loggedin/', include('loggedin.urls')),
    url(r'^logout/', include('logout.urls')),
    url(r'^admin_reg/', include('admin_reg.urls')),
    url(r'^admin_login/', include('admin_login.urls')),
    url(r'^manager_reg/', include('manager_reg.urls')),
    url(r'^manager_login/', include('manager_login.urls')),
    url(r'^otp/', include('otp.urls')),

]
