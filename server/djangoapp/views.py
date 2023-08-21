from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, DealerReview
from .restapis import get_request, get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealer_by_id_from_cf
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
    if request.method == "GET":
        context = {} # create a blank array for rendering
        # Get dealers from the URL
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/802304f3-f623-4143-9b89-bd84ebf3d479/dealership-package/get-dealership"
        dealer_data = get_dealers_from_cf(url)
        # Concatenate all dealer's full name; insert into context for rendering
#        dealer_names = ' | '.join([dealer.full_name for dealer in dealer_data])
        context["ds_list"] = dealer_data
#        return HttpResponse(dealer_names) # Return a list of dealer name
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context = {} # create a blank array for rendering
        # Get dealers from the URL
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/802304f3-f623-4143-9b89-bd84ebf3d479/dealership-package/get-reviews"
        reviews_data = get_dealer_reviews_from_cf(url, dealer_id)
        context["review_list"] = reviews_data
        dealer_data = get_dealer_by_id_from_cf("https://us-south.functions.appdomain.cloud/api/v1/web/802304f3-f623-4143-9b89-bd84ebf3d479/dealership-package/get-dealership", dealer_id)
        context["dealer_list"] = dealer_data
#        return HttpResponse(reviews_data) # Return a list of dealer name
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/802304f3-f623-4143-9b89-bd84ebf3d479/dealership-package/post-reviews"
        dealer = get_dealer_by_id_from_cf(url, dealer_id)
        cars = CarModel.objects.filter(dealer_id=dealer_id)
        context["vehicles"] = cars
        context["dealer"] = dealer
    return render(request, 'djangoapp/add_review.html', context)

    if request.method == "POST":
        url = "https://us-south.functions.cloud.ibm.com/api/v1/namespaces/802304f3-f623-4143-9b89-bd84ebf3d479/actions/dealership-package/post-review"      
        if 'purchasecheck' in request.POST:
            was_purchased = True
        else:
            was_purchased = False
            cars = CarModel.objects.filter(dealer_id=dealer_id)
            for car in cars:
                if car.id == int(request.POST['car']):
                    review_car = car  
                    review = {}
                    review["time"] = datetime.utcnow().isoformat()
                    review["name"] = request.POST['name']
                    review["dealership"] = dealer_id
                    review["review"] = request.POST['content']
                    review["purchase"] = was_purchased
                    review["purchase_date"] = request.POST['purchasedate']
                    review["car_make"] = review_car.make.name
                    review["car_model"] = review_car.name
                    review["car_year"] = review_car.year.strftime("%Y")
        json_payload = {}
        json_payload["review"] = review
    response = post_request(url, json_payload, dealerId=dealer_id)
    return redirect("djangoapp:dealer_details", dealer_id=dealer_id)