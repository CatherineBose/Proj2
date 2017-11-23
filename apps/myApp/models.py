from __future__ import unicode_literals

import re
import bcrypt
from django.db import models
import datetime
from time import gmtime, strftime

emailFilterREGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
nameFilterREGEX = re.compile(r'^[^\W_]+(-[^\W_]+)?$', re.U)

# Create your models here.
class UserManager(models.Manager):
    def login_validator(self, postData):
        errors = []
        if len(self.filter(email=postData['email'])) > 0:
            user = self.filter(email=postData['email'])[0]
            # check this user's password
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors.append('password incorrect, check if caps lock is on')
        else:
            errors.append('email incorrect or your not registered ')
        if errors:
            return errors
        return user

    def register_validator(self,postData):
        #Initialize empty array for errors 
        errors = [] 
        # check first name and last name length
        name = str(postData['name'])
        alias= str(postData['alias'])
        if len(name) < 2: 
            errors.append("User name and alias should be more than 2 characters")
        if len(alias) < 2:
            errors.append("alias should be more than 2 characters")
        # check password
        if len(postData['password']) < 8:
            errors.append("Password should have more than 8 characters") 
        # check name has valid characters
        name = postData['name']
        print "type(name)", type(name)
        print name
        nameString = str (name)
        print "nameString: ", nameString
        print "nameString.isalpha(): ", nameString.isalpha()
        # if not nameString.isalpha():
        if not all(i.isalpha() or i==' ' for i in nameString):
            errors.append("User name should contains only letters no special characters allowed ")
        #Alias
        alias = postData['alias']
        aliasString = str (alias)
        # if not str(postData['alias']).isalpha():
        if not all(i.isalpha() or i==' ' for i in aliasString):
            errors.append("alias should contains only letters no special characters allowed")
        # check email with Email_REgex
        if not re.match(emailFilterREGEX, postData['email']):
            errors.append("Not a valid email")
        if len(User.objects.filter(email=postData['email'])) > 0:
            errors.append("email already in use") 
        # check password
        if postData['password'] != postData['confirm']:
            errors.append("Password doesn't match")
        # # check if password has one capital letter and one no
        passWdString = postData['password']
        print "passWdString: ", passWdString
        if not (any(x.isupper() for x in passWdString) ):
            print passWdString + " passWdString is not a valid password"
            errors.append("Password should have at least one capital letter ")
        # check if password has one no
        if not(any(x.isdigit() for x in passWdString)):
            errors.append("Password should have at least one digit")
        #Date check
        print "inside the Date check"
        try:
            print "inside try" 
            dob = datetime.datetime.strptime(postData['birthday'], '%Y-%m-%d')
            print "dob:", dob
            print "datetime.datetime.now():", datetime.datetime.now()
            if dob > datetime.datetime.now():
                print "inside if which means dob > datetime.datetime.now()"
                print "errors.append : Birthday day shoud be valid !"
                errors.append("Birthday day shoud be valid !")
        except:
            errors.append ("Please input a birth date")
        
        print "errors List \n", errors
        print "name=postData['name']", postData['name']
        print "alias=postData['alias']", postData['alias']
        print "email=postData['email']", postData['email']
        print "password", postData['password']
        print "birthday = postData['birthday']", postData['birthday']
        
       
        if not errors:
                print "Inside hash password"
                # add a new user
                # hash password
                hashed = bcrypt.hashpw((postData['password'].encode()), bcrypt.gensalt(5))
                print "hashed code: ", hashed
                new_user = self.create(
                    name=postData['name'],
                    alias=postData['alias'],
                    email=postData['email'],
                    password=hashed,
                    birthday = postData['birthday']
                )
                return new_user
        return errors

class AppointmentManager(models.Manager):

    def update_myapp(self, POST,user_id , appt_id):
        date = (postData['date']).strftime('%Y-%m-%d')
        time = postData['time']
        task = (postData['task'])
        status= (postData['status'])
        errors = []
        taskString = str (task)
        statusString = str (status)

        print "taskString.isalpha(): ", taskString.isalpha()
        # if not taskString.isalpha():
        if not all(i.isalpha() or i==' ' for i in taskString):
            errors.append("User name should contains only letters or spaces, no special characters allowed!! ")
        #Status is alpha
        if not all(i.isalpha() for i in statusString):
            errors.append("status should contain only letters no special characters allowed")
        #Date check
        print "inside the Date check"
        try:
            print "inside try" 
            appDate = datetime.datetime.strptime(postData['date'], '%Y-%m-%d')
            print "appDate:",appDate
            print "datetime.datetime.now():", datetime.datetime.now()
            if appDate < datetime.datetime.now():
                print "inside if which means appDate <  datetime.datetime.now()"
                print "errors.append : Appointment can be only set for current or future date !"
                errors.append("Appointment can be only set for current or future date !")
        except:
            errors.append ("Please input a appointment date")
        if not errors:
            appointment = Appointment.objects.filter(user_id=user_id, id=appt_id).update(task=task, status = status, date=date, time=time)
            return (True, appointment)
        return (False, errors)
    def appointment_valid(self, POST, user_id):
		print "AppManager", user_id
		user_id = user_id
		task = POST['task']
		date = POST['date']
		time = POST['time']
		#status = POST['status']
		errors = []
		
		if len(task) < 1 or len(date) < 1 or len(time) < 1:
			errors["mesage"]="A field can not be empty"
		else:
			if date < unicode(datetime.date.today()):
				errors["date"]="Appointment can not be in the past"
			else:
				#user = User.objects.get(id=user_id)
				appointment = Appointment.objects.create(user_id=user_id, task=task, date=date, time=time)
				return (True, appointment)
		return (False, errors)

	
    def appointment_add__validator(self, postData):
        errors = []
        #Filter if task exists for the user : if yes check date
        if len(self.filter(task=postData['task'])) > 0:
            appointment = self.filter(task=postData['task'])[0]
            # check this user's task date
            postDate = postData['date'].strftime('%Y-%m-%d')
            if (appointment.date == postData['date']):
                errors.append('Task exists please add another task')
        if errors:
            return errors
        return appointment
    

    def appointment_validator(self,postData):
        #Initialize empty array for errors 
        errors = [] 
        # check first name and last name length
        task = str(postData['task'])
        status= str(postData['status'])
        if len(task) < 2: 
            errors.append("task should be more than 2 characters")
        if len(status) < 2:
            errors.append("Please choose a status")
        # check task has valid characters
        task = postData['task']
        print "type(task)", type(task)
        print task
        taskString = str (task)
        print "taskString: ", taskString
        print "taskString.isalpha(): ", taskString.isalpha()
        # if not taskString.isalpha():
        if not all(i.isalpha() or i==' ' for i in taskString):
            errors.append("User name should contains only letters or spaces, no special characters allowed!! ")
        #Status is alpha
        status = postData['status']
        statusString = str (status)
        # if not  statusString.isalpha():
        if not all(i.isalpha() for i in statusString):
            errors.append("status should contain only letters no special characters allowed")
        #Date check
        print "inside the Date check"
        try:
            print "inside try" 
            appDate = datetime.datetime.strptime(postData['date'], '%Y-%m-%d')
            print "appDate:",appDate
            print "datetime.datetime.now():", datetime.datetime.now()
            if appDate < datetime.datetime.now():
                print "inside if which means appDate <  datetime.datetime.now()"
                print "errors.append : Appointment can be only set for current or future date !"
                errors.append("Appointment can be only set for current or future date !")
        except:
            errors.append ("Please input a appointment date")
        
        print "errors List \n", errors
        print "task=postData['task']", postData['task']
        print "time=postData['time']", postData['time']
        print "date=postData['email']", postData['date']
        
        if not errors:
                print "Inside Appointment object creation"
                # add a new appointment
                new_appointment = self.create(
                    task=postData['task'],
                    status = "Pending",
                    date = postData['date'],
                    time = postData['time']

                )
                return new_user
        return errors

class User(models.Model):
    name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    email = models.TextField(max_length=45)
    password = models.CharField(max_length=45)
    birthday = models.DateTimeField(default = None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return "User: \n{}\n{}\n{}\n{}\n".format(self.id, self.name, self.email, self.birthday)

class Appointment(models.Model):
    task = models.CharField(max_length=100)
    #Setting Default value as  Pending when a appointment gets created
    status = models.CharField(max_length=45, default = 'Pending')
    date = models.DateField(default = None)
    time = models.TimeField(default = None)
    users = models.ForeignKey(User, related_name="appointments")
    objects = AppointmentManager()
    def __repr__(self):
        return "User: \n{}\n{}\n{}\n{}\n".format(self.task, self.status, self.date, self.time)
'''
-------------
from apps.myApp.models import *
Appointment.objects.create(task="dentist", date ='2018-10-12', time = '10:00:00')
Appointment.objects.create(task="dentist", date ='2018-10-12', time = '10:00:00', users_id = 1)
Appointment.objects.create(task="dentist", date ='2017-12-12', time = '10:00:00', users_id = 2)
Appointment.objects.create(task="Lunch with Friends", date ='2017-12-01', time = '11:00:00', users_id = 1)
Appointment.objects.create(task="Church Christmas Mass", date ='2017-12-25', time = '11:00:00', users_id = 1)
Appointment.objects.create(task="Grocery Shopping", date ='2017-11-22', time = '4:00:00', users_id = 1)
Appointment.objects.create(task="Decking up the Tree", date ='2017-11-22', time = '9:30:00', users_id = 1)
Appointment.objects.filter(users=1)
Appointment.objects.filter(users=1).order_by("time")
Appointment.objects.filter(users=1).filter(date ='2017-11-22').order_by("time")
Appointment.objects.filter(users=1).exclude(date ='2017-11-22').order_by("time")
'''