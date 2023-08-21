from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL
urlpatterns = [
    path(route='', view=views.get_dealerships, name='index'),
    # path for about view
    path(route='index', view=views.index, name='index'),
    # path for about view
    path(route='about', view=views.about, name='about'),
    # path for contact us view
    path(route='contact', view=views.contact, name='contact'),

    # path for registration
    path(route='registration', view=views.user_registration, name='registration'),

    # path for login
    path(route='login', view=views.login_user, name='login'),

    # path for logout
    path(route='logout', view=views.logout_user, name='logout'),

    path(route='', view=views.get_dealerships, name='index'),

    # path for dealer reviews view
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),
    
    # path for add a review view
    path('review/<int:dealer_id>', view=views.add_review, name='add_review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
