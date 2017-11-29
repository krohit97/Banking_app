from ipware.ip import get_ip
from django.conf import settings
import os
import re
from django.shortcuts import render, redirect
# Create your views here.
from django.db import connection, transaction
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
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

# Create your views here.
def index(request):
    if request.method=='POST':
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

        cursor.execute("select password from manager where username= %s",[username])
        if(cursor.rowcount):
            pswdsql=cursor.fetchone()
            pswdsql=str(pswdsql[0])
            if(pswdsql==password):
                request.session['username'] = username
                request.session['type'] = 'manger'
                return redirect('/loggedin')
            else:
                return redirect('/home')
        else:
            return redirect('/home')
    else:
        form=UserCreationForm()
        ip = get_ip(request)
        path = settings.BASE_DIR
        os.chdir(path)
        with open("Logs.txt", "a") as myfile:
            myfile.write(ip)
            myfile.write("\n")
        args={'form':form}
        return render(request, 'manager_login/login_form.html')