from django.conf import settings
from django.shortcuts import render
from ipware.ip import get_ip
from django.conf import settings
import os
# Create your views here.
def index(request):
	ip = get_ip(request)
	path=settings.BASE_DIR
	os.chdir(path)
	with open("Logs.txt", "a") as myfile:
		myfile.write(ip)
		myfile.write("\n")
	return render(request,'home/home.html')
def login(request):
	ip = get_ip(request)
	path = settings.BASE_DIR
	os.chdir(path)
	with open("Logs.txt", "a") as myfile:
		myfile.write(ip)
		myfile.write("\n")
	return render(request,'home/login.html')
def register(request):
	ip = get_ip(request)
	path = settings.BASE_DIR
	os.chdir(path)
	with open("Logs.txt", "a") as myfile:
		myfile.write(ip)
		myfile.write("\n")
	return render(request,'home/register.html')
