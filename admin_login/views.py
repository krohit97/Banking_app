from django.shortcuts import render, redirect
import re
# Create your views here.
from django.db import connection, transaction
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
# Create your views here.

def check_usename(text):
    if re.match(r'^\w+$', text) and len(text)<=18:
        return 1
    else:
        return 0

def check_password(text):
    if re.match(r'[A-Za-z0-9@#$*]{8,}', text) and len(text)<=28:
        return 1
    else:
        return 0


def index(request):
    if request.method=='POST':
        flag = 1
        form = UserCreationForm(request.POST)
        cursor = connection.cursor()
        username =request.POST.get('uname')
        flag = check_usename(username)
        if (flag == 0):
            return redirect('/logout')
        password =request.POST.get('pswd')
        flag = check_password(password)
        if (flag == 0):
            return redirect('/logout')
        cursor.execute("select password from admin where username= %s",[username])
        if(cursor.rowcount):
            pswdsql=cursor.fetchone()
            pswdsql=str(pswdsql[0])
            if(pswdsql==password):
                request.session['username'] = username
                request.session['type'] = 'admin'
                return redirect('/loggedin')
            else:
                return redirect('/home')
        else:
            return redirect('/home')
    else:
        form=UserCreationForm()
        args={'form':form}
        return render(request, 'admin_login/login_form.html')