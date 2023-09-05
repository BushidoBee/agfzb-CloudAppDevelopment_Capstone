from django.contrib import admin
from .models import CarMake, CarModel, CustomerReview

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel

# CustomeReviewsAdmin class
class CustomerReviewAdmin(admin.ModelAdmin):
    list_display = ['review_id', 'customer_name', 'make', 'model', 'year', 'customer_review', 'date_of_purchase']
    search_fields = ['customer_name']

#  CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['car_brand', 'car_model', 'dealer_id', 'vehicle_type', 'year']
    search_fields = ['car_brand']
    EXTRA = 5

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ['brand', 'descript']
    search_fields = ['brand']

# Register models here
admin.site.register(CustomerReview, CustomerReviewAdmin)
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)