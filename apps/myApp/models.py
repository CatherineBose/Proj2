#coding: utf-8
from __future__ import unicode_literals
import sys
import re
import bcrypt
from django.db import models
import datetime
from time import gmtime, strftime

print sys.getdefaultencoding()
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

    def update_myapp(self, postData,user_id , appt_id):
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

    def appointment_valid_add_create(self, postData, user_id):
        errors = []
        print "Inside appointment_valid_add_create"
        print "postData\n", postData
        # print "postData['date']", postData['date']
        #Filter if task exists for the user : if yes check date
        task = str(postData['task'])
        if len(task) < 2: 
            errors.append("task should be more than 2 characters")
        #Check if task exists in Database 
        if len(self.filter(task=postData['task'])) > 0:
            appointment = self.filter(task=postData['task'])[0]
            # if task exists check this user's task date
            postDate = postData['date'].strftime('%Y-%m-%d')
            print "postData['date']:", postData['date']
            print "#######postDate after .strftime('%Y-%m-%d') ###", postDate
            if (appointment.date == postData['date']) and (appointment.date == postData['date']) :
                errors.append('Task exists for the day please add another task/ edit the existing task')
        taskString = str (task)
        print "taskString: ", taskString
        # if not taskString.isalpha():
        if not all(i.isalpha() or i==' ' for i in taskString):
            errors.append("Task should contains only letters or spaces, no special characters allowed!! ")
        #Date check
        print "inside the Date check"
        postDate = postData['date']
        print "postDate:",postDate
        if postDate < unicode(datetime.date.today()):
            errors.append("Appointment can be only set for current or future date ")
        #How to convert a date/string to dateTime Object 
        # datetime.strptime(cr_date, '%Y-%m-%d %H:%M:%S.%f').strftime('%m/%d/%Y')
        postDate = postData['date']
        postDateObj = datetime.datetime.strptime(postDate,'%Y-%m-%d')
        dt_str = datetime.datetime.strftime(postDateObj ,'%Y-%m-%d %H:%M:%S')
        print " postDateObj",  postDateObj,  "dt_str ", dt_str 
        print "datetime.datetime.now():", datetime.datetime.now()
        print "datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')::", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # if  dt_str< datetime.datetime.now():
        #     errors.append("Appointment can be only set for current or future date !")
        # try:
        #     print "inside date check try" 
        #     # appDate = datetime.datetime.strptime(postData['date'], '%Y-%m-%d')
        #     print "postData['date']:", postData['date']
        #     print "#######postDate after.strftime('%Y-%m-%d') ###", postData['date'].strftime('%Y-%m-%d')
        #     postDate = postData['date']
        #     print "postDate:",postDate
        #     print "datetime.datetime.now():", datetime.datetime.now()
        #     print "datetime.datetime.now().strftime('%Y-%m-%d')::", datetime.datetime.now().strftime('%Y-%m-%d')
        #     if postDate < datetime.datetime.now():
        #         print "inside if which means postDate <  datetime.datetime.now()"
        #         print "errors.append : Appointment can be only set for current or future date !"
        #         errors.append("Appointment can be only set for current or future date !")
        # except:
        #     errors.append ("Please input a appointment date")
        
        if not errors:
                print "Inside new appointment creation"
                # Appointment.objects.create(task="dentist", date ='2018-10-12', time = '10:00:00', users_id = 1)
                new_appointment = self.create(
                    task=postData['task'],
                    date=postData['date'],
                    time=postData['time'],
                    users_id=user_id
                )
                return True
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