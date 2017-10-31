from django.shortcuts import render, redirect
# Create your views here.
from django.db import connection, transaction
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
# Create your views here.
def index(request):
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        cursor = connection.cursor()
        username =request.POST.get('uname')
        password =request.POST.get('pswd')
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
        args={'form':form}
        return render(request, 'manager_login/login_form.html')