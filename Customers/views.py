from django.db import IntegrityError
from django.shortcuts import render,redirect
from .models import Customers
from django.contrib.auth import authenticate
from django.views.decorators.cache import never_cache
import random
from django.core.mail import send_mail
import time
from django.http import HttpResponseBadRequest
from django.urls import reverse

from allauth.socialaccount.models import SocialAccount

# Create your views here.

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp):
    print(email)
    print("entered")
    subject = 'Your OTP for Signup'
    message = f'Your OTP for signup is: {otp}'
    send_mail(subject, message, 'aawinachu123@gmail.com', [email])
    print("sended email")



def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        
        # Custom validation logic
        if not name:
            return render(request, 'signup.html', {'error_message': 'Name is required.'})
        
        if not email:
            return render(request, 'signup.html', {'error_message': 'Email is required.'})
        
        if Customers.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error_message': 'This email is already registered.'})
        
        if len(password) < 8:
            return render(request, 'signup.html', {'error_message': 'Password must be at least 8 characters long.'})
        
        
        
        
        
        
        # Generate OTP
        otp = generate_otp()
        print(otp)
        # Save OTP in session
        otp_creation_time = time.time()  # Record the current time
        request.session['otp'] = otp
        request.session['otp_creation_time'] = otp_creation_time
        request.session['signup_data'] = {
            'name': name,
            
            'email': email,
            'password': password
        }
        
        # Send OTP via email
        send_otp_email(email, otp)
        
        return render(request, 'otp_verification.html', {'email': email})
    
    return render(request, 'signup.html')



def verify_otp(request):
    if request.method == 'POST':
        print("yess")
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')
        otp_creation_time = request.session.get('otp_creation_time')
        
        if entered_otp == stored_otp:
            current_time = time.time()
            if current_time - otp_creation_time <= 30:  # Check if OTP is within 30 seconds
                signup_data = request.session.get('signup_data')
                
                
                try:
                    user = Customers.objects.create(username=signup_data['name'], email=signup_data['email'], password=signup_data['password'])
                except:
                    error_message = "A user with this username or email already exists."
            # Assuming you have a function to create user and log them in
            # Create user and redirect to home page
                del request.session['otp']
                del request.session['otp_creation_time']
                del request.session['signup_data']
                return redirect('home')
            else:
                print("otp expired")
                error_message = "OTP has expired. Please request a new OTP."
                
        else:
            error_message = "Invalid OTP. Please try again."
            
        return render(request, 'otp_verification.html', {'email': request.session.get('signup_data').get('email'), 'error_message': error_message})

    return redirect('signup')













@never_cache
# def signup(request):
#     if request.method=='POST':
#         name=request.POST.get('name')
#         email=request.POST.get('email')
#         password=request.POST.get('password')
        
#         try:
#             user = Customers.objects.create(username=name, email=email, password=password)
#             request.session['username'] = user.username
#             return redirect('home')
#         except IntegrityError:
#             # Handle the case where the username already exists
#             # You can render the signup form again with an error message
#             error_message = "Username already exists. Please choose a different username."
#             return render(request, 'signup.html', {'error_message': error_message})
        
#     return render(request, 'signup.html')

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