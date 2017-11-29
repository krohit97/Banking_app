from django.shortcuts import render, HttpResponse, redirect
# Create your views here.
from django.db import connection, transaction
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def index(request):
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        cursor = connection.cursor()
        fname =request.POST.get('fname')
        lname =request.POST.get('lname')
        street=request.POST.get('street')
        city =request.POST.get('city')
        state =request.POST.get('state')
        pin =request.POST.get('pin')
        gender =request.POST.get('gender')
        email =request.POST.get('email')
        contact =request.POST.get('contact')
        dob =request.POST.get('dob')
        username =request.POST.get('uname')
        password =request.POST.get('pswd')
        query="INSERT INTO employee(first_name, last_name,street, city, state, pin,gender, email, contact,dob, user_name, password) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(fname,lname,street,city,state,pin,gender,email,contact,dob,username,password)
        cursor.execute(query)
        return redirect('/home')
    else:
        form=UserCreationForm()
        args={'form':form}
        return render(request, 'emp_reg/reg_form.html')