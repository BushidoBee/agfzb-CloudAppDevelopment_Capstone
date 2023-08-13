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
        return  "Brand: " + str(self.car_brand) + " " + str(self.car_model) + " | Dealer #" + str(self.dealer_id)

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

    def __init__(self, dealership, name, purchase, review):
        # Fields below cannot be empty
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        # These fields can be null
        self.purchase_date = ""
        self.purchase_make = ""
        self.purchase_model = ""
        self.purchase_year = ""
        self.sentiment = ""
        self.id = ""

    def __str__(self):
        return "Review: " + self.review

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
