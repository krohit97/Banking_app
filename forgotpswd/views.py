from django.shortcuts import render, HttpResponse, redirect
# Create your views here.
from django.db import connection, transaction
from django.contrib.auth.forms import UserCreationForm
import pyotp
import smtplib
from smtplib import SMTP
import string
import random

def index(request):
    if request.session.has_key('type'):
        if request.method=='POST':
            smtp = SMTP()
            smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login('kumarfcs2@gmail.com', 'lostintheecho')
            username=request.POST.get('uname')
            cursor = connection.cursor()
            if (request.session['type'] == 'cust'):
                cursor.execute("select email from customer where user_name= %s", [username])
            if (request.session['type'] == 'emp'):
                cursor.execute("select email from employee where user_name= %s", [username])
            if (request.session['type'] == 'merch'):
                cursor.execute("select email from customer where user_name= %s", [username])
            if (cursor.rowcount):
                mailid = cursor.fetchone()
                mailid = str(mailid[0])
            else:
                return redirect('/logout')
            SUBJECT = "New Password"
            chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
            size = random.randint(8, 12)
            new_pswd=''.join(random.choice(chars) for x in range(size))
            print new_pswd
            TEXT = "Your new password is: " + str(new_pswd)
            message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
            smtpObj.sendmail("email", mailid, message)
            if (request.session['type'] == 'cust'):
                cursor.execute('update customer set password = %s where user_name = %s',[new_pswd,username])
            elif (request.session['type'] == 'emp'):
                cursor.execute('update employee set password = %s where user_name = %s',[new_pswd,username])
            elif (request.session['type'] == 'merch'):
                    cursor.execute('update customer set password = %s where user_name = %s', [new_pswd, username])
            else:
                return redirect('/logout')
            return redirect('/logout')
        else:
            form=UserCreationForm()
            args={'form':form}
            return render(request, 'forgotpswd/enter_uname.html')
    else:
        return redirect('/logout')