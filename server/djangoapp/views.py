from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
# Create an `about` view to render a static about page
def index(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)

# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_user(request):
    context = {}
    if request.method == "POST":
        user = request.POST['username']
        password = request.POST['psw']
        logon_user = authenticate(username=user, password=password)
        if logon_user is not None:
            login(request, logon_user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password, please try again."
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)


# Create a `logout_request` view to handle sign out request
def logout_user(request):
    # print("Signing out: `{}`, good bye!".format(request.user.username))  Get the user object based on session id in request
    logout(request) # Logout user in the request
    return redirect('djangoapp:index') # Redirect user back to previous view

# Create a `registration_request` view to handle sign up request
def user_registration(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST': # Record new User's Data
        new_user = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False # Verify User Identity
        try:
            User.objects.get(username=new_user)
            user_exist = True
        except:
            logger.error("New user")
    if not user_exist:
        user = User.objects.create_user(username=new_user, first_name=first_name, last_name=last_name, password=password)
        login(request, user)
        return redirect("djangoapp:index")
    else:
        context['message'] = "A User under this name has already been created, please try again."
        return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
 def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/802304f3-f623-4143-9b89-bd84ebf3d479/dealerships/dealer-get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

