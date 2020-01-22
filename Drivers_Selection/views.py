import json
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


def save_data_passenger(instances):
    for instance in instances:
        instance.starting_place = Place.objects.create(address=instance.address, city=instance.city, zip_code=instance.zip_code,
                                        country_code=instance.country_code, is_destination=False)
        instance.starting_place.set_coordinates()
        if instance.starting_place.is_valid:
            print(instance.starting_place.coordinates)
            instance.save()
    return


def get_all_passengers():
    passengers = Passenger.objects.all()
    for passenger in passengers:
        if passenger.starting_place.is_valid is False:
            passenger.starting_place.set_coordinates()
    return passengers


def get_all_drivers():
    drivers = Driver.objects.all()
    for driver in drivers:
        if driver.starting_place.is_valid is False:
            driver.starting_place.set_coordinates()
    return drivers


def get_all_places():
    places = Place.objects.all()
    for place in places:
        if place.is_valid is False:
            place.set_coordinates()
    return places


def remove_old_destination():
    places = get_all_places()
    for place in places:
        if place.is_destination:
            place.is_destination = False
            place.save()
    return

def get_json_drivers(drivers):
    drivers_json_str = "["
    for driver in drivers:
        drivers_json_str += json.dumps(driver.to_json())
        drivers_json_str += ','
    drivers_json_str = drivers_json_str[:-1]
    drivers_json_str += "]"
    return drivers_json_str

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
        save_data_passenger(instances)

    passenger_form = passengerFormSet(queryset=Passenger.objects.none())

    if request.method == "POST" and 'drivers submit' in request.POST:
        driver_form = driverFormSet(request.POST)
        instances = driver_form.save(commit=False)
        save_data_passenger(instances)

    driver_form = driverFormSet(queryset=Passenger.objects.none())

    if request.method == "POST" and 'destination submit' in request.POST:
        destination_form = destinationFormSet(request.POST)
        instances = destination_form.save(commit=False)
        destination = get_all_places()
        for instance in instances:
            remove_old_destination()
            instance.set_coordinates()
            instance.is_destination = True
            print(instance.is_destination)
            instance.save()
    destination_form = destinationFormSet(queryset=Passenger.objects.none())

    passengers = get_all_passengers()
    drivers = get_all_drivers()
    destination = get_all_places()

    for passenger in passengers:
        print(passenger.last_name)
        print(passenger.starting_place.coordinates)

    if request.method == "POST" and 'remove data' in request.POST:
        delete_passenger_data(passengers)
        delete_driver_data(drivers)
        delete_destination_data(destination)

    return render(request, 'Drivers_Selection/collecting_data_template.html', {'passenger_form': passenger_form, 'driver_form': driver_form, 'destination_form': destination_form, 'passengers': passengers, 'drivers': drivers, 'destination': destination})


def create_scores_view(request):
    drivers = get_all_drivers()
    passengers = get_all_passengers()
    places = get_all_places()

    destination = None
    for dest in places:
        if dest.is_destination:
            destination = dest

    for driver in drivers:
        print(driver.last_name)
        print(driver.starting_place.coordinates)

    for passenger in passengers:
        print(passenger.last_name)
        print(passenger.starting_place.coordinates)

    print(destination.address)
    #   building the passengers_distance_matrix aka passenger_matrix
    p_rows_number = len(drivers)
    print(p_rows_number)
    p_cols_number = len(passengers)
    print(p_cols_number)
    i = 0
    j = 0
    passengers_matrix = [[0 for x in range(p_rows_number)] for y in range(p_cols_number)]
    for driver in drivers:
        for passenger in passengers:
            passengers_matrix[j][i] = round(geodesic(driver.starting_place.coordinates,
                                                    passenger.starting_place.coordinates).km, 4)
            time.sleep(1)
            j += 1
        j = 0
        i += 1
    print(i)
    print(j)
    json_drivers = get_json_drivers(drivers)
#    passengers_matrix = Matrix.objects.create(name="passenger_matrix")
#    i, j = 0, 0
#    for driver in drivers:
#        for passenger in passengers:
#            Cell.objects.create(matrix="passenger_matrix", row=i, col=j, val=passenger_matrix[j][i])
#            time.sleep(1)
#            j += 1
#        j = 0
#        i += 1
#    passengers_cells = Cell.objects.all()
#    for i in range(p_rows_number):
#        for j in range(p_cols_number):

    for i in range(p_rows_number):
        for j in range(p_cols_number):
            print(passengers_matrix[j][i])

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

    return render(request, 'Drivers_Selection/show_tables_template.html', {'passengers': passengers, 'drivers': drivers, 'destination': destination, 'passengers_matrix': passengers_matrix, 'drivers_number': p_rows_number, 'passengers_number': p_cols_number, 'json_drivers': json_drivers})
