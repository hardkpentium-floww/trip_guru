from django.contrib import admin
from .models.destination import Destination
from .models.hotel import Hotel
from .models.user import  User
from .models.booking import Booking
from .models.rating import  Rating

class AdminHotelModel(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'tariff')  # Specify the fields to display


class DestinationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')  # Specify the fields to display


# Register the model with the custom admin class
admin.site.register(Destination, DestinationAdmin)
admin.site.register(Hotel, AdminHotelModel)
admin.site.register(Booking)
admin.site.register(User)
admin.site.register(Rating)