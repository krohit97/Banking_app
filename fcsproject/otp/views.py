from django.shortcuts import render, HttpResponse, redirect
# Create your views here.
from django.db import connection, transaction
from django.contrib.auth.forms import UserCreationForm
import pyotp
import smtplib
from smtplib import SMTP

def index(request):
	if request.session.has_key('username'):
		if request.method=='POST':
			otpvar = request.session['otp']
			request.session.pop('otp',otpvar)
			form = UserCreationForm(request.POST)
			otp =request.POST.get('otp')
			if int(otp) == int(otpvar):
				return redirect('/loggedin')
			else:
				username = request.session['username']
				request.session.pop('username', username)
				type=request.session['type']
				request.session.pop('type', type)
				return redirect('/logout')
		else:
			form=UserCreationForm()
			args={'form':form}
			totp = pyotp.TOTP('base32secret3232')
			smtp = SMTP()
			smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
			smtpObj.ehlo()
			smtpObj.starttls()
			smtpObj.login('kumarfcs2@gmail.com', 'lostintheecho')
			username=request.session['username']
			cursor = connection.cursor()
			if(request.session['type']=='cust'):
				cursor.execute("select email from customer where user_name= %s",[username])
			if(request.session['type'] == 'emp'):
				cursor.execute("select email from employee where user_name= %s", [username])
			mailid=cursor.fetchone()
			mailid=str(mailid[0])
			otpvar=totp.now()
			request.session['otp']=str(otpvar)
			SUBJECT = "Bank OTP"
			TEXT = "Your one time password is: " + str(otpvar)
			# print TEXT
			message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
			# message = 'OTP is: ' + str(otpvar)
			smtpObj.sendmail("email", mailid, message)
			return render(request, 'otp/otp_verify.html')
	else:
		return redirect('/home')
