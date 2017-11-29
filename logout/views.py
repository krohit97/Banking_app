from django.shortcuts import render,redirect

# Create your views here.
def index(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect('/home')