from django.contrib import admin
from .models import *

admin.site.register(Person)
admin.site.register(Passenger)
admin.site.register(Driver)
admin.site.register(Place)
admin.site.register(Car)
admin.site.register(Trip)
