from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render,redirect
from django.contrib.auth.models import auth,User
from django.contrib import messages
from django.http import HttpResponse
from .models import Datasave,Blogpost
import random
import smtplib
@csrf_protect 
def home(request): 
    if request.method=='POST':
        name=request.POST['namefield']
        topic=request.POST['topic']
        textfield=request.POST['textfield']
        if User.objects.filter(username=name).exists():
            if Blogpost.objects.filter(heading=name,topic=topic,description=textfield):
                return redirect('/')
            else:
                blogsaver=Blogpost(heading=name,topic=topic,description=textfield)
                blogsaver.save()
        else:
            messages.info(request, 'Invalid username')
            return redirect('/')
    content=Blogpost.objects.all()
    return render(request, 'homepage.html',{'content':content})
@csrf_protect
def about(request):
    return render(request, 'about.html')
@csrf_protect
def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Invalid credentials')
            return redirect('login')
    else: 
        return render(request, 'loginpage.html')
def progress(request):
    return render(request, 'progress.html')
@csrf_protect
def signup(request):
    if request.method =='POST':
        full_name=request.POST['fullname']
        username=request.POST['username']
        email=request.POST['email']
        mobile_number=request.POST['mobile']
        password=request.POST['password']
        con_password=request.POST['confirmpassword']
        if full_name=='' and username=='' and email=='' and mobile_number=='' and password=='' and con_password=='':
            messages.info(request, 'All the fields are empty please enter details..')
            return redirect('signup')
        elif full_name=='':
            messages.info(request, 'Full Name field is empty')
            return redirect('signup')
        elif username=='':
            messages.info(request, 'Username field is empty')
            return redirect('signup')
        elif email=='':
            messages.info(request, 'Email field is empty')
            return redirect('signup')
        elif mobile_number=='':
            messages.info(request, 'Mobile Number field is empty')
            return redirect('signup')
        elif password=='':
            messages.info(request, 'Password field is empty')
            return redirect('signup')
        elif con_password=='':
            messages.info(request, 'Conform Password field is empty')
            return redirect('signup')
        
        if password==con_password:
            if full_name=='' or len(full_name)<=4:
                messages.info(request,'Your name must be atleast 5 characters')
                return redirect('signup')
            elif len(username)<=5 or username=='':
                messages.info(request, 'your username must be 5 characters')
                return redirect('signup')
            elif email=='':
                messages.info(request,'Oops! you have not entered your mail..')
                return redirect('signup')
            elif len(str(mobile_number)) <10 or len(str(mobile_number))>10 or str(mobile_number)=='':
                messages.info(request, 'Please enter a valid mobile number')
                return redirect('signup')
            elif len(password) <8 :
                messages.info(request, 'Your password must be greater than or equal to 8 characters..')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'username already exists ')
                return redirect('signup')

            elif Datasave.objects.filter(full_name=full_name,mobile_number=mobile_number,email=email).exists():
                messages.info(request,'mobile number or email  already exists ')
                return redirect('signup')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                data=Datasave(full_name=full_name,mobile_number=mobile_number,email=email)
                data.save()
                user.set_password(password)
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'passwords does not match')
            return redirect('signup')
    else:
        return render(request, 'signup.html')
@csrf_protect
def logout(request):
    auth.logout(request)
    return redirect('/')
@csrf_protect
def delete(request,id):
    if request.method=='GET':
        post=Blogpost.objects.get(id=id)
        post.delete()
        return redirect('/')
    return render(request, 'homepage.html')
otp=random.randint(100000,999999)
@csrf_protect
def generate_otp(request):
    if request.method=='POST':
        emailforgot=request.POST['emailforgot']
        if emailforgot=='':
            messages.info(request,'Please enter mail to continue')
            return redirect('generate_otp')
        elif User.objects.filter(email=emailforgot).exists():
            messages.info(request,'Entered mail is correct')
            server=smtplib.SMTP('smtp.gmail.com',587)
            server.starttls()
            server.login('liveforothers129@gmail.com' ,'utaplhilwnfyjdcc')
            msg=f'Hello,Mr.person we are from live for others. You are requested to reset your password  \n  Your otp is '+str(otp)
            server.sendmail('parveensayedbhai1234@gmail.com',emailforgot ,msg)
            server.quit()
            return redirect('password_reset')
        else:
            messages.info(request,'please enter your registered email')
            return redirect('generate_otp')
    else:
        return render(request,'getotp.html',{'otp':otp}) 
@csrf_protect
def password_reset(request):
    if request.method=='POST':
        username=request.POST['username']
        otp_check=request.POST['otp_check']
        password1=request.POST['password1']
        password2=request.POST['password2']
        
        if username=='' and password1=='' and password2=='' and str(otp_check)=='':
            messages.info(request,'please enter details to continue..')
            return redirect('password_reset')
        if username=='':
            messages.info(request,'please enter your username')
            return redirect('password_reset')
        elif str(otp_check)=='':
            messages.info(request,'please enter your new password')
            return redirect('password_reset')
        elif password1=='' :
            messages.info(request,'please enter your new password')
            return redirect('password_reset')
        elif len(password1)<8 :
            messages.info(request,'Password length must greater than 7 characters.')
            return redirect('password_reset')
        elif password2=='':
            messages.info(request,'please re-enter your new password')
            return redirect('password_reset')
        if User.objects.filter(username=username).exists():
            if str(otp)== str(otp_check):
                if password1==password2:
                    user=User.objects.get(username=username)
                    user.set_password(password1)
                    user.save()
                    return redirect('login')
                else:
                    messages.info(request,'password does not match')
                    return redirect('password_reset')
            else:
                messages.info(request,'Oops! your otp is invalid')
                return redirect('password_reset')

        else:
            messages.info(request,'email or username does not exist')
            return redirect('password_reset')

    return render(request,'password_reset.html')
