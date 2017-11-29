from django.shortcuts import render, HttpResponse, redirect
# Create your views here.
from django.db import connection, transaction
from django.contrib.auth.forms import UserCreationForm
import datetime
import random
# Create your views here.
def index(request):
        if request.session.has_key('username'):
                user=request.session['username']
                user_type=request.session['type']
                if(user_type=='cust'):
                        return render(request, 'loggedin/customer_login.html')
                elif(user_type=='emp'):
                        return render(request, 'loggedin/employee_login.html')
                elif (user_type == 'manger'):
                        return render(request, 'loggedin/manager_login.html')
                elif (user_type == 'admin'):
                        return render(request, 'loggedin/admin_login.html')
        else:
                return redirect('/home')


def cust_view(request):
        if request.session.has_key('username'):
                user = request.session['username']
                cursor = connection.cursor()
                cursor.execute("select cust_id from customer where user_name= %s", [user])
                cust_id = cursor.fetchone()
                cust_id = str(cust_id[0])
                cursor.execute("select balance from account where cust_id= %s", [cust_id])
                balance = cursor.fetchone()
                balance = int(balance[0])
                values=[]
                values.append(user)
                values.append(balance)
                return render(request,'loggedin/cust_view.html',{"values":values} )
        else:
                return redirect('/home')


def cust_debit(request):
        if request.session.has_key('username'):
                if request.method == 'POST':
                        user = request.session['username']
                        cursor = connection.cursor()
                        password = request.POST.get('pswd')
                        bal = request.POST.get('balance')
                        cursor.execute("select password from customer where user_name= %s", [user])
                        pswdsql = cursor.fetchone()
                        pswdsql = str(pswdsql[0])
                        if (pswdsql == password):
                                cursor.execute("select cust_id from customer where user_name= %s", [user])
                                cust_id = cursor.fetchone()
                                cust_id = str(cust_id[0])
                                cursor.execute("select balance from account where cust_id= %s", [cust_id])
                                balance = cursor.fetchone()
                                balance = int(balance[0])
                                if(int(balance)>int(bal)):
                                        #balance = int(balance)-int(bal)
                                        #values = []
                                        #values.append(user)
                                        #cursor.execute("update account set balance= %s where cust_id=%s", (balance,int(cust_id)))
                                        #cursor.execute("select balance from account where cust_id= %s", [cust_id])
                                        #balance = cursor.fetchone()
                                        #balance = int(balance[0])
                                        #values.append(balance)
                                        cursor.execute("select ac_no from account where cust_id= %s", [cust_id])
                                        ac_from = cursor.fetchone()
                                        ac_from = int(ac_from[0])
                                        all_emp_id = []
                                        trans_date = datetime.datetime.now()
                                        trans_type = 'debit'
                                        bal = int(bal)
                                        trans_date = datetime.datetime.now()
                                        bal = int(bal)
                                        if (bal>20000):
                                                query = 'Select id from manager'
                                                cursor.execute(query)
                                                manids = cursor.fetchall()
                                                for i in manids:
                                                        all_emp_id.append(i[0])
                                                man_id = random.choice(all_emp_id)
                                                query = "INSERT INTO manager_transfer(manager_id,trans_date,trans_type,amount,ac_from,ac_to) values ('%s','%s', '%s','%s','%s', '%s')" % (man_id, trans_date, trans_type, bal, ac_from, ac_from)
                                        else:
                                                query = 'Select emp_id from employee'
                                                cursor.execute(query)
                                                empids = cursor.fetchall()
                                                for i in empids:
                                                        all_emp_id.append(i[0])
                                                emp_id = random.choice(all_emp_id)
                                                query = "INSERT INTO emp_transfer(emp_id,trans_date,trans_type,amount,ac_from,ac_to) values ('%s','%s', '%s','%s','%s', '%s')" % (emp_id, trans_date,trans_type,bal,ac_from,ac_from)
                                        cursor.execute(query)
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
                        form = UserCreationForm()
                        args = {'form': form}
                        return render(request, 'loggedin/cust_debit.html')
        else:
                return redirect('/home')


def cust_credit(request):
        if request.session.has_key('username'):
                if request.method == 'POST':
                        user = request.session['username']
                        cursor = connection.cursor()
                        password = request.POST.get('pswd')
                        bal = request.POST.get('balance')
                        cursor.execute("select password from customer where user_name= %s", [user])
                        pswdsql = cursor.fetchone()
                        pswdsql = str(pswdsql[0])
                        if (pswdsql == password):
                                cursor.execute("select cust_id from customer where user_name= %s", [user])
                                cust_id = cursor.fetchone()
                                cust_id = str(cust_id[0])
                                cursor.execute("select ac_no from account where cust_id= %s", [cust_id])
                                ac_from = cursor.fetchone()
                                ac_from = int(ac_from[0])
                                all_emp_id = []
                                trans_date = datetime.datetime.now()
                                trans_type = 'credit'
                                bal = int(bal)
                                query=''
                                if (bal > 20000):
                                        query = 'Select id from manager'
                                        cursor.execute(query)
                                        manids = cursor.fetchall()
                                        for i in manids:
                                                all_emp_id.append(i[0])
                                        man_id = random.choice(all_emp_id)
                                        query = "INSERT INTO manager_transfer(manager_id,trans_date,trans_type,amount,ac_from,ac_to) values ('%s','%s', '%s','%s','%s', '%s')" % (
                                        man_id, trans_date, trans_type, bal, ac_from, ac_from)
                                else:
                                        query = 'Select emp_id from employee'
                                        cursor.execute(query)
                                        empids = cursor.fetchall()
                                        for i in empids:
                                                all_emp_id.append(i[0])
                                        emp_id = random.choice(all_emp_id)
                                        query = "INSERT INTO emp_transfer(emp_id,trans_date,trans_type,amount,ac_from,ac_to) values ('%s','%s', '%s','%s','%s', '%s')" % (
                                        emp_id, trans_date, trans_type, bal, ac_from, ac_from)
                                cursor.execute(query)
                                return render(request, 'loggedin/customer_login.html')
                        else:
                                form = UserCreationForm()
                                args = {'form': form}
                                return render(request, 'loggedin/cust_credit.html')
                else:
                        form = UserCreationForm()
                        args = {'form': form}
                        return render(request, 'loggedin/cust_credit.html')
        else:
                return redirect('/home')


def cust_modify(request):
        if request.session.has_key('username'):
                if request.method == 'POST':
                        user = request.session['username']
                        cursor = connection.cursor()
                        password = request.POST.get('opswd')
                        cursor.execute("select password from customer where user_name= %s", [user])
                        pswdsql = cursor.fetchone()
                        pswdsql = str(pswdsql[0])
                        if (pswdsql == password):
                                cursor.execute("select cust_id from customer where user_name= %s", [user])
                                cust_id = cursor.fetchone()
                                cust_id = str(cust_id[0])
                                fname = request.POST.get('fname')
                                lname = request.POST.get('lname')
                                street = request.POST.get('street')
                                city = request.POST.get('city')
                                state = request.POST.get('state')
                                pin = request.POST.get('pin')
                                email = request.POST.get('email')
                                contact = request.POST.get('contact')
                                pan = request.POST.get('pan')
                                dob = request.POST.get('dob')
                                adhar = request.POST.get('adhar')
                                password = request.POST.get('pswd')
                                cursor.execute("update customer set first_name=%s,last_name=%s,street=%s,city=%s,state=%s,pin=%s,email=%s,pan=%s,dob=%s,contact=%s,password=%s,adhar=%s where cust_id=%s",
                                               (fname, lname,street,city,state,pin,email,pan,dob,contact,password,adhar,int(cust_id)))
                                return render(request, 'loggedin/customer_login.html')
                        else:
                                form = UserCreationForm()
                                args = {'form': form}
                                return render(request, 'loggedin/cust_modify.html')
                else:
                        form = UserCreationForm()
                        args = {'form': form}
                        return render(request, 'loggedin/cust_modify.html')
        else:
                return redirect('/home')


def cust_transfer(request):
        if request.session.has_key('username'):
                if request.method == 'POST':
                        user = request.session['username']
                        cursor = connection.cursor()
                        password = request.POST.get('pswd')
                        accno = request.POST.get('accno')
                        bal = request.POST.get('balance')
                        cursor.execute("select password from customer where user_name= %s", [user])
                        pswdsql = cursor.fetchone()
                        pswdsql = str(pswdsql[0])
                        if (pswdsql == password):
                                cursor.execute("select cust_id from customer where user_name= %s", [user])
                                cust_id = cursor.fetchone()
                                cust_id = str(cust_id[0])
                                cursor.execute("select balance from account where cust_id= %s", [cust_id])
                                balance = cursor.fetchone()
                                balance = int(balance[0])
                                reciever_bal=-1
                                try:
                                        cursor.execute("select balance from account where ac_no= %s", [accno])
                                        reciever_bal=cursor.fetchone()
                                        reciever_bal= int(reciever_bal[0])
                                except:
                                        pass
                                if(int(balance)>=int(bal) and int(reciever_bal)>=0):
                                        #balance=int(balance)-int(bal)
                                        #reciever_bal = int(reciever_bal)+int(bal)
                                        #cursor.execute("update account set balance= %s where cust_id=%s",(balance, int(cust_id)))
                                        #cursor.execute("update account set balance= %s where ac_no=%s",(reciever_bal,accno))
                                        #return render(request, 'loggedin/customer_login.html')
                                        cursor.execute("select cust_id from customer where user_name= %s", [user])
                                        cust_id = cursor.fetchone()
                                        cust_id = str(cust_id[0])
                                        cursor.execute("select ac_no from account where cust_id= %s", [cust_id])
                                        ac_from = cursor.fetchone()
                                        ac_from = int(ac_from[0])
                                        ac_to = int(accno)
                                        all_emp_id = []
                                        trans_date = datetime.datetime.now()
                                        trans_type = 'transfer'
                                        bal = int(bal)
                                        query=''
                                        if (bal > 20000):
                                                query = 'Select id from manager'
                                                cursor.execute(query)
                                                manids = cursor.fetchall()
                                                for i in manids:
                                                        all_emp_id.append(i[0])
                                                man_id = random.choice(all_emp_id)
                                                query = "INSERT INTO manager_transfer(manager_id,trans_date,trans_type,amount,ac_from,ac_to) values ('%s','%s', '%s','%s','%s', '%s')" % (man_id, trans_date, trans_type, bal, ac_from, ac_from)
                                        else:
                                                query = 'Select emp_id from employee'
                                                cursor.execute(query)
                                                empids=cursor.fetchall()
                                                for i in empids:
                                                        all_emp_id.append(i[0])
                                                emp_id=random.choice(all_emp_id)
                                                query = "INSERT INTO emp_transfer(emp_id,trans_date,trans_type,amount,ac_from,ac_to) values ('%s','%s', '%s','%s','%s', '%s')" % (emp_id, trans_date, trans_type, bal, ac_from, ac_to)
                                        cursor.execute(query)
                                        return render(request, 'loggedin/customer_login.html')
                                else:
                                        form = UserCreationForm()
                                        args = {'form': form}
                                        return render(request, 'loggedin/cust_transfer.html')
                        else:
                                form = UserCreationForm()
                                args = {'form': form}
                                return render(request, 'loggedin/cust_transfer.html')
                else:
                        form = UserCreationForm()
                        args = {'form': form}
                        return render(request, 'loggedin/cust_transfer.html')
        else:
                return redirect('/home')


def cust_add_account(request):
        if request.session.has_key('username'):
                if request.method == 'POST':
                        user = request.session['username']
                        cursor = connection.cursor()
                        password = request.POST.get('pswd')
                        cursor.execute("select password from customer where user_name= %s", [user])
                        pswdsql = cursor.fetchone()
                        pswdsql = str(pswdsql[0])
                        if (pswdsql == password):
                                cursor.execute("select cust_id from customer where user_name= %s", [user])
                                cust_id = cursor.fetchone()
                                cust_id = str(cust_id[0])
                                balance = request.POST.get('balance')
                                open_date=datetime.datetime.now()
                                query = "INSERT INTO account (cust_id,balance,open_date) values ('%s','%s', '%s')" % (cust_id,balance,open_date)
                                cursor.execute(query)
                                return render(request, 'loggedin/customer_login.html')
                        else:
                                form = UserCreationForm()
                                args = {'form': form}
                                return render(request, 'loggedin/cust_add_account.html')
                else:
                        form = UserCreationForm()
                        args = {'form': form}
                        return render(request, 'loggedin/cust_add_account.html')
        else:
                return redirect('/home')
