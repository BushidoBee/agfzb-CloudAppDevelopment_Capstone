import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        if "apikey" in kwargs:
            response = requests.get(url, headers={
                                    'Content-Type': 'application/json'}, params=kwargs, auth=HTTPBasicAuth("apikey", kwargs["apikey"]))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)

    except Exception as e:
        print("Error ", e)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print(json_payload)
    print("POST from {} ".format(url))
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        print(json_data)
        return json_data
    except:
        print("Network exception occurred")

# Create a get_dealers_from_cf method to get dealers from a cloud function
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        all_dealers = json_result
        # For each dealer object
        for dealer in all_dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

def get_dealer_by_id_from_cf(url, dealerId):
    json_data = get_request(url, id=dealerId)
    if json_data:
        for select_dealer in json_data: # find the desired Dealer in the JSON data; set it into a variable
            dealer_info = select_dealer["doc"]
            if dealer_info['id'] == dealerId:                
                # Grab returned result and input into object to be returned
                dealer_info = CarDealer(address=dealer_info["address"],
                                        city=dealer_info["city"],
                                        full_name=dealer_info["full_name"],
                                        id=dealer_info["id"],
                                        lat=dealer_info["lat"],
                                        long=dealer_info["long"],
                                        short_name=dealer_info["short_name"],
                                        st=dealer_info["st"], zip=dealer_info["zip"]
                                        )
                return dealer_info # return the result


# Get reviews by dealer ID from cloud function
def get_dealer_reviews_from_cf(url, dealer_id):
    select_reviews = [] # create a blank array
    json_data = get_request(url) #, dealerId=dealer_id) # Connect to Cloud database using "url" and "dealerId"; store it as JSON Metadata
    select_dealer = dealer_id
    # If JSON Data is valid, make a new variable.
    if json_data:
        # Start a loop through reviews retrieved
        all_reviews = json_data
        for check_review in all_reviews:
            # Check for a purchase and set "None" to nullable fields (if needed)
            this_review = check_review["doc"]
            if this_review["dealership"] == select_dealer: # and this_review["purchase"] != "False":
                # Print information using DealerReview class in ".Models" to a Variable
                review_object = DealerReview(
                    dealership = this_review["dealership"],
                    name = this_review["name"],
                    purchase = this_review["purchase"],
                    review = this_review["review"],
                    # NULLable fields
                    purchase_date = this_review["purchase_date"],
                    vehicle_make = this_review["car_make"],
                    vehicle_model = this_review["car_model"],
                    vehicle_year = this_review["car_year"],
                    sentiment = analyze_review_sentiments(this_review["review"]),
                    dealerID = this_review["id"]
                )
                select_reviews.append(review_object) # Append to the final variable below
    return select_reviews
#            elif this_review["dealership"] == dealer_id:
#                review_object = DealerReview(
#                    dealership = this_review["dealership"],
#                    name = this_review["name"],
#                    purchase = this_review["purchase"],
#                    review = this_review["review"],
#                    purchase_date = None,
#                    vehicle_make = None,
#                    vehicle_model = None,
#                    vehicle_year = None,
#                    sentiment = None,
#                    dealerID = None
#                )

# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(dealer_review):
# - Call get_request() with specified arguments
    API_KEY = "FgM2B2exYJospESfrkNRgFqSL2MqU2bSzVwVfAJ6iYUg"
    NLU_URL = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/6e1a6e9c-7f7e-4a02-aff8-cde16269958c'
    authenticator = IAMAuthenticator(API_KEY)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2021-08-01', authenticator=authenticator)
# - Get the returned sentiment label such as Positive or Negative
    natural_language_understanding.set_service_url(NLU_URL)
    response = natural_language_understanding.analyze(text=dealer_review, features=Features(
        sentiment=SentimentOptions(targets=[dealer_review]))).get_result()
    label = json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']
    return(label)