from django.db import models
from django.utils.timezone import now
import datetime

# Class CarMake w/ Name and Description Fields
class CarMake(models.Model):
    brand = models.CharField(null=False, max_length=20, primary_key=True)
    descript = models.CharField(max_length=1000)

    def __str__(self):
        return self.brand

# Class CarModel w/ Unique ID, Car Brands, Model, Vehicle Type, and Year Fields
class CarModel(models.Model):
    SUV = 'suv'
    SEDAN = 'sedan'
    TRUCK = 'truck'
    COUPE = 'coupe'
    CAR_TYPES = [(SEDAN, 'Sedan'),(SUV, 'Suv'),(TRUCK, 'Truck'),(COUPE, 'Coupe')]
    car_brand = models.ForeignKey(CarMake, on_delete=models.CASCADE, default='None')
    car_model = models.CharField(null=False, max_length=20)
    dealer_id = models.IntegerField(null=False)
    vehicle_type = models.CharField(max_length=5, choices=CAR_TYPES)
    year = models.DateField()
    
    def __str__(self):
        return  str(self.dealer_id)

# Class CustomerReviews w/ Unique ID, Customer, and the car they bought, and/or reviewed
class CustomerReview(models.Model):
    review_id = models.AutoField(null=False, primary_key=True, editable=False)
    customer_name = models.TextField(null=False, max_length=40)
    dealer_sale = models.IntegerField(null=False)
    make = models.CharField(null=False, max_length=20)
    model = models.CharField(null=False, max_length=20)
    year = models.DateField(null=False)
    car_sold = models.BooleanField()
    date_of_purchase = models.DateField()
    customer_review = models.TextField()
    submit_timestamp = models.TextField()

# Class CarDealer; Holds Basic Data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip
    
    def __str__(self):
        return "Dealer name: " + self.full_name

# Class DealerReview; Holds Basic Data
class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, vehicle_make, vehicle_model, vehicle_year, sentiment, dealerID):
        # Fields below cannot be empty
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        # These fields can be null
        self.purchase_date = purchase_date
        self.purchase_make = vehicle_make
        self.purchase_model = vehicle_model
        self.purchase_year = vehicle_year
        self.sentiment = sentiment
        self.id = id

    def __str__(self):
        return "Review: " + self.review

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
