from django.db import IntegrityError
from django.shortcuts import render,redirect
from .models import Customers
from django.contrib.auth import authenticate
from django.views.decorators.cache import never_cache


# Create your views here.
@never_cache
def signup(request):
    if request.method=='POST':
        name=request.POST.get('name')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        try:
            user = Customers.objects.create(username=name, phone_no=phone, email=email, password=password)
            request.session['username'] = user.username
            return redirect('home')
        except IntegrityError:
            # Handle the case where the username already exists
            # You can render the signup form again with an error message
            error_message = "Username already exists. Please choose a different username."
            return render(request, 'signup.html', {'error_message': error_message})
        
    return render(request, 'signup.html')

@never_cache
def signin(request):
    if request.method=='POST':
        name=request.POST.get('name')
        password=request.POST.get('password')
        print(name)
        print(password)
        user=authenticate(request,username=name,password=password)
        print(user)
        if user is not None and user.is_active:
            print("authenticated")
            # User=Customers.objects.get(username=name)
            # request.session['username']=User.username
            return redirect('home')
    return render(request,'signin.html')