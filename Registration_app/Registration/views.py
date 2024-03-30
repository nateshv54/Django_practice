from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.shortcuts import redirect
from .models import user_details
from django.contrib import messages
import datetime
from django.views.decorators.csrf import csrf_protect
import random

import environ
env = environ.Env()
environ.Env.read_env()

def details_view(request):
    if request.method == 'POST':
        # Extract data from the HTML form
        name = request.POST.get('username')
        email = request.POST.get('email')

        # Check if the user already exists
        # if user_already_exists(email):
        #     template=loader.get_template('login.html')
        #     return HttpResponse(template.render())
        
        user_detail=user_details(name=name,email=email)
        user_detail.save()
        template=loader.get_template('success.html')
        subject="Registration Successful"
        message=f'Thank you {name} for Registering with us'
        from_email=env('GMAIL_USERNAME')
        user_email=[email]
        send_otp(email)

        send_mail(subject,message,from_email,user_email,fail_silently=False)
        return HttpResponse(template.render())

    # Load the details.html template for GET requests
    template = loader.get_template('details.html')
    return HttpResponse(template.render({}, request))

# def user_already_exists(email):
#     return user_details.objects.filter(email=email).exists()

def send_otp(email):
    otp=random.randint(1000,9999)
    print("OTP1")
    subject = "OTP for Login"
    message = f'YOur OTP for login is : {otp}'
    from_email = env('GMAIL_USERNAME')
    user_email = [email]
    send_mail(subject, message, from_email, user_email, fail_silently=False)
    

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        if user_details.objects.filter(email=username).exists():
            template = loader.get_template('login.html')
            otp = send_otp(username)
            request.session['otp'] = otp
            request.session['username'] = username
            return HttpResponse(template.render({'otp_generated': True, 'username': username}, request))
        else:
            messages.error(request, "User doesn't exist")
            template = loader.get_template('details.html')
            return HttpResponse(template.render({}, request))

    return HttpResponse(loader.get_template('login.html').render({}, request))


def login_success(request):
    template=loader.get_template('login_success.html')
    username1=user_details.objects.filter(email='nateshv121@gmail.com').first()
    return HttpResponse(template.render({'username1':username1},request))
def verify_otp_view(request):
    if request.method == 'POST':
        user_entered_otp = request.POST.get('otp')
        saved_otp = request.session.get('otp')
        otp_expiry = request.session.get('otp_expiry')

        if saved_otp and user_entered_otp == str(saved_otp) and datetime.datetime.now() < otp_expiry:
            # OTP is valid
            # Add your logic here for successful login
            template = loader.get_template('login_success.html')
            return HttpResponse(template.render({'username': request.session.get('username')}, request))
        else:
            messages.error(request, 'Invalid OTP. Please try again or go to the details page.')
            template = loader.get_template('login.html')
            return HttpResponse(template.render({'otp_validation_failed': True, 'username': request.session.get('username')}, request))

    return redirect('login')

def resend_otp_view(request):
    # Resend OTP to the user's email
    username = request.POST.get('username')
    otp = random.randint(100000, 999999)
    send_otp(username, otp)

    # Save the new OTP and its expiry time in the session
    request.session['otp'] = otp
    request.session['otp_expiry'] = datetime.datetime.now() + datetime.timedelta(minutes=5)

    messages.success(request, 'OTP resent to your email.')
    template = loader.get_template('login.html')
    return HttpResponse(template.render({'otp_generated': True, 'username': username}, request))
