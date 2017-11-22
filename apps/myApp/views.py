from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime
from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from .models import User
from .models import *

# urlpatterns = [
#     url(r'^$', views.index),     # This line has changed
#     url(r'^register$', views.register),
#     url(r'^login$', views.login),
#     url(r'^logout$', views.logout),
#     url(r'^home$', views.wall),
#     url(r'^user/(?P<id>\d+)',views.show),
#     url(r'^remove/(?P<id>\d+)', views.remove),
#     url(r'^add/(?P<id>\d+)', views.add)
# ]
# Create your views here.

def index(request):
    return render(request,'myApp/index.html')
    

def register(request):
    result = User.objects.register_validator(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    # if user_id  in request.session:
    print "result.id",result.id
    request.session['user_id'] = result.id
    messages.success(request, "Successfully registered!")
    return redirect('/home')

def login(request):
    result = User.objects.login_validator(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect ('/')   
    request.session['user_id'] = result.id
    print "Successfully logged in!"
    messages.success(request, "Successfully logged in!")
    return redirect('/home')

def logout(request):
    try:
        del request.session['user_id']
    except KeyError:
        print "Error while trying to logout"
    # return HttpResponse("You're logged out.")
    return redirect ('/')   

def wall(request):
    try:
        request.session['user_id']
    except KeyError:
        return redirect ('/')
    user = User.objects.get(id=request.session['user_id'])

    return render(request,'myApp/wall.html')


def show(request, id):
    try:
        request.session['user_id']
    except KeyError:
        return redirect ('/')
    print "request.session['user_id']", request.session['user_id']
    print "id called : ", id
    user = User.objects.get(id=id)
    print user.name
    print user.email
    print user.alias
    context ={
        'user': user
    }
    return render(request,'myApp/show.html', context)


def remove(request,id):
    try:
        request.session['user_id']
    except KeyError:
        return redirect ('/')
    return redirect('/home')



def add(request):
    try:
        request.session['user_id']
    except KeyError:
        return redirect ('/')   
    return redirect('/home')
