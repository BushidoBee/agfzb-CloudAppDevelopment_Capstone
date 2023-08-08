from django.db import models
from django.utils.timezone import now
import datetime

# Class CarMake w/ Name and Description Fields
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=20, primary_key=True)
    descript = models.TextField()

    def __str__(self):
        return "Name: " + self.name + "," \
                "Description: " + self.descript

# Class CarModel w/ Unique ID, Make, Name, Vehicle Type, Model Type, and Year Fields
class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField(null=False)
    name = models.CharField(null=False, max_length=20, primary_key=True)
    SUV = 'suv'
    SEDAN = 'sedan'
    COUPE = 'coupe'
    VAN = 'van'
    VEHICLE_TYPE = [(SUV, 'SUV'),(SEDAN, 'Sedan'),(COUPE, 'coupe'),(VAN, 'van')]
    model_type = models.CharField(max_length=5, choices=VEHICLE_TYPE)
    year = models.IntegerField(default=datetime.date.today().year)
    
    def __str__(self):
        return  "Make: " + self.make.name + "," \
                "Name: " + self.name + "," \
                "Year: " + str(self.year) + "," \
                "Type: " + self.model_type + "," \
                "Dealer ID: " + str(self.dealer_id)

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
