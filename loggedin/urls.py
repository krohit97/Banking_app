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
from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index,name='index'),
    url(r'^cust_view$', views.cust_view),
    url(r'^cust_debit$', views.cust_debit),
    url(r'^cust_credit$', views.cust_credit),
    url(r'^cust_transfer$', views.cust_transfer),
    url(r'^cust_modify$', views.cust_modify),
    url(r'^cust_statement', views.cust_statement),
    url(r'^cust_add_account$', views.cust_add_account),
    url(r'^merch_view$', views.merch_view),
    url(r'^merch_debit$', views.merch_debit),
    url(r'^merch_credit$', views.merch_credit),
    url(r'^merch_transfer$', views.merch_transfer),
    url(r'^merch_modify$', views.merch_modify),
    url(r'^merch_add_account$', views.merch_add_account),
    url(r'^merch_decision$', views.merch_decision),
    url(r'^admin_view$', views.admin_view),
    url(r'^emp_view_transactions$', views.emp_view_transactions),
    url(r'^emp_decision$', views.emp_decision),
    url(r'^admin_add_emp_acc$', views.admin_add_emp_acc),
    url(r'^admin_mod_emp_acc$', views.admin_mod_emp_acc),
    url(r'^admin_del_emp_acc$', views.admin_del_emp_acc),
    url(r'^admin_view_emp_acc$', views.admin_view_emp_acc),
    url(r'^admin_access_log$', views.admin_access_log),
    url(r'^admin_add_cust_acc$', views.admin_add_cust_acc),
    url(r'^admin_mod_cust_acc$', views.admin_mod_cust_acc),
    url(r'^admin_del_cust_acc$', views.admin_del_cust_acc),
    url(r'^admin_view_cust_acc$', views.admin_view_cust_acc),
    url(r'^admin_grant_permit$', views.admin_grant_permit),
    url(r'^manager_view_transactions$', views.manager_view_transactions),
    url(r'^manager_decision$', views.manager_decision),
]
