from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime
from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from .models import User
from .models import *
import datetime

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
    id = request.session['user_id']
    date = datetime.datetime.now()
    dateformat= date.strftime('%Y-%m-%d')
    print dateformat
    print "date:", datetime.datetime.now()
    print "id", id
    todayApp = Appointment.objects.filter(users= id).filter(date = dateformat).order_by("time")
    remainingApp = Appointment.objects.filter(users= id).exclude(date = dateformat).order_by("time")
    # for i in todayApp:
    #     print i.task
    #     print i.date
    #     print i.status
    context ={
        'user': user,
        'todayApp': todayApp,
        'remApp': remainingApp
    }
    return render(request,'myApp/wall.html', context)


def edit(request, number):

	appointment = Appointment.objects.get(id = number)
	context = {
		"appointment": appointment
	}
	#user_id = request.session['id']
def edit(request, id):
    try:
        request.session['user_id']
    except KeyError:
        return redirect ('/')

    print "request.session['user_id']", request.session['user_id']
    print "appointment id called to edit : ", id
    user = User.objects.get(id=request.session['user_id'])
    print user.name
    appointment = Appointment.objects.get(id = id)
  
    appointment.date = (appointment.date).strftime('%Y-%m-%d')
    appointment.time = appointment.time.replace(microsecond = 0)
    print  appointment.time
    print "appointment .id: ", appointment.id
    context ={
        'user': user,
        'appointment': appointment
    }
    return render(request,'myApp/edit.html', context)


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
    # user_id = request.session['user_id']
    # task = request.POST['task']
    # date = (request.POST['date']).strftime('%Y-%m-%d')
    # time = request.POST['time']
    print "form data Inside add"
    # print task, date, time
    print "##Appointment Add method #########"
    result = Appointment.objects.appointment_valid_add_create(request.POST, request.session['user_id'])
    print "result", result
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/home')
    else:
        messages.success(request, "Successfully Added Appointment!")
        return redirect('/home')

def update(request, user_id, id):
	result= Appointment.objects.update_myapp(request.POST, user_id, id)
	user_id = request.session['id']
	# appointment = Appointment.objects.appointment_valid(request.POST, user_id)
	# appointment.save()
	if result[0] == False:
		for error in result[1]:
			messages.add_message(request, messages.INFO, error)
	else:
		return redirect("/appointments")

	return redirect("/update")


