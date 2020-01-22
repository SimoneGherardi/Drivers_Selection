from django.shortcuts import render
from django.forms import modelformset_factory
import time
from geopy.distance import geodesic
from .forms import *

from .models import *


def delete_passenger_data(Passengers):
    for passenger in Passengers:
        passenger.delete()
    return


def delete_driver_data(Drivers):
    for driver in Drivers:
        driver.delete()
    return


def delete_destination_data(Destination):
    for destination in Destination:
        destination.delete()
    return



def save_data(instances):
    for instance in instances:
        instance.starting_place = Place.objects.create(address=instance.address, city=instance.city, zip_code=instance.zip_code,
                                        country_code=instance.country_code, is_destination=False)
        instance.starting_place.set_coordinates()
        instance.save()

    return


def collecting_data_view(request):
#    passengerFormSet = modelformset_factory(Passenger, fields=('first_name', 'last_name', 'address', 'city', 'zip_code', 'country_code'))
#    driverFormSet = modelformset_factory(Driver, fields=('first_name', 'last_name', 'address', 'city', 'zip_code', 'country_code', 'car_name', 'fuel_type', 'fuel_consumption', 'available_seats'))
#    destinationFormSet = modelformset_factory(Place, fields=('address', 'city', 'zip_code', 'country_code'))

    passengerFormSet = modelformset_factory(Passenger, form=PassengerForm, fields=('first_name', 'last_name', 'address', 'city', 'zip_code', 'country_code'))
    driverFormSet = modelformset_factory(Driver, form=DriverForm, fields=('first_name', 'last_name', 'address', 'city', 'zip_code', 'country_code', 'car_name', 'fuel_type', 'fuel_consumption', 'available_seats'))
    destinationFormSet = modelformset_factory(Place, form=PlaceForm, fields=('address', 'city', 'zip_code', 'country_code'))

    if request.method == "POST" and 'passengers submit' in request.POST:
        passenger_form = passengerFormSet(request.POST)
        instances = passenger_form.save(commit=False)
        save_data(instances)

    passenger_form = passengerFormSet(queryset=Passenger.objects.none())
    passengers = Passenger.objects.all()

    if request.method == "POST" and 'drivers submit' in request.POST:
        driver_form = driverFormSet(request.POST)
        instances = driver_form.save(commit=False)
        save_data(instances)

    driver_form = driverFormSet(queryset=Passenger.objects.none())
    drivers = Driver.objects.all()

    if request.method == "POST" and 'destination submit' in request.POST:
        destination_form = destinationFormSet(request.POST)
        instances = destination_form.save(commit=False)
        destination = Place.objects.all()
        for instance in instances:
            delete_destination_data(destination)
            instance.set_coordinates()
            instance.is_destination = True
            print(instance.is_destination)
            instance.save()
    destination_form = destinationFormSet(queryset=Passenger.objects.none())
    destination = Place.objects.all()

    for passenger in passengers:
        print(passenger.starting_place.coordinates)

    if request.method == "POST" and 'remove data' in request.POST:
        delete_passenger_data(passengers)
        delete_driver_data(drivers)
        delete_destination_data(destination)

    return render(request, 'Drivers_Selection/collecting_data_template.html', {'passenger_form': passenger_form, 'driver_form': driver_form, 'destination_form': destination_form, 'passengers': passengers, 'drivers': drivers, 'destination': destination})


def create_scores_view(request):
    drivers = Driver.objects.all()
    passengers = Passenger.objects.all()
    places = Place.objects.all()
    destination = None
    for dest in places:
        if dest.is_destination:
            destination = dest
    for driver in drivers:
        print(driver.last_name)
        print(driver.starting_place)
    for passenger in passengers:
        print(passenger.last_name)
    print(destination.address)
    #   building the passengers_distance_matrix aka passenger_matrix
    p_rows_number = len(drivers)
    print(p_rows_number)
    p_cols_number = len(passengers)
    print(p_cols_number)
    i = 0
    j = 0
    passenger_matrix = [[0 for x in range(p_rows_number)] for y in range(p_cols_number)]
    for driver in drivers:
        for passenger in passengers:
            passenger_matrix[j][i] = round(geodesic(driver.starting_place.coordinates,
                                                    passenger.starting_place.coordinates).km, 4)
            time.sleep(1)

#    for i in range(p_rows_number):
#        for j in range(p_cols_number):


#    for i in range(p_rows_number):
#        for j in range(p_cols_number):
#            print(passenger_matrix[j][i])

    # building the destination_distance_matrix aka the distance_matrix
#    if destination is not None:
#        destination_matrix = [[0 for x in range(p_rows_number)] for y in range(2)]
#        for i in range(p_rows_number):
#            for j in range(1):
#                destination_matrix[j][i] = round(geodesic(drivers[i].starting_place.coordinates,
#                                                          destination.coordinates).km, 4)
#                time.sleep(1)
#    else:
#        destination_matrix = []

    return render(request, 'Drivers_Selection/show_scores_template.html', {'passengers': passengers, 'drivers': drivers, 'destination': destination})
