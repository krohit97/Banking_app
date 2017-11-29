from django.conf import settings
import os
from django.shortcuts import render, HttpResponse, redirect
# Create your views here.
from django.db import connection, transaction
from django.contrib.auth.forms import UserCreationForm
import datetime
import random
# Create your views here.
def index(request):
        if( request.session.has_key('username') and request.session.has_key('type')):
                user=request.session['username']
                user_type=request.session['type']
                if(user_type=='cust'):
                        return render(request, 'loggedin/customer_login.html')
                elif (user_type == 'merch'):
                        return render(request, 'loggedin/merchant_login.html')
                elif(user_type=='emp'):
                        return render(request, 'loggedin/employee_login.html')
                elif (user_type == 'manger'):
                        return render(request, 'loggedin/manager_login.html')
                elif (user_type == 'admin'):
                        return render(request, 'loggedin/admin_login.html')
                else:
                        return redirect('/logout')
        else:
                return redirect('/logout')


def cust_view(request):
        if request.session.has_key('username') and request.session['type']=='cust':
                user = request.session['username']
                cursor = connection.cursor()
                try:
                        cursor.execute("select cust_id from customer where user_name= %s", [user])
                except:
                        return redirect('/logout')
                cust_id=''
                if (cursor.rowcount):
                        cust_id = cursor.fetchone()
                        cust_id = str(cust_id[0])
                else:
                        return redirect('/logout')
                try:
                        cursor.execute("select * from customer where cust_id= %s", [cust_id])
                except:
                        return redirect('/logout')
                data_all=cursor.fetchall()
                data=[]
                for i in data_all:
                        data.append(i)
                fname = str(data[0][1])
                lname = str(data[0][2])
                street = str(data[0][3])
                city = str(data[0][4])
                state = str(data[0][5])
                pin = str(data[0][6])
                gender = str(data[0][7])
                email = str(data[0][8])
                pan = str(data[0][9])
                dob = str(data[0][10])
                user_name = str(data[0][11])
                password = str(data[0][12])
                contact  = str(data[0][13])
                adhar = str(data[0][14])
                s=''
                s=s+' Customer ID='+str(cust_id)+', First Name= '+str(fname)+', Last Name= '+str(lname)
                s=s+', Street='+str(street)+', City= '+str(city)+', State= '+str(state)
                s = s + ', Pin=' + str(pin) + ', Gender= ' + str(gender) + ', Email= ' + str(email)
                s = s + ', PAN=' + str(pan) + ', DOB= ' + str(dob) + ', User Name= ' + str(user_name)
                s = s + ', Password=' + str(password) + ', Contact= ' + str(contact) + ', Adhar= ' + str(adhar)
                s=s+'\n\n'
                try:
                        cursor.execute("select * from account where cust_id= %s", [cust_id])
                        data_all = cursor.fetchall()
                        data = []
                        for i in data_all:
                                data.append(i)
                        if (cursor.rowcount):
                                s = s + 'Account details:'
                                s = s + '\n\n'
                                for i in data:
                                        print i
                                        acno = str(i[0])
                                        balance = str(i[2])
                                        open_date = str(i[3])
                                        s = s + ' Account number=' + str(acno) + ', Balance= ' + str(balance) + ', Open Date= ' + str(open_date)
                                        s = s + '\n'
                except:
                        pass

                res = HttpResponse(s)
                res['Content-Disposition'] = 'attachment; filename=CustomerDetails.txt'
                return res
        else:
                return redirect('/logout')


def cust_debit(request):
        if request.session.has_key('username') and request.session['type']=='cust':
                if request.method == 'POST':
                        user = request.session['username']
                        cursor = connection.cursor()
                        password = request.POST.get('pswd')
                        ac_no = request.POST.get('acno')
                        bal = request.POST.get('balance')
                        if(bal<0):
                                return redirect('/loggedin')
                        try:
                                cursor.execute("select password from customer where user_name= %s", [user])
                        except:
                                return redirect('/logout')
                        pswdsql=''
                        if (cursor.rowcount):
                                pswdsql = cursor.fetchone()
                                pswdsql = str(pswdsql[0])
                        else:
                                return redirect('/logout')
                        if (pswdsql == password):
                                try:
                                        cursor.execute("select cust_id from customer where user_name= %s", [user])
                                except:
                                        return redirect('/logout')
                                cust_id=0
                                if (cursor.rowcount):
                                        cust_id = cursor.fetchone()
                                        cust_id = int(cust_id[0])
                                else:
                                        return redirect('/logout')
                                try:
                                        cursor.execute("select cust_id from account where ac_no= %s", [ac_no])
                                except:
                                        return redirect('/loggedin')
                                customer_id=0
                                if (cursor.rowcount):
                                        customer_id = cursor.fetchone()
                                        customer_id = int(customer_id[0])
                                else:
                                        return redirect('/loggedin')
                                if(customer_id==cust_id):
                                        try:
                                                cursor.execute("select balance from account where ac_no= %s", [ac_no])
                                        except:
                                                return redirect('/loggedin')
                                        balance=0
                                        if (cursor.rowcount):
                                                balance = cursor.fetchone()
                                                balance = int(balance[0])
                                        else:
                                                return redirect('/loggedin')
                                        if (int(balance) > int(bal)):
                                        # balance = int(balance)-int(bal)
                                        # values = []
                                        # values.append(user)
                                        # cursor.execute("update account set balance= %s where cust_id=%s", (balance,int(cust_id)))
                                        # cursor.execute("select balance from account where cust_id= %s", [cust_id])
                                        # balance = cursor.fetchone()
                                        # balance = int(balance[0])
                                        # values.append(balance)
                                                try:
                                                        cursor.execute("select ac_no from account where cust_id= %s", [cust_id])
                                                except:
                                                        return redirect('/loggedin')
                                                ac_from=0
                                                if (cursor.rowcount):
                                                        ac_from = cursor.fetchone()
                                                        ac_from = int(ac_from[0])
                                                else:
                                                        return redirect('/loggedin')
                                                all_emp_id = []
                                                trans_date = datetime.datetime.now()
                                                trans_type = 'debit'
                                                bal = int(bal)
                                                trans_date = datetime.datetime.now()
                                                trans_date=(str)(trans_date)
                                                trans_date=trans_date[:10]
                                                bal = int(bal)
                                                if (bal>20000):
                                                        try:
                                                                query = 'Select id from manager'
                                                        except:
                                                                return redirect('/loggedin')
                                                        cursor.execute(query)
                                                        manids=''
                                                        if (cursor.rowcount):
                                                                manids = cursor.fetchall()
                                                        else:
                                                                return redirect('/loggedin')
                                                        for i in manids:
                                                                all_emp_id.append(i[0])
                                                        man_id = random.choice(all_emp_id)
                                                        try:
                                                                query = "INSERT INTO manager_transfer(manager_id,trans_date,trans_type,amount,ac_from,ac_to) values ('%s','%s', '%s','%s','%s', '%s')" % (man_id, trans_date, trans_type, bal, ac_no, ac_no)
                                                        except:
                                                                return redirect('/loggedin')
                                                else:
                                                        try:
                                                                query = 'Select emp_id from employee'
                                                        except:
                                                                return redirect('/loggedin')
                                                        cursor.execute(query)
                                                        empids=''
                                                        if (cursor.rowcount):
                                                                empids = cursor.fetchall()
                                                        else:
                                                                return redirect('/loggedin')
                                                        for i in empids:
                                                                all_emp_id.append(i[0])
                                                        emp_id = random.choice(all_emp_id)
                                                        try:
                                                                query = "INSERT INTO emp_transfer(emp_id,trans_date,trans_type,amount,ac_from,ac_to) values ('%s','%s', '%s','%s','%s', '%s')" % (emp_id, trans_date,trans_type,bal,ac_no,ac_no)
                                                        except:
                                                                return redirect('/loggedin')
                                                cursor.execute(query)
                                                return render(request, 'loggedin/customer_login.html')
                                        else:
                                                form = UserCreationForm()
                                                args = {'form': form}
                                                return render(request, 'loggedin/customer_login.html')
                                else:
                                        form = UserCreationForm()
                                        args = {'form': form}
                                        return render(request, 'loggedin/customer_login.html')
                        else:
                                form = UserCreationForm()
                                args = {'form': form}
                                return render(request, 'loggedin/cust_debit.html')
                else:
                        form = UserCreationForm()
                        args = {'form': form}
                        return render(request, 'loggedin/cust_debit.html')
        else:
                return redirect('/logout')


def cust_credit(request):
        if request.session.has_key('username') and request.session['type']=='cust':
                if request.method == 'POST':
                        user = request.session['username']
                        cursor = connection.cursor()
                        password = request.POST.get('pswd')
                        bal = request.POST.get('balance')
                        if(bal<0):
                                return redirect('/loggedin')
                        ac_no=request.POST.get('acno')
                        try:
                                cursor.execute("select password from customer where user_name= %s", [user])
                        except:
                                return redirect('/loggedin')
                        pswdsql=''
                        if(cursor.rowcount):
                                pswdsql = cursor.fetchone()
                                pswdsql = str(pswdsql[0])
                        else:
                                return redirect('/loggedin')
                        if (pswdsql == password):
                                try:
                                        cursor.execute("select cust_id from customer where user_name= %s", [user])
                                except:
                                        return redirect('/logout')
                                cust_id=0
                                if (cursor.rowcount):
                                        cust_id = cursor.fetchone()
                                        cust_id = int(cust_id[0])
                                else:
                                        return redirect('/logout')
                                try:
                                        cursor.execute("select cust_id from account where ac_no= %s", [ac_no])
                                except:
                                        return redirect('/loggedin')
                                customer_id=0
                                if (cursor.rowcount):
                                        customer_id = cursor.fetchone()
                                        customer_id = int(customer_id[0])
                                else:
                                        return redirect('/loggedin')
                                if(customer_id==cust_id):
                                        all_emp_id = []
                                        trans_date = datetime.datetime.now()
                                        trans_date = (str)(trans_date)
                                        trans_date = trans_date[:10]
                                        trans_type = 'credit'
                                        bal = int(bal)
                                        query=''
                                        if (bal > 20000):
                                                try:
                                                        query = 'Select id from manager'
                                                except:
                                                        return redirect('/loggedin')
                                                cursor.execute(query)
                                                manids = ''
                                                if (cursor.rowcount):
                                                        manids = cursor.fetchall()
                                                else:
                                                        return redirect('/loggedin')
                                                for i in manids:
                                                        all_emp_id.append(i[0])
                                                man_id = random.choice(all_emp_id)
                                                try:
                                                        query = "INSERT INTO manager_transfer(manager_id,trans_date,trans_type,amount,ac_from,ac_to) values ('%s','%s', '%s','%s','%s', '%s')" % (man_id, trans_date, trans_type, bal, ac_no,ac_no)
                                                except:
                                                        return redirect('/loggedin')
                                        else:
                                                try:
                                                        query = 'Select emp_id from employee'
                                                except:
                                                        return redirect('/loggedin')
                                                cursor.execute(query)
                                                empids=''
                                                if (cursor.rowcount):
                                                        empids = cursor.fetchall()
                                                else:
                                                        return redirect('/loggedin')
                                                for i in empids:
                                                        all_emp_id.append(i[0])
                                                emp_id = random.choice(all_emp_id)
                                                try:
                                                        query = "INSERT INTO emp_transfer(emp_id,trans_date,trans_type,amount,ac_from,ac_to) values ('%s','%s', '%s','%s','%s', '%s')" % (emp_id, trans_date, trans_type, bal, ac_no, ac_no)
                                                except:
                                                        return redirect('/loggedin')
                                        try:
                                                cursor.execute(query)
                                        except:
                                                return render('/loggedin')
                                        return render(request, 'loggedin/customer_login.html')
                                else:
                                        return render('/logout')
                        else:
                                form = UserCreationForm()
                                args = {'form': form}
                                return render(request, 'loggedin/customer_login.html')
                else:
                        form = UserCreationForm()
                        args = {'form': form}
                        return render(request, 'loggedin/cust_credit.html')
        else:
                return redirect('/logout')


def cust_modify(request):
        if request.session.has_key('username') and request.session['type']=='cust':
                if request.method == 'POST':
                        user = request.session['username']
                        cursor = connection.cursor()
                        password = request.POST.get('opswd')
                        try:
                                cursor.execute("select password from customer where user_name= %s", [user])
                        except:
                                return redirect('/logout')
                        pswdsql = ''
                        if (cursor.rowcount):
                                pswdsql = cursor.fetchone()
                                pswdsql = str(pswdsql[0])
                        else:
                                return redirect('/logout')
                        try:
                                cursor.execute("select gender from customer where user_name= %s", [user])
                        except:
                                return redirect('/logout')
                        gender = ''
                        if (cursor.rowcount):
                                gender =cursor.fetchone()
                                gender = str(gender[0])
                        else:
                                return redirect('/logout')
                        if (pswdsql == password):
                                cust_id=''
                                try:
                                        cursor.execute("select cust_id from customer where user_name= %s", [user])
                                except:
                                        return redirect('/logout')
                                if (cursor.rowcount):
                                        cust_id = cursor.fetchone()
                                        cust_id = str(cust_id[0])
                                else:
                                        return redirect('/logout')
                                fname = request.POST.get('fname')
                                lname = request.POST.get('lname')
                                street = request.POST.get('street')
                                city = request.POST.get('city')
                                state = request.POST.get('state')
                                pin = request.POST.get('pin')
                                email = request.POST.get('email')
                                contact = request.POST.get('contact')
                                dob = request.POST.get('dob')
                                password = request.POST.get('pswd')
                                req_type = 'modify'
                                user_type = 'cust'
                                query = "INSERT INTO admin_allow(first_name, last_name,street, city, state, pin,gender, email, contact,dob, user_name, password,user_type,request_type) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (fname, lname, street, city, state, pin, gender, email, contact, dob, user, password,user_type, req_type)
                                try:
                                        cursor.execute(query)
                                except:
                                        return redirect('/loggedin')
                                return render(request, 'loggedin/customer_login.html')
                        else:
                                form = UserCreationForm()
                                args = {'form': form}
                                return render(request, 'loggedin/customer_login.html')
                else:
                        form = UserCreationForm()
                        args = {'form': form}
                        return render(request, 'loggedin/cust_modify.html')
        else:
                return redirect('/logout')


def cust_transfer(request):
        if request.session.has_key('username') and request.session['type']=='cust':
                if request.method == 'POST':
                        user = request.session['username']
                        cursor = connection.cursor()
                        password = request.POST.get('pswd')
                        accno = request.POST.get('accno')
                        bal = request.POST.get('balance')
                        if(bal<0):
                                return redirect('/loggedin')
                        ac_no = request.POST.get('acno')
                        try:
                                cursor.execute("select password from customer where user_name= %s", [user])
                        except:
                                return redirect('/logout')
                        pswdsql= ''
                        if (cursor.rowcount):
                                pswdsql = cursor.fetchone()
                                pswdsql = str(pswdsql[0])
                        else:
                                return redirect('/logout')
                        if (pswdsql == password):
                                try:
                                        cursor.execute("select cust_id from customer where user_name= %s", [user])
                                except:
                                        return redirect('/logout')
                                cust_id=0
                                if (cursor.rowcount):
                                        cust_id = cursor.fetchone()
                                        cust_id = int(cust_id[0])
                                else:
                                        return redirect('/logout')
                                try:
                                        cursor.execute("select cust_id from account where ac_no= %s", [ac_no])
                                except:
                                        return redirect('/loggedin')
                                customer_id=0
                                if (cursor.rowcount):
                                        customer_id = cursor.fetchone()
                                        customer_id = int(customer_id[0])
                                else:
                                        return redirect('/loggedin')
                                if(customer_id==cust_id):
                                        try:
                                                cursor.execute("select cust_id from customer where user_name= %s", [user])
                                        except:
                                                return redirect('/logout')
                                        cust_id= ''
                                        if (cursor.rowcount):
                                                cust_id = cursor.fetchone()
                                                cust_id = str(cust_id[0])
                                        else:
                                                return redirect('/logout')
                                        try:
                                                cursor.execute("select balance from account where cust_id= %s", [cust_id])
                                        except:
                                                return redirect('/loggedin')
                                        balance=0
                                        if (cursor.rowcount):
                                                balance = cursor.fetchone()
                                                balance = int(balance[0])
                                        else:
                                                return redirect('/loggedin')
                                        reciever_bal=-1
                                        try:
                                                cursor.execute("select balance from account where ac_no= %s", [accno])
                                                reciever_bal=cursor.fetchone()
                                                reciever_bal= int(reciever_bal[0])
                                        except:
                                                return redirect('/loggedin')
                                        if(int(balance)>=int(bal) and int(reciever_bal)>=0):

                                                try:
                                                        cursor.execute("select cust_id from customer where user_name= %s", [user])
                                                except:
                                                        return redirect('/logout')
                                                cust_id = ''
                                                if (cursor.rowcount):
                                                        cust_id = cursor.fetchone()
                                                        cust_id = str(cust_id[0])
                                                else:
                                                        return redirect('/logout')
                                                try:
                                                        cursor.execute("select ac_no from account where cust_id= %s", [cust_id])
                                                except:
                                                        return redirect('/logout')
                                                aac_from=0
                                                if (cursor.rowcount):
                                                        ac_from = cursor.fetchone()
                                                        ac_from = int(ac_from[0])
                                                else:
                                                        return redirect('/logout')
                                                ac_to = int(accno)
                                                all_emp_id = []
                                                trans_date = datetime.datetime.now()
                                                trans_date = (str)(trans_date)
                                                trans_date = trans_date[:10]
                                                trans_type = 'transfer'
                                                bal = int(bal)
                                                query=''
                                                if (bal > 20000):
                                                        query = 'Select id from manager'
                                                        try:
                                                                cursor.execute(query)
                                                        except:
                                                                return redirect('/loggedin')
                                                        manids=''
                                                        if (cursor.rowcount):
                                                                manids = cursor.fetchall()
                                                        else:
                                                                return redirect('/loggedin')
                                                        for i in manids:
                                                                all_emp_id.append(i[0])
                                                        man_id = random.choice(all_emp_id)
                                                        query = "INSERT INTO manager_transfer(manager_id,trans_date,trans_type,amount,ac_from,ac_to) values ('%s','%s', '%s','%s','%s', '%s')" % (man_id, trans_date, trans_type, bal, ac_no, ac_from)
                                                else:
                                                        query = 'Select emp_id from employee'
                                                        try:
                                                                cursor.execute(query)
                                                        except:
                                                                return redirect('/loggedin')
                                                        empids = ''
                                                        if (cursor.rowcount):
                                                                empids=cursor.fetchall()
                                                        else:
                                                                return redirect('/loggedin')
                                                        for i in empids:
                                                                all_emp_id.append(i[0])
                                                        emp_id=random.choice(all_emp_id)
                                                        query = "INSERT INTO emp_transfer(emp_id,trans_date,trans_type,amount,ac_from,ac_to) values ('%s','%s', '%s','%s','%s', '%s')" % (emp_id, trans_date, trans_type, bal, ac_no, ac_to)
                                                try:
                                                        cursor.execute(query)
                                                except:
                                                        return redirect('/loggedin')
                                                return render(request, 'loggedin/customer_login.html')
                                        else:
                                                form = UserCreationForm()
                                                args = {'form': form}
                                                return render(request, 'loggedin/customer_login.html')
                                else:
                                        return render('/logout')
                        else:
                                form = UserCreationForm()
                                args = {'form': form}
                                return render(request, 'loggedin/customer_login.html')
                else:
                        form = UserCreationForm()
                        args = {'form': form}
                        return render(request, 'loggedin/cust_transfer.html')
        else:
                return redirect('/logout')


def cust_add_account(request):
        if request.session.has_key('username') and request.session['type']=='cust':
                if request.method == 'POST':
                        user = request.session['username']
                        cursor = connection.cursor()
                        password = request.POST.get('pswd')
                        try:
                                cursor.execute("select password from customer where user_name= %s", [user])
                        except:
                                return redirect('/loggedin')
                        pswdsql= ''
                        if (cursor.rowcount):
                                pswdsql = cursor.fetchone()
                                pswdsql = str(pswdsql[0])
                        else:
                                return redirect('/loggedin')
                        if (pswdsql == password):
                                try:
                                        cursor.execute("select cust_id from customer where user_name= %s", [user])
                                except:
                                        return redirect('/logout')
                                cust_id= ''
                                if (cursor.rowcount):
                                        cust_id = cursor.fetchone()
                                        cust_id = str(cust_id[0])
                                else:
                                        return redirect('/logout')
                                balance = request.POST.get('balance')
                                if(balance<0):
                                        return redirect('/loggedin')
                                open_date=datetime.datetime.now()
                                query = "INSERT INTO account (cust_id,balance,open_date) values ('%s','%s', '%s')" % (cust_id,balance,open_date)
                                try:
                                        cursor.execute(query)
                                except:
                                        return redirect('/loggedin')
                                return render(request, 'loggedin/customer_login.html')
                        else:
                                form = UserCreationForm()
                                args = {'form': form}
                                return render(request, 'loggedin/customer_login.html')
                else:
                        form = UserCreationForm()
                        args = {'form': form}
                        return render(request, 'loggedin/cust_add_account.html')
        else:
                return redirect('/logout')

def cust_statement(request):
        if request.session.has_key('username') and request.session['type'] == 'cust':
                user = request.session['username']
                cursor = connection.cursor()
                try:
                        cursor.execute("select cust_id from customer where user_name= %s", [user])
                except:
                        return redirect('/logout')
                cust_id = ''
                if (cursor.rowcount):
                        cust_id = cursor.fetchone()
                        cust_id = str(cust_id[0])
                else:
                        return redirect('/logout')
                try:
                        cursor.execute("select balance from account where cust_id= %s", [cust_id])
                except:
                        return redirect('/loggedin')
                balance = cursor.fetchone()
                balance = int(balance[0])
                values = []
                values.append(user)
                values.append(balance)
                return render(request, 'loggedin/cust_view.html', {"values": values})
        else:
                return redirect('/logout')
def admin_view(request):
        if request.session.has_key('username') and request.session['type']=='admin':
                cursor = connection.cursor()
                print '1'
                try:
                        cursor.execute('select * from admin_allow')
                except:
                        return redirect('/loggedin')
                data=[]
                data_all = ''
                if (cursor.rowcount):
                        data_all=cursor.fetchall()
                else:
                        return redirect('/logout')
                for i in data_all:
                        data.append(i)
                s = ''
                for i in data:
                        req_id= str(i[0])
                        fname = str(i[1])
                        lname = str(i[2])
                        street = str(i[3])
                        city = str(i[4])
                        state = str(i[5])
                        pin = str(i[6])
                        gender = str(i[7])
                        email = str(i[10])
                        contact = str(i[11])
                        dob = str(i[12])
                        user_name = str(i[13])
                        password = str(i[14])
                        user_type= str(i[15])
                        req_type = str(i[16])
                        s = s+ 'Request Id= '+str(req_id)+', First Name= ' + str(fname) + ', Last Name= ' + str(lname)
                        s = s + ', Street=' + str(street) + ', City= ' + str(city) + ', State= ' + str(state)
                        s = s + ', Pin=' + str(pin) + ', Gender= ' + str(gender) + ', Email= ' + str(email)
                        s = s + ', DOB= ' + str(dob) + ', User Name= ' + str(user_name)
                        s = s + ', Password=' + str(password) + ', Contact= ' + str(contact) + ', State= ' + str(state)
                        s = s+ 'User type= ' + str(user_type) + ', Request type= ' + str(req_type)
                        s = s + '\n\n'
                res = HttpResponse(s)
                res['Content-Disposition'] = 'attachment; filename=User_Requests.txt'
                return res
        else:
                return redirect('/logout')

#admin allows an emp request to add
def admin_grant_permit(request):
        if request.session.has_key('username') and request.session['type'] == 'admin':
                if request.method == 'POST':
                        req_id = request.POST.get('req_id')
                        permit=request.POST.get('permit')
                        cursor = connection.cursor()
                        try:
                                cursor.execute('select request_type from admin_allow where req_id= %s', (req_id))
                        except:
                                return redirect('/loggedin')
                        req_type=''
                        if(cursor.rowcount):
                                req_type=cursor.fetchone()
                                req_type = str(req_type[0])
                        else:
                                return redirect('/loggedin')
                        try:
                                cursor.execute('select user_type from admin_allow where req_id= %s', (req_id))
                        except:
                                return redirect('/loggedin')
                        user_type=''
                        if (cursor.rowcount):
                                user_type= cursor.fetchone()
                                user_type= str(user_type[0])
                        else:
                                return redirect('/loggedin')
                        if(permit=='accept' and req_type=='add' and user_type=='emp'):
                                try:
                                        cursor.execute('select * from admin_allow where req_id= %s',(req_id))
                                except:
                                        return redirect('/loggedin')
                                data = []
                                data_all = cursor.fetchall()
                                for i in data_all:
                                        data.append(i)
                                fname=str(data[0][1])
                                lname =str(data[0][2])
                                street=str(data[0][3])
                                city=str(data[0][4])
                                state=str(data[0][5])
                                pin=str(data[0][6])
                                gender=str(data[0][7])
                                email= str(data[0][10])
                                contact=str(data[0][11])
                                dob=str(data[0][12])
                                user_name=str(data[0][13])
                                password=str(data[0][14])
                                try:
                                        cursor.execute("INSERT into employee(first_name, last_name,street, city, state, pin,gender, email, contact,dob, user_name, password) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(fname, lname, street, city, state, pin, gender, email, contact, dob, user_name, password))
                                        cursor.execute('Delete from admin_allow where req_id = %s', (req_id))
                                except:
                                        return redirect('/loggedin')
                        elif (permit == 'accept' and req_type == 'add' and user_type == 'cust'):
                                try:
                                        cursor.execute('select * from admin_allow where req_id= %s', (req_id))
                                except:
                                        return redirect('/loggedin')
                                data = []
                                data_all = cursor.fetchall()
                                for i in data_all:
                                        data.append(i)
                                fname = str(data[0][1])
                                lname = str(data[0][2])
                                street = str(data[0][3])
                                city = str(data[0][4])
                                state = str(data[0][5])
                                pin = str(data[0][6])
                                gender = str(data[0][7])
                                pan = str(data[0][8])
                                adhar = str(data[0][9])
                                email = str(data[0][10])
                                contact = str(data[0][11])
                                dob = str(data[0][12])
                                user_name = str(data[0][13])
                                password = str(data[0][14])
                                print '1'
                                try:
                                        cursor.execute(
                                                "INSERT into customer(first_name, last_name,street, city, state, pin,gender, email, contact,dob, user_name, password,adhar,pan) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                                                fname, lname, street, city, state, pin, gender, email, contact, dob,
                                                user_name, password,adhar,pan))
                                        #cursor.execute('Delete from admin_allow where req_id = %s', (req_id))
                                except:
                                        return redirect('/loggedin')
                        elif(permit=='reject'):
                                cursor = connection.cursor()
                                try:
                                        cursor.execute('Delete from admin_allow where req_id = %s',(req_id))
                                except:
                                        return redirect('/loggedin')
                        return render(request, 'loggedin/admin_login.html')
                else:
                        form = UserCreationForm()
                        args = {'form': form}
                        return render(request, 'loggedin/admin_grant_permit.html')
        else:
                return redirect('/logout')
#admin directly add a new emp
def admin_add_emp_acc(request):
        if request.session.has_key('username') and request.session['type'] == 'admin':
                if request.method == 'POST':
                        form = UserCreationForm(request.POST)
                        cursor = connection.cursor()
                        fname = request.POST.get('fname')
                        lname = request.POST.get('lname')
                        street = request.POST.get('street')
                        city = request.POST.get('city')
                        state = request.POST.get('state')
                        pin = request.POST.get('pin')
                        gender = request.POST.get('gender')
                        email = request.POST.get('email')
                        contact = request.POST.get('contact')
                        dob = request.POST.get('dob')
                        username = request.POST.get('uname')
                        password = request.POST.get('pswd')
                        query = "INSERT INTO employee (first_name, last_name,street, city, state, pin,gender, email, contact,dob, user_name, password) values ('%s','%s','%s','%s', '%s','%s', '%s','%s', '%s','%s', '%s','%s')" % (fname, lname, street, city, state, pin, gender, email, contact, dob, username,password)
                        try:
                                cursor.execute(query)
                        except:
                                return redirect('/loggedin')
                        return render(request, 'loggedin/admin_login.html')
                else:
                        form = UserCreationForm()
                        args = {'form': form}
                        return render(request, 'loggedin/admin_add_emp_acc.html')
        else:
                return redirect('/logout')

#admin directly modifies an emp account
def admin_mod_emp_acc(request):
        if request.session.has_key('username') and request.session['type'] == 'admin':
                if request.method == 'POST':
                        user = request.session['username']
                        cursor = connection.cursor()
                        fname = request.POST.get('fname')
                        lname = request.POST.get('lname')
                        street = request.POST.get('street')
                        city = request.POST.get('city')
                        state = request.POST.get('state')
                        pin = request.POST.get('pin')
                        gender = request.POST.get('gender')
                        email = request.POST.get('email')
                        contact = request.POST.get('contact')
                        dob = request.POST.get('dob')
                        username = request.POST.get('username')
                        try:
                                cursor.execute("update employee set first_name=%s,last_name=%s,street=%s,city=%s,state=%s,gender=%s,pin=%s,email=%s,dob=%s,contact=%s where user_name=%s",(fname, lname, street, city, state, gender, pin, email, dob, contact, username))
                        except:
                                return redirect('/loggedin')
                        return render(request, 'loggedin/admin_login.html')
                else:
                        form = UserCreationForm()
                        args = {'form': form}
                        return render(request, 'loggedin/admin_mod_emp_acc.html')
        else:
                return redirect('/logout')
def admin_del_emp_acc(request):
        if request.session.has_key('username') and request.session['type'] == 'admin':
                if request.method == 'POST':
                        cursor = connection.cursor()
                        emp_id=request.POST.get('emp_id')
                        try:
                                cursor.execute('select trans_id from emp_transfer where emp_id = %s', (emp_id))
                        except:
                                return redirect('/loggedin')
                        trans_ids=cursor.fetchall()
                        trans_id=[]
                        for i in trans_ids:
                                trans_id.append(i)
                        try:
                                for i in trans_id:
                                        cursor.execute('Delete from transfer_log where trans_id = %s', (i))
                                for i in trans_id:
                                        cursor.execute('Delete from emp_transfer where trans_id = %s', (i))
                                cursor.execute('Delete from employee where emp_id = %s', (emp_id))
                        except:
                                return redirect('/loggedin')
                        return render(request, 'loggedin/admin_login.html')
                else:
                        form = UserCreationForm()
                        args = {'form': form}
                        return render(request, 'loggedin/admin_del_emp_acc.html')
                return render(request, 'loggedin/admin_view.html', {"data": data})
        else:
                return redirect('/logout')
def admin_access_log(request):
        if request.session.has_key('username') and request.session['type'] == 'admin':
                path = settings.BASE_DIR
                os.chdir(path)
                log_file = open("Logs.txt", "r")
                data = log_file.read()
                res = HttpResponse(data)
                res['Content-Disposition'] = 'attachment; filename=LogFile.txt'
                return res
        else:
                return redirect('/logout')
def admin_add_cust_acc(request):
        if request.session.has_key('username') and request.session['type'] == 'admin':
                if request.method == 'POST':
                        form = UserCreationForm(request.POST)
                        cursor = connection.cursor()
                        fname = request.POST.get('fname')
                        lname = request.POST.get('lname')
                        street = request.POST.get('street')
                        city = request.POST.get('city')
                        state = request.POST.get('state')
                        pin = request.POST.get('pin')
                        gender = request.POST.get('gender')
                        email = request.POST.get('email')
                        contact = request.POST.get('contact')
                        pan = request.POST.get('pan')
                        adhar = request.POST.get('adhar')
                        dob = request.POST.get('dob')
                        username = request.POST.get('uname')
                        password = request.POST.get('pswd')
                        query = "INSERT INTO customer(first_name, last_name,street, city, state, pin,gender, email, contact,dob, user_name, password, pan, adhar) values ('%s','%s','%s','%s', '%s','%s', '%s','%s', '%s','%s', '%s','%s','%s','%s')" % (fname, lname, street, city, state, pin, gender, email, contact, dob, username, password,pan,adhar)
                        try:
                                cursor.execute(query)
                        except:
                                return redirect('/loggedin')
                else:
                        form = UserCreationForm()
                        args = {'form': form}
                        return render(request, 'loggedin/admin_add_cust_acc.html')
                return render(request, 'loggedin/admin_login.html')
        else:
                return redirect('/logout')


def admin_mod_cust_acc(request):
        if request.session.has_key('username') and request.session['type'] == 'admin':
                if request.method == 'POST':
                        req_id = request.POST.get('req_id')
                        permit = request.POST.get('permit')
                        cursor = connection.cursor()
                        try:
                                cursor.execute("select request_type from admin_allow where req_id= %s", [req_id])
                        except:
                                return redirect('/loggedin')
                        req_type=''
                        if (cursor.rowcount):
                                req_type = cursor.fetchone()
                                req_type = str(req_type[0])
                        else:
                                return redirect('/loggedin')
                        if (permit == 'accept' and req_type == 'modify'):
                                cursor = connection.cursor()
                                try:
                                        cursor.execute('select * from admin_allow where req_id= %s', (req_id))
                                except:
                                        return redirect('/loggedin')
                                data = []
                                data_all = cursor.fetchall()
                                for i in data_all:
                                        data.append(i)
                                fname = str(data[0][1])
                                lname = str(data[0][2])
                                street = str(data[0][3])
                                city = str(data[0][4])
                                state = str(data[0][5])
                                pin = str(data[0][6])
                                gender = str(data[0][7])
                                email = str(data[0][8])
                                contact = str(data[0][9])
                                dob = str(data[0][10])
                                user_name = str(data[0][11])
                                password = str(data[0][12])
                                try:
                                        cursor.execute("update customer set first_name=%s,last_name=%s,street=%s,city=%s,state=%s,gender=%s,pin=%s,email=%s,dob=%s,contact=%s,password=%s where user_name=%s",(fname, lname, street, city, state, gender, pin, email, dob, contact, password,user_name ))
                                        cursor.execute('Delete from admin_allow where req_id = %s', (req_id))
                                except:
                                        return redirect('/loggedin')
                        elif (permit == 'reject' and req_type == 'modify'):
                                cursor = connection.cursor()
                                try:
                                        cursor.execute('Delete from admin_allow where req_id = %s', (req_id))
                                except:
                                        return redirect('/loggedin')
                        return render(request, 'loggedin/admin_login.html')
                else:
                        form = UserCreationForm()
                        args = {'form': form}
                        return render(request, 'loggedin/admin_grant_permit.html')
        else:
                return redirect('/logout')


def admin_del_cust_acc(request):
        if request.session.has_key('username') and request.session['type'] == 'admin':
                if request.method == 'POST':
                        cursor = connection.cursor()
                        cust_id=request.POST.get('cust_id')
                        accnos=[]
                        try:
                                cursor.execute('select ac_no from account where cust_id = %s', (cust_id))
                        except:
                                return redirect('/loggedin')
                        accnos = cursor.fetchall()
                        acc_no= []
                        for i in accnos:
                                acc_no.append(i)
                        try:
                                for i in acc_no:
                                        cursor.execute('Delete from transfer_log where ac_from = %s', (i))
                                        cursor.execute('Delete from transfer_log where ac_to = %s', (i))
                                for i in acc_no:
                                        cursor.execute('Delete from emp_transfer where ac_from = %s', (i))
                                        cursor.execute('Delete from emp_transfer where ac_to = %s', (i))
                                for i in acc_no:
                                        cursor.execute('Delete from account where ac_no= %s', (i))
                                cursor.execute('Delete from customer where cust_id = %s', (cust_id))
                        except:
                                return redirect('/loggedin')
                        return render(request, 'loggedin/admin_login.html')
                else:
                        form = UserCreationForm()
                        args = {'form': form}
                        return render(request, 'loggedin/admin_del_cust_acc.html')
                return render(request, 'loggedin/admin_view.html', {"data": data})
        else:
                return redirect('/logout')

def admin_view_emp_acc(request):
        if request.session.has_key('username') and request.session['type'] == 'admin':
                cursor = connection.cursor()
                cursor.execute('select * from employee')
                data = []
                data_all=''
                if (cursor.rowcount):
                        data_all = cursor.fetchall()
                else:
                        return redirect('/loggedin')
                for i in data_all:
                        data.append(i)
                return render(request, 'loggedin/admin_view_emp_acc.html', {"data": data})
        else:
                return redirect('/logout')

def admin_view_cust_acc(request):
        if request.session.has_key('username') and request.session['type'] == 'admin':
                cursor = connection.cursor()
                cursor.execute('select * from customer')
                data = []
                data_all=''
                s=''
                if (cursor.rowcount):
                        data_all = cursor.fetchall()
                else:
                        return redirect('/loggedin')
                for i in data_all:
                        data.append(i)
                for i in data:
                        cust_id = str(data[i][0])
                        fname = str(data[i][1])
                        lname = str(data[i][2])
                        street = str(data[i][3])
                        city = str(data[i][4])
                        state = str(data[i][5])
                        pin = str(data[i][6])
                        gender = str(data[i][7])
                        email = str(data[i][8])
                        pan = str(data[i][9])
                        dob = str(data[i][10])
                        user_name = str(data[i][11])
                        contact = str(data[i][13])
                        adhar = str(data[i][14])
                        s = s+ ' Customer ID=' + str(cust_id) + ', First Name= ' + str(fname) + ', Last Name= ' + str(
                                lname)
                        s = s + ', Street=' + str(street) + ', City= ' + str(city) + ', State= ' + str(state)
                        s = s + ', Pin=' + str(pin) + ', Gender= ' + str(gender) + ', Email= ' + str(email)
                        s = s + ', PAN=' + str(pan) + ', DOB= ' + str(dob) + ', User Name= ' + str(user_name)
                        s = s + ', Contact= ' + str(contact) + ', Adhar= ' + str(adhar)
                        s = s + '\n\n'
                res = HttpResponse(s)
                res['Content-Disposition'] = 'attachment; filename=CustomerDetails.txt'
                return res
        else:
                return redirect('/logout')


def emp_view_transactions(request):
        if request.session.has_key('username') and request.session['type']=='emp':
                user = request.session['username']
                cursor = connection.cursor()
                try:
                        cursor.execute("select emp_id from employee where user_name= %s", [user])
                except:
                        return redirect('/loggedin')
                emp_id=''
                if (cursor.rowcount):
                        emp_id = cursor.fetchone()
                        emp_id = str(emp_id[0])
                else:
                        return redirect('/loggedin')
                try:
                        cursor.execute("select * from emp_transfer where emp_id= %s", [emp_id])
                except:
                        return redirect('/loggedin')
                data = []
                transaction_details=''
                if(cursor.rowcount):
                        transaction_details = cursor.fetchall()
                else:
                        return redirect('/loggedin')
                for i in transaction_details:
                        data.append(i)
                s=''
                for i in data:
                        trans_id = str(data[i][0])
                        emp_id = str(data[i][1])
                        trans_date= str(data[i][2])
                        trans_type= str(data[i][3])
                        amount= str(data[i][4])
                        ac_from= str(data[i][5])
                        ac_to= str(data[i][6])
                        s = s+' Transaction ID=' + str(trans_id) + ', Employee ID= ' + str(emp_id)
                        s = s + ', Transaction Date=' + str(trans_date) + ', Transaction type= ' + str(trans_type)
                        s = s + ', Amount=' + str(amount) + ', Account From= ' + str(ac_from) + ', Account To=  ' + str(ac_to)
                        s = s + '\n\n'
                res = HttpResponse(s)
                res['Content-Disposition'] = 'attachment; filename=EmployeeDetails.txt'
                return res
        else:
                return redirect('/logout')


def emp_decision(request):
        if request.session.has_key('username') and request.session['type']=='emp':
                if request.method == 'POST':
                        transid = request.POST.get('transid')
                        option = request.POST.get('decision')
                        cursor = connection.cursor()
                        if option == 'accept':

                                try:
                                        cursor.execute("update emp_transfer set approval = %s where trans_id= %s",('Yes', transid))
                                except:
                                        return redirect('/loggedin')
                                '''
                                data = []
                                data_all=''
                                if(cursor.rowcount):
                                        data_all = cursor.fetchall()
                                else:
                                        return redirect('/logout')
                                for i in data_all:
                                        data.append(i)
                                empid = str(data[0][1])
                                transdate = str(data[0][2])
                                transtype = str(data[0][3])
                                transamount = str(data[0][4])
                                trans_ac_from = str(data[0][5])
                                trans_ac_to = str(data[0][6])
                                # gender = str(data[0][7])
                                # email = str(data[0][8])
                                # contact = str(data[0][9])
                                # dob = str(data[0][10])
                                # user_name = str(data[0][11])
                                # password = str(data[0][12])


                                # cursor.execute("select emp_id from emp_transfer where trans_id= %s", [transid])
                                # empid = cursor.fetchone()
                                # empid = int(empid[0])

                                # cursor.execute("select trans_date from emp_transfer where trans_id= %s", [transid])
                                # transdate = cursor.fetchone()
                                # transdate = str(transdate[0])

                                # cursor.execute("select trans_type from emp_transfer where trans_id= %s", [transid])
                                # transtype = cursor.fetchone()
                                # transtype = str(transtype[0])

                                # print transtype

                                # cursor.execute("select amount from emp_transfer where trans_id= %s", [transid])
                                # transamount = cursor.fetchone()
                                # transamount = int(transamount[0])

                                # print transamount

                                # cursor.execute("select ac_from from emp_transfer where trans_id= %s", [transid])
                                # trans_ac_from = cursor.fetchone()
                                # trans_ac_from = int(trans_ac_from[0])

                                # cursor.execute("select ac_to from emp_transfer where trans_id= %s", [transid])
                                # trans_ac_to = cursor.fetchone()
                                # trans_ac_to = int(trans_ac_to[0])

                                if transtype == "debit":  ##subtract amount from balance
                                        try:
                                                cursor.execute("select balance from account where ac_no= %s", [trans_ac_from])
                                        except:
                                                return redirect('/logout')
                                        balance = cursor.fetchone()
                                        balance = int(balance[0])
                                        if transamount <= balance:
                                                try:
                                                        cursor.execute("update account set balance = %s where ac_no= %s",(balance - transamount, trans_ac_from))
                                                except:
                                                        return redirect('/logout')

                                elif transtype == "credit":
                                        try:
                                                cursor.execute("select balance from account where ac_no= %s", [trans_ac_from])
                                        except:
                                                return redirect('/logout')
                                        if(cursor.rowcount):
                                                balance = cursor.fetchone()
                                                balance = int(balance[0])
                                        else:
                                                return redirect('/employee_login')
                                        cursor.execute("update account set balance = %s where ac_no= %s",
                                                       [balance + transamount], [trans_ac_from])

                                elif transtype == "transfer":
                                        try:
                                                cursor.execute("select balance from account where ac_no= %s", [trans_ac_from])
                                        except:
                                                return redirect('/logout')
                                        if(cursor.rowcount):
                                                balance_from = cursor.fetchone()
                                                balance_from = int(balance_from[0])
                                        else:
                                                return redirect('/employee_login')
                                        try:
                                                cursor.execute("select balance from account where ac_no= %s", [trans_ac_to])
                                        except:
                                                return redirect('/logout')
                                        if(cursor.rowcount):
                                                balance_to = cursor.fetchone()
                                                balance_to = int(balance_to[0])
                                        else:
                                                return redirect('/employee_login')
                                        if transamount <= balance_from:
                                                try:
                                                        cursor.execute("update account set balance = %s where ac_no= %s",(balance_from - transamount,trans_ac_from))
                                                except:
                                                        return redirect('/logout')
                                                try:
                                                        cursor.execute("update account set balance = %s where ac_no= %s",(balance_to + transamount,trans_ac_to))
                                                except:
                                                        return redirect('/logout')
                                query = "INSERT INTO transfer_log (trans_id, trans_date, trans_type, amount, ac_from, ac_to, status,approved_by) values ('%s','%s', '%s','%s', '%s','%s', '%s', '%s')" % (
                                transid, transdate, transtype, transamount, trans_ac_from, trans_ac_to, 'accept','emp')
                                try:
                                        cursor.execute(query)
                                except:
                                        return redirect('/logout')
                                '''
                                return redirect('/loggedin/emp_decision')
                                #cursor.execute("delete from emp_transfer where trans_id= %s", [transid])

                        elif option == 'decline':
                                try:
                                        cursor.execute('select * from emp_transfer where trans_id= %s', [transid])
                                except:
                                        return redirect('/loggedin')
                                data = []
                                data_all = cursor.fetchall()
                                for i in data_all:
                                        data.append(i)
                                empid = str(data[0][1])
                                transdate = str(data[0][2])
                                transtype = str(data[0][3])
                                transamount = str(data[0][4])
                                trans_ac_from = str(data[0][5])
                                trans_ac_to = str(data[0][6])
                                cursor.execute("update emp_transfer set approval = %s where trans_id= %s",('No', transid))
                                query = "INSERT INTO transfer_log (trans_id, trans_date, trans_type, amount, ac_from, ac_to, status,approved_by) values ('%s','%s', '%s','%s', '%s','%s', '%s', '%s')" % (
                                        transid, transdate, transtype, transamount, trans_ac_from, trans_ac_to,
                                        'decline', 'emp')
                                try:
                                        cursor.execute(query)
                                except:
                                        return redirect('/loggedin')
                                return redirect('/loggedin/emp_decision')

                                #cursor.execute("delete from emp_transfer where trans_id= %s", [transid])
                        else:
                                return redirect('/loggedin/emp_decision')

                else:
                        form = UserCreationForm()
                        args = {'form': form}
                        return render(request, 'loggedin/emp_decision.html')

        else:
                return redirect('/logout')


def manager_view_transactions(request):
        if request.session.has_key('username') and request.session['type']=='manger':
                cursor=connection.cursor()
                try:
                        cursor.execute("select * from manager_transfer")
                except:
                        return redirect('/loggedin')
                data = []
                transaction_details=''
                if(cursor.rowcount):
                        transaction_details = cursor.fetchall()
                else:
                        return redirect('/loggedin')
                for i in transaction_details:
                        data.append(i)
                s = ''
                for i in data:
                        trans_id = str(data[i][0])
                        emp_id = str(data[i][1])
                        trans_date = str(data[i][2])
                        trans_type = str(data[i][3])
                        amount = str(data[i][4])
                        ac_from = str(data[i][5])
                        ac_to = str(data[i][6])
                        s = s+' Transaction ID=' + str(trans_id) + ', Employee ID= ' + str(emp_id)
                        s = s + ', Transaction Date=' + str(trans_date) + ', Transaction type= ' + str(trans_type)
                        s = s + ', Amount=' + str(amount) + ', Account From= ' + str(ac_from) + ', Account To=  ' + str(
                                ac_to)
                        s = s + '\n\n'
                res = HttpResponse(s)
                res['Content-Disposition'] = 'attachment; filename=EmployeeDetails.txt'
                return res
        else:
                return redirect('/logout')


def manager_decision(request):
        if request.session.has_key('username') and request.session['type']=='manger':
                if request.method == 'POST':
                        transid = request.POST.get('transid')
                        option = request.POST.get('decision')
                        cursor = connection.cursor()
                        if option == 'accept':
                                try:
                                        cursor.execute('select * from manager_transfer where trans_id= %s', [transid])
                                except:
                                        return redirect('/loggedin')
                                data = []
                                data_all=''
                                if(cursor.rowcount):
                                        data_all = cursor.fetchall()
                                else:
                                        return redirect('/loggedin')
                                for i in data_all:
                                        data.append(i)
                                managerid = str(data[0][1])
                                transdate = str(data[0][2])
                                transtype = str(data[0][3])
                                transamount = str(data[0][4])
                                trans_ac_from = str(data[0][5])
                                trans_ac_to = str(data[0][6])

                                # cursor.execute("select manager_id from manager_transfer where trans_id= %s", [transid])
                                # managerid = cursor.fetchone()
                                # managerid = int(managerid[0])

                                # cursor.execute("select trans_date from manager_transfer where trans_id= %s", [transid])
                                # transdate = cursor.fetchone()
                                # transdate = str(transdate[0])

                                # cursor.execute("select trans_type from manager_transfer where trans_id= %s", [transid])
                                # transtype = cursor.fetchone()
                                # transtype = str(transtype[0])

                                # cursor.execute("select amount from manager_transfer where trans_id= %s", [transid])
                                # transamount = cursor.fetchone()
                                # transamount = int(transamount[0])
                                # print transamount;

                                # cursor.execute("select ac_from from manager_transfer where trans_id= %s", [transid])
                                # trans_ac_from = cursor.fetchone()
                                # trans_ac_from = int(trans_ac_from[0])

                                # cursor.execute("select ac_to from manager_transfer where trans_id= %s", [transid])
                                # trans_ac_to = cursor.fetchone()
                                # trans_ac_to = int(trans_ac_to[0])

                                if transtype == "debit":  ##subtract amount from balance
                                        try:
                                                cursor.execute("select balance from account where ac_no= %s", [trans_ac_from])
                                        except:
                                                return redirect('/loggedin')
                                        balance = cursor.fetchone()
                                        balance = int(balance[0])
                                        if transamount <= balance:
                                                try:
                                                        cursor.execute("update account set balance = %s where ac_no= %s",(balance - transamount, trans_ac_from))
                                                except:
                                                        return redirect('/loggedin')

                                elif transtype == "credit":
                                        try:
                                                cursor.execute("select balance from account where ac_no= %s", [trans_ac_from])
                                        except:
                                                return redirect('/loggedin')
                                        if(cursor.rowcount):
                                                balance = cursor.fetchone()
                                                balance = int(balance[0])
                                        else:
                                                return redirect('/loggedin')
                                        try:
                                                cursor.execute("update account set balance = %s where ac_no= %s",(balance + transamount, trans_ac_from))
                                        except:
                                                return redirect('/loggedin')

                                elif transtype == "transfer":
                                        try:
                                                cursor.execute("select balance from account where ac_no= %s", [trans_ac_from])
                                        except:
                                                return redirect('/loggedin')
                                        if(cursor.rowcount):
                                                balance_from = cursor.fetchone()
                                                balance_from = int(balance_from[0])
                                        else:
                                                return redirect('/loggedin')
                                        try:
                                                cursor.execute("select balance from account where ac_no= %s", [trans_ac_to])
                                        except:
                                                return redirect('/loggedin')
                                        if(cursor.rowcount):
                                                balance_to = cursor.fetchone()
                                                balance_to = int(balance_to[0])
                                        else:
                                                return redirect('/loggedin')

                                        if transamount <= balance_from:
                                                try:
                                                        cursor.execute("update account set balance = %s where ac_no= %s",(balance_from - transamount,trans_ac_from))
                                                except:
                                                        return redirect('/loggedin')
                                                try:
                                                        cursor.execute("update account set balance = %s where ac_no= %s",(balance_to + transamount,trans_ac_to))
                                                except:
                                                        return redirect('/loggedin')

                                query="INSERT INTO transfer_log (trans_id, trans_date, trans_type, amount, ac_from, ac_to, status,approved_by) values ('%s','%s', '%s','%s', '%s','%s', '%s', '%s')"%(transid,transdate, transtype, transamount, trans_ac_from, trans_ac_to, 'accept','manager')
                                try:
                                        cursor.execute(query)
                                except:
                                        return redirect('/loggedin')

                                return redirect('/loggedin/manager_decision')
                                # cursor.execute("delete from manager_transfer where trans_id= %s", [transid])

                        elif option == 'decline':
                                try:
                                        cursor.execute('select * from manager_transfer where trans_id= %s', [transid])
                                except:
                                        return redirect('/loggedin')
                                data = []
                                data_all = cursor.fetchall()
                                for i in data_all:
                                        data.append(i)
                                managerid = str(data[0][1])
                                transdate = str(data[0][2])
                                transtype = str(data[0][3])
                                transamount = str(data[0][4])
                                trans_ac_from = str(data[0][5])
                                trans_ac_to = str(data[0][6])
                                
                                # cursor.execute("select manager_id from manager_transfer where trans_id= %s", [transid])
                                # managerid = cursor.fetchone()
                                # managerid = int(managerid[0])

                                # cursor.execute("select trans_date from emp_transfer where trans_id= %s", [transid])
                                # transdate = cursor.fetchone()
                                # transdate = str(transdate[0])

                                # cursor.execute("select trans_type from emp_transfer where trans_id= %s", [transid])
                                # transtype = cursor.fetchone()
                                # transtype = str(transtype[0])

                                # cursor.execute("select amount from emp_transfer where trans_id= %s", [transid])
                                # transamount = cursor.fetchone()
                                # transamount = int(transamount[0])

                                # cursor.execute("select ac_from from emp_transfer where trans_id= %s", [transid])
                                # trans_ac_from = cursor.fetchone()
                                # trans_ac_from = int(trans_ac_from[0])

                                # cursor.execute("select ac_to from emp_transfer where trans_id= %s", [transid])
                                # trans_ac_to = cursor.fetchone()
                                # trans_ac_to = int(trans_ac_to[0])

                                query = "INSERT INTO transfer_log (trans_id, trans_date, trans_type, amount, ac_from, ac_to, status,approved_by) values ('%s','%s', '%s','%s', '%s','%s', '%s', '%s')" % (
                                transid, transdate, transtype, transamount, trans_ac_from, trans_ac_to,
                                'decline', 'manager')
                                try:
                                        cursor.execute(query)
                                except:
                                        return redirect('/loggedin')
                                return redirect('/loggedin/manager_decision')

                                # cursor.execute("delete from manager_transfer where trans_id= %s", [transid])
                        else:
                                return redirect('/loggedin/manager_decision')

                else:
                        form = UserCreationForm()
                        args = {'form': form}
                        return render(request, 'loggedin/manager_decision.html')

        else:
                return redirect('/logout')


def merch_decision(request):
        if request.session.has_key('username') and request.session['type'] == 'merch':
                user = request.session['username']
                cursor = connection.cursor()

                if request.method == 'POST':
                        transid = request.POST.get('transid')
                        option = request.POST.get('decision')

                        cursor = connection.cursor()
                        if option == 'accept':
                                try:
                                        cursor.execute('select approval from emp_transfer where trans_id= %s', [transid])
                                except:
                                        return redirect('/loggedin')
                                approval = cursor.fetchone()
                                approval = str(approval)
                                if (approval == 'Yes'):

                                        try:
                                                cursor.execute('select * from emp_transfer where trans_id= %s',
                                                               [transid])
                                        except:
                                                return redirect('/loggedin')
                                        data = []
                                        data_all = cursor.fetchall()
                                        for i in data_all:
                                                data.append(i)
                                        empid = str(data[0][1])
                                        transdate = str(data[0][2])
                                        transtype = str(data[0][3])
                                        transamount = str(data[0][4])
                                        trans_ac_from = str(data[0][5])
                                        trans_ac_to = str(data[0][6])

                                        if transtype == "debit":  ##subtract amount from balance
                                                try:
                                                        cursor.execute("select balance from account where ac_no= %s",[trans_ac_from])
                                                except:
                                                       return redirect('/loggedin')
                                                balance = cursor.fetchone()
                                                balance = int(balance[0])
                                                print balance
                                                if transamount <= balance:
                                                        try:
                                                                cursor.execute("update account set balance = %s where ac_no= %s",(balance - transamount, trans_ac_from))
                                                        except:
                                                                return redirect('/loggedin')
                                        elif transtype == "credit":
                                                try:
                                                        cursor.execute("select balance from account where ac_no= %s",[trans_ac_from])
                                                except:
                                                       return redirect('/loggedin')
                                                balance = cursor.fetchone()
                                                balance = int(balance[0])
                                                try:
                                                        cursor.execute("update account set balance = %s where ac_no= %s",[balance + transamount], [trans_ac_from])
                                                except:
                                                       return redirect('/loggedin')

                                        elif transtype == "transfer":
                                                try:
                                                        cursor.execute("select balance from account where ac_no= %s",[trans_ac_from])
                                                except:
                                                       return redirect('/loggedin')
                                                balance_from = cursor.fetchone()
                                                balance_from = int(balance_from[0])
                                                try:
                                                        cursor.execute("select balance from account where ac_no= %s",[trans_ac_to])
                                                except:
                                                       return redirect('/loggedin')
                                                balance_to = cursor.fetchone()
                                                balance_to = int(balance_to[0])

                                                if transamount <= balance_from:
                                                        try:
                                                                cursor.execute("update account set balance = %s where ac_no= %s",(balance_from - transamount, trans_ac_from))
                                                                cursor.execute("update account set balance = %s where ac_no= %s",(balance_to + transamount, trans_ac_to))
                                                        except:
                                                                return redirect('/loggedin')

                                        query = "INSERT INTO transfer_log (trans_id, trans_date, trans_type, amount, ac_from, ac_to, status,approved_by) values ('%s','%s', '%s','%s', '%s','%s', '%s', '%s')" % (
                                                transid, transdate, transtype, transamount, trans_ac_from, trans_ac_to,
                                                'accept', 'merch')
                                        try:
                                                cursor.execute(query)
                                        except:
                                                return redirect('/loggedin')

                                return redirect('/loggedin/merch_decision')
                                # cursor.execute("delete from emp_transfer where trans_id= %s", [transid])

                        elif option == 'decline':
                                try:
                                        cursor.execute('select * from emp_transfer where trans_id= %s', [transid])
                                except:
                                        return redirect('/logout')
                                data = []
                                data_all = cursor.fetchall()
                                for i in data_all:
                                        data.append(i)
                                empid = str(data[0][1])
                                transdate = str(data[0][2])
                                transtype = str(data[0][3])
                                transamount = str(data[0][4])
                                trans_ac_from = str(data[0][5])
                                trans_ac_to = str(data[0][6])

                                query = "INSERT INTO transfer_log (trans_id, trans_date, trans_type, amount, ac_from, ac_to, status,approved_by) values ('%s','%s', '%s','%s', '%s','%s', '%s', '%s')" % (
                                        transid, transdate, transtype, transamount, trans_ac_from, trans_ac_to,
                                        'decline', 'merch')
                                try:
                                        cursor.execute(query)
                                except:
                                        return redirect('/loggedin')

                                return redirect('/loggedin/merch_decision')

                                # cursor.execute("delete from emp_transfer where trans_id= %s", [transid])
                        else:
                                return redirect('/loggedin/emp_decision')

                else:
                        form = UserCreationForm()
                        args = {'form': form}
                        return render(request, 'loggedin/merch_decision.html')


        else:
                return redirect('/logout')


def merch_view(request):
        if request.session.has_key('username') and request.session['type'] == 'merch':
                user = request.session['username']
                cursor = connection.cursor()
                try:
                        cursor.execute("select cust_id from customer where user_name= %s", [user])
                except:
                        return redirect('/logout')
                cust_id=''
                if (cursor.rowcount):
                        cust_id = cursor.fetchone()
                        cust_id = str(cust_id[0])
                else:
                        return redirect('/logout')
                print cust_id
                try:
                        cursor.execute("select * from customer where cust_id= %s", [cust_id])
                except:
                        return redirect('/logout')
                data_all = cursor.fetchall()
                data = []
                s=''
                for i in data_all:
                        data.append(i)
                print data
                fname = str(data[0][1])
                lname = str(data[0][2])
                street = str(data[0][3])
                city = str(data[0][4])
                state = str(data[0][5])
                pin = str(data[0][6])
                gender = str(data[0][7])
                email = str(data[0][8])
                user_name = str(data[0][11])
                password = str(data[0][12])
                contact = str(data[0][13])
                s = s+' Merchant ID=' + str(cust_id) + ', First Name= ' + str(fname)
                s = s + ', Street=' + str(street) + ', City= ' + str(city) + ', State= ' + str(state)
                s = s + ', Pin=' + str(pin) + ', Gender= ' + str(gender) + ', Email= ' + str(email)
                s = s + ', User Name= ' + str(user_name)+ ', Password=' + str(password) + ', Contact= ' + str(contact)
                s = s + '\n\n'
                print cust_id
                try:
                        cursor.execute("select * from account where cust_id= %s", [cust_id])
                        data_all = cursor.fetchall()
                        data = []
                        for i in data_all:
                                data.append(i)
                        if (cursor.rowcount):
                                s = s + 'Account details:'
                                s = s + '\n\n'
                                for i in data:
                                        print i
                                        acno = str(i[0])
                                        balance = str(i[2])
                                        open_date = str(i[3])
                                        s = s + ' Account number=' + str(acno) + ', Balance= ' + str(
                                                balance) + ', Open Date= ' + str(open_date)
                                        s = s + '\n'
                except:
                        pass

                res = HttpResponse(s)
                res['Content-Disposition'] = 'attachment; filename=MerchantDetails.txt'
                return res
        else:
                return redirect('/logout')


def merch_debit(request):
        if request.session.has_key('username') and request.session['type'] == 'merch':
                if request.method == 'POST':
                        user = request.session['username']
                        cursor = connection.cursor()
                        password = request.POST.get('pswd')
                        bal = request.POST.get('balance')
                        if(bal<0):
                                return redirect('/loggedin')
                        ac_no = request.POST.get('acno')
                        try:
                                cursor.execute("select password from customer where user_name= %s", [user])
                        except:
                                return redirect('/logout')
                        pswdsql=''
                        if (cursor.rowcount):
                                pswdsql = cursor.fetchone()
                                pswdsql = str(pswdsql[0])
                        else:
                                return redirect('/logout')
                        if (pswdsql == password):
                                try:
                                        cursor.execute("select cust_id from customer where user_name= %s", [user])
                                except:
                                        return redirect('/logout')
                                cust_id=0
                                if (cursor.rowcount):
                                        cust_id = cursor.fetchone()
                                        cust_id = int(cust_id[0])
                                else:
                                        return redirect('/logout')
                                try:
                                        cursor.execute("select cust_id from account where ac_no= %s", [ac_no])
                                except:
                                        return redirect('/loggedin')
                                customer_id=0
                                if (cursor.rowcount):
                                        customer_id = cursor.fetchone()
                                        customer_id = int(customer_id[0])
                                else:
                                        return redirect('/loggedin')
                                if(customer_id==cust_id):
                                        try:
                                                cursor.execute("select balance from account where ac_no= %s", [ac_no])
                                        except:
                                                return redirect('/loggedin')
                                        balance=0
                                        if (cursor.rowcount):
                                                balance = cursor.fetchone()
                                                balance = int(balance[0])
                                        else:
                                                return redirect('/loggedin')
                                        if (int(balance) > int(bal)):
                                        # balance = int(balance)-int(bal)
                                        # values = []
                                        # values.append(user)
                                        # cursor.execute("update account set balance= %s where cust_id=%s", (balance,int(cust_id)))
                                        # cursor.execute("select balance from account where cust_id= %s", [cust_id])
                                        # balance = cursor.fetchone()
                                        # balance = int(balance[0])
                                        # values.append(balance)
                                                balance=int(balance)-int(bal)
                                                try:
                                                        cursor.execute("update account set balance = %s where ac_no= %s",(balance,ac_no))
                                                except:
                                                        return redirect('/loggedin')
                                                return render(request, 'loggedin/merchant_login.html')
                                        else:
                                                form = UserCreationForm()
                                                args = {'form': form}
                                                return render(request, 'loggedin/merchant_login.html')
                                else:
                                        form = UserCreationForm()
                                        args = {'form': form}
                                        return render(request, 'loggedin/merchant_login.html')
                        else:
                                form = UserCreationForm()
                                args = {'form': form}
                                return render(request, 'loggedin/merchant_login.html')
                else:
                        form = UserCreationForm()
                        args = {'form': form}
                        return render(request, 'loggedin/merch_debit.html')
        else:
                return redirect('/logout')


def merch_credit(request):
        if request.session.has_key('username') and request.session['type'] == 'merch':
                if request.method == 'POST':
                        user = request.session['username']
                        cursor = connection.cursor()
                        password = request.POST.get('pswd')
                        bal = request.POST.get('balance')
                        if(bal<0):
                                return redirect('/loggedin')
                        ac_no = request.POST.get('acno')
                        try:
                                cursor.execute("select password from customer where user_name= %s", [user])
                        except:
                                return redirect('/logout')
                        pswdsql= ''
                        if (cursor.rowcount):
                                pswdsql = cursor.fetchone()
                                pswdsql = str(pswdsql[0])
                        else:
                                return redirect('/logout')
                        if (pswdsql == password):
                                try:
                                        cursor.execute("select cust_id from customer where user_name= %s", [user])
                                except:
                                        return redirect('/logout')
                                cust_id = 0
                                if (cursor.rowcount):
                                        cust_id = cursor.fetchone()
                                        cust_id = int(cust_id[0])
                                else:
                                        return redirect('/logout')
                                try:
                                        cursor.execute("select cust_id from account where ac_no= %s", [ac_no])
                                except:
                                        return redirect('/logout')
                                customer_id= 0
                                if (cursor.rowcount):
                                        customer_id = cursor.fetchone()
                                        customer_id = int(customer_id[0])
                                else:
                                        return redirect('/logout')
                                if (customer_id == cust_id):
                                        try:
                                                cursor.execute("select balance from account where ac_no= %s", [ac_no])
                                        except:
                                                return redirect('/loggedin')
                                        balance = 0
                                        if (cursor.rowcount):
                                                balance = cursor.fetchone()
                                                balance = int(balance[0])
                                        else:
                                                return redirect('/loggedin')
                                        balance = int(balance) + int(bal)
                                        try:
                                                cursor.execute("update account set balance = %s where ac_no= %s",(balance, ac_no))
                                        except:
                                                return redirect('/loggedin')
                                        return render(request, 'loggedin/merchant_login.html')
                                else:
                                        form = UserCreationForm()
                                        args = {'form': form}
                                        return render(request, 'loggedin/merchant_login.html')
                        else:
                                form = UserCreationForm()
                                args = {'form': form}
                                return render(request, 'loggedin/merchant_login.html')
                else:
                        form = UserCreationForm()
                        args = {'form': form}
                        return render(request, 'loggedin/merch_credit.html')
        else:
                return redirect('/logout')


def merch_transfer(request):
        if request.session.has_key('username') and request.session['type'] == 'merch':
                if request.method == 'POST':
                        user = request.session['username']
                        cursor = connection.cursor()
                        password = request.POST.get('pswd')
                        accno = request.POST.get('accno')
                        ac_no = request.POST.get('ac_no')
                        bal = request.POST.get('balance')
                        if(bal<0):
                                return redirect('/loggedin')
                        try:
                                cursor.execute("select password from customer where user_name= %s", [user])
                        except:
                                return redirect('/logout')
                        pswdsql = cursor.fetchone()
                        pswdsql = str(pswdsql[0])
                        if (pswdsql == password):
                                try:
                                        cursor.execute("select cust_id from customer where user_name= %s", [user])
                                except:
                                        return redirect('/logout')
                                cust_id= 0
                                if (cursor.rowcount):
                                        cust_id = cursor.fetchone()
                                        cust_id = int(cust_id[0])
                                else:
                                        return redirect('/logout')
                                try:
                                        cursor.execute("select balance from account where cust_id= %s", [cust_id])
                                        cursor.execute("select cust_id from account where ac_no= %s", [ac_no])
                                        customer_id=0
                                        if(cursor.rowcount):
                                                customer_id = cursor.fetchone()
                                                customer_id = int(customer_id[0])
                                        else:
                                                return redirect('/loggedin')
                                except:
                                        return redirect('/loggedin')
                                flag=0
                                balance=0
                                if (customer_id == cust_id):
                                        flag=1
                                        try:
                                                cursor.execute("select balance from account where ac_no= %s", [ac_no])
                                        except:
                                                return redirect('/loggedin')
                                        customer_id = 0
                                        if (cursor.rowcount):
                                                balance = cursor.fetchone()
                                                balance = int(balance[0])
                                        else:
                                                return redirect('/loggedin')
                                else:
                                        return render(request, 'loggedin/merchant_login.html')
                                reciever_bal = -1
                                try:
                                        cursor.execute("select balance from account where ac_no= %s", [accno])
                                        customer_id = 0
                                        if (cursor.rowcount):
                                                reciever_bal = cursor.fetchone()
                                                reciever_bal = int(reciever_bal[0])
                                        else:
                                                return redirect('/loggedin')
                                except:
                                        return redirect('/loggedin')
                                if (int(balance) >= int(bal) and int(reciever_bal) >= 0):
                                        # balance=int(balance)-int(bal)
                                        # reciever_bal = int(reciever_bal)+int(bal)
                                        # cursor.execute("update account set balance= %s where cust_id=%s",(balance, int(cust_id)))
                                        # cursor.execute("update account set balance= %s where ac_no=%s",(reciever_bal,accno))
                                        # return render(request, 'loggedin/customer_login.html')
                                        balance=int(balance)- int(bal)
                                        reciever_bal = int(reciever_bal) + int(bal)
                                        try:
                                                cursor.execute("update account set balance = %s where ac_no= %s",(balance, ac_no))
                                                cursor.execute("update account set balance = %s where ac_no= %s",(reciever_bal, accno))
                                        except:
                                                return redirect('/loggedin')
                                        return render(request, 'loggedin/merchant_login.html')
                                else:
                                        form = UserCreationForm()
                                        args = {'form': form}
                                        return render(request, 'loggedin/merchant_login.html')
                        else:
                                form = UserCreationForm()
                                args = {'form': form}
                                return render(request, 'loggedin/merchant_login.html')
                else:
                        form = UserCreationForm()
                        args = {'form': form}
                        return render(request, 'loggedin/merch_transfer.html')
        else:
                return redirect('/logout')


def merch_modify(request):
        if request.session.has_key('username') and request.session['type'] == 'merch':
                if request.method == 'POST':
                        user = request.session['username']
                        cursor = connection.cursor()
                        password = request.POST.get('opswd')
                        try:
                                cursor.execute("select password from customer where user_name= %s", [user])
                        except:
                                return redirect('/logout')
                        pswdsql=''
                        if (cursor.rowcount):
                                pswdsql = cursor.fetchone()
                                pswdsql = str(pswdsql[0])
                        else:
                                return redirect('/logout')
                        if (pswdsql == password):
                                fname = request.POST.get('fname')
                                street = request.POST.get('street')
                                city = request.POST.get('city')
                                state = request.POST.get('state')
                                pin = request.POST.get('pin')
                                email = request.POST.get('email')
                                contact = request.POST.get('contact')
                                password = request.POST.get('pswd')
                                try:
                                        cursor.execute("update customer set first_name=%s,street=%s,city=%s,state=%s,pin=%s,email=%s,contact=%s,password=%s where user_name=%s",(fname, street, city, state, pin, email, contact, password, user))
                                except:
                                        return redirect('/loggedin')
                                return render(request, 'loggedin/merchant_login.html')
                        else:
                                form = UserCreationForm()
                                args = {'form': form}
                                return render(request, 'loggedin/merchant_login.html')
                else:
                        form = UserCreationForm()
                        args = {'form': form}
                        return render(request, 'loggedin/merch_modify.html')
        else:
                return redirect('/logout')


def merch_add_account(request):
        if request.session.has_key('username') and request.session['type'] == 'merch':
                if request.method == 'POST':
                        user = request.session['username']
                        cursor = connection.cursor()
                        password = request.POST.get('pswd')
                        try:
                                cursor.execute("select password from customer where user_name= %s", [user])
                        except:
                                return redirect('/logout')
                        pswdsql= ''
                        if (cursor.rowcount):
                                pswdsql = cursor.fetchone()
                                pswdsql = str(pswdsql[0])
                        else:
                                return redirect('/logout')
                        if (pswdsql == password):
                                try:
                                        cursor.execute("select cust_id from customer where user_name= %s", [user])
                                except:
                                        return redirect('/logout')
                                cust_id = 0
                                if (cursor.rowcount):
                                        cust_id = cursor.fetchone()
                                        cust_id = str(cust_id[0])
                                else:
                                        return redirect('/logout')
                                balance = request.POST.get('balance')
                                if(balance<0):
                                        return redirect('/loggedin')
                                open_date = datetime.datetime.now()
                                query = "INSERT INTO account (cust_id,balance,open_date) values ('%s','%s', '%s')" % (cust_id,balance,open_date)
                                try:
                                        cursor.execute(query)
                                except:
                                        return redirect('/loggedin')
                                return render(request, 'loggedin/merchant_login.html')
                        else:
                                form = UserCreationForm()
                                args = {'form': form}
                                return render(request, 'loggedin/merch_add_account.html')
                else:
                        form = UserCreationForm()
                        args = {'form': form}
                        return render(request, 'loggedin/merch_add_account.html')
        else:
                return redirect('/logout')
