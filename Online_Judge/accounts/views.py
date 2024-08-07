from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.template import loader
from django.http import HttpResponse
from userprofile.models import UserProfile
# Create your views here.


app_name = 'accounts'
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username)

        if user.exists():
            messages.info(request, f'User with the username "{username}" already exists')
            return redirect("/auth/register/")
        
        user = User.objects.create_user(username=username)
        user.set_password(password)
        user.save()

        #Check if the user profile already exists
        if not UserProfile.objects.filter(user=user).exists():
            UserProfile.objects.create(user=user)
        
        messages.info(request, f'User with username "{username}" created successfully.')
        return redirect('/auth/register/')
    
    template = loader.get_template('register.html')
    context = {}
    return HttpResponse(template.render(context, request))


'''
def register_user(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username)

        if user.exists():
            messages.info(request, f'User with the username "{username}" already exists')
            return redirect("/auth/register/")
        
        user = User.objects.create_user(username=username)

        user.set_password(password)

        user.save()
        
        messages.info(request,f'User with username "{username}" created successfully.')
        return redirect('/auth/register/')
    
    template = loader.get_template('register.html')
    context = {}
    return HttpResponse(template.render(context,request))
'''

def login_user(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.info(request,f'User with username "{username}" does not exist.')
            return redirect('/auth/login/')
        
        user = authenticate(username=username, password=password)

        if user is None:
            messages.info(request,'invalid password')
            return redirect('/auth/login')
        

        login(request,user)
        #messages.info(request,'login successful')

        return redirect('/home/homepage/')
    
    template = loader.get_template('login.html')
    context ={}
    return HttpResponse(template.render(context,request))

def logout_user(request):
    logout(request)
    messages.info(request,'logout successfully')
    return redirect('/auth/login/')
    
