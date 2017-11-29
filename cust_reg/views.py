import random
from django.shortcuts import render, HttpResponse, redirect
# Create your views here.
from django.db import connection, transaction
from django.contrib.auth.forms import UserCreationForm
import re
from ipware.ip import get_ip
from django.conf import settings
import os
def check_alphanum(text):
    if text.isalnum():
        return 1
    else:
        return 0

def check_dob(text):
    k = text.split("-")
    if len(k)==3:
        if int(k[0])<=2017 and int(k[1]) <=12 and int(k[2])<=31:
            return 1
    return 0

def check_usename(text):
    if re.match(r'^\w+$', text) and len(text)<=18:
        return 1
    else:
        return 0

def check_password(text):
    if re.match(r'[A-Za-z0-9@#$*]{8,}', text) and len(text)<=18:
        return 1
    else:
        return 0

def is_text(text):
    if text.isalpha():
        return 1
    else:
        return 0

# Create your views here.
def index(request):
    if request.method=='POST':
        print'0'
        flag = 1
        form = UserCreationForm(request.POST)
        cursor = connection.cursor()
        fname =request.POST.get('fname')
        print'1'
        flag = is_text(fname)
        if flag==0:
            return redirect('/logout')
        print'2'
        lname =request.POST.get('lname')
        flag = is_text(lname)
        if flag == 0:
            return redirect('/logout')
        street=request.POST.get('street')
        flag = check_alphanum(street)
        if flag ==0:
            return  redirect('/logout')
        print'3'
        city =request.POST.get('city')
        flag = is_text(city)
        if flag ==0:
            return redirect('/logout')

        state =request.POST.get('state')
        flag = is_text(state)
        if flag ==0:
            return redirect('/logout')
        print'4'
        pin =request.POST.get('pin')
        flag = check_alphanum(pin)
        if flag ==0:
            return redirect('/logout')
        print'5'
        gender =request.POST.get('gender')
        email =request.POST.get('email')
        contact =request.POST.get('contact')
        pan =request.POST.get('pan')
        entered_captcha=request.POST.get('captcha')
        session_captcha=request.session['captcha']
        flag = check_alphanum(pan)
        if flag == 0:
            return redirect('/logout')
        print'6'
        dob =request.POST.get('dob')
        flag = check_dob(dob)
        if flag == 0:
            return redirect('/logout')
        print'6.5'
        adhar =request.POST.get('adhar')
        username =request.POST.get('uname')
        flag = check_usename(username)
        if flag == 0:
            return redirect('/logout')
        print'7'
        password =request.POST.get('pswd')
        rpassword=request.POST.get('pswd_repeat')
        if(password!=rpassword):
            return redirect('/logout')
        print'8'
        flag = check_password(password)
        if flag == 0:
            return redirect('/logout')
        print'9'
        req_type = 'add'
        user_type = 'cust'
        try:
            cursor.execute("select cust_id from customer where user_name= %s",[username])
            if (cursor.rowcount):
                return redirect('/logout')
        except:
            pass
        if(int(entered_captcha)!=int(session_captcha)):
            return redirect('/logout')
        request.session.pop('captcha', session_captcha)
        query = "INSERT INTO admin_allow(first_name, last_name,street, city, state, pin,gender, email, contact,dob, user_name, password,user_type,request_type) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (fname, lname, street, city, state, pin, gender, email, contact, dob, username, password, user_type, req_type)
        cursor.execute(query)
        return redirect('/home')
    else:
        form=UserCreationForm()
        args={'form':form}
        ip = get_ip(request)
        path = settings.BASE_DIR
        os.chdir(path)
        with open("Logs.txt", "a") as myfile:
            myfile.write(ip)
            myfile.write("\n")
        captcha = random.randint(1111, 9999)
        request.session['captcha'] =captcha
        return render(request, 'cust_reg/reg_form.html',{'captcha':captcha})