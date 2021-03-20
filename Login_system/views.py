from django.conf import settings
from django.http import HttpResponse 
from django.shortcuts import render, redirect 
'''from .models import *
from .forms import *
from PIL import Image '''
import math, random 
from django.views import View
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.core.mail import send_mail
def login(request):
    if request.method=="POST":
        user=request.POST['username']
        passwd=request.POST['password']

        user=auth.authenticate(username=user,password=passwd)
        if user is not None:
            auth.login(request,user)
            return redirect('/main')
        else:
            messages.warning(request,'Invalid Login Credentials !!! ')
            #return HttpResponse("<script>alert('Invalid Login Credentials !!! ');</script>")
            return redirect('/Login')


    else:
        return render(request,"signin.html")

def forgot_pass(request):
    if request.method=="POST":
        forgot_pass.email=request.POST['email']
        if User.objects.filter(email=forgot_pass.email).exists():
            digits = "0123456789"
            for i in range(6) : 
                forgot_pass.OTP += digits[math.floor(random.random() * 10)] 
            subject = "Request for Password Change"
            message = "Your request for changing password is accepted you need to use the pin "+forgot_pass.OTP+" for changing the passwod ..."
            from_email = settings.EMAIL_HOST_USER
            to_list = [request.POST["email"],]
            send_mail(subject,message,from_email,to_list,fail_silently=True)
            return redirect('/Check_otp')
        else:
            messages.warning(request,'Email is Invalid !!!')
            return redirect('/Forgot_password')

    else:
        return render(request,"email.html")   

def signup(request):
    if request.method == 'POST':
        signup.username=request.POST['username']
        signup.email=request.POST['email']
        signup.pass1=request.POST['password1']
        pass2=request.POST['password2']
        if signup.pass1==pass2:
            if User.objects.filter(username=signup.username).exists():
                messages.warning(request,'Username already Taken !!! ')
                return redirect('/Register')
                #return HttpResponse("<script>alert('Username already Taken !!! ');</script>")
            elif User.objects.filter(email=signup.email).exists():
                messages.warning(request,'Email already Taken !!! ')
                return redirect('/Register')
                #return HttpResponse("<script>alert('Email already Taken !!! ');</script>")
            else:
                digits = "0123456789"
                signup.reg_pin = ""
                for i in range(6) : 
                    signup.reg_pin += digits[math.floor(random.random() * 10)]
                subject = "Request for Account Creation"
                message = "You are just one step ahead for ur creation of account You need to  use this pin "+signup.reg_pin+" for creating account ..."
                from_email = settings.EMAIL_HOST_USER
                to_list = [signup.email,]
                send_mail(subject,message,from_email,to_list,fail_silently=True)
                forgot_pass.OTP=""
                return redirect('/Check_otp')
                
                #return redirect('/Login')
        else:
            messages.warning(request,'Password  not matching  !!! ')
            return redirect('/Register')
            #return HttpResponse("<script>alert('Password  not matching ');</script>")    
    else:
	    return render(request,"signup.html")

def logout(request):
    auth.logout(request)
    return redirect('/main')

 
    
def check_user_otp(request):
    if request.method=="POST":
        pin_value=request.POST['pin']
        #return render(request,"test.html",{'encoded':forgot_pass.OTP,'p':pin_value})
        if pin_value==forgot_pass.OTP:
            return redirect('/change_password')
        elif pin_value==signup.reg_pin:
            user = User.objects.create_user(username=signup.username,email=signup.email,password=signup.pass1)
            user.save()
            messages.warning(request,'Account created successfully !!! ')
            return redirect('/Login')
        else:
            messages.warning(request,'Invalid OTP !!! ')
            return redirect('/Check_otp')
        
    else:
        return render(request,"otp.html")

def change_password(request):
    if request.method=="POST":
        pass1=request.POST['password1']
        pass2=request.POST['password2']
        if pass1 == pass2:
            users=User.objects.filter(email=forgot_pass.email) 
            user=users[0]
            user.set_password(pass2)
            user.save()
            messages.warning(request,'Password Changed Successfully !!! ')
            return redirect('/Login')
            #return HttpResponse(("<script>alert('Password Changed Successfully !!!');</script>"))
            
        else:
            messages.warning(request,'Invalid Password !!! ')
            return redirect('/change_password')
    else:
        return render(request,"pass_change.html")
   