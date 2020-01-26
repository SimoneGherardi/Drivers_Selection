import json
from django.shortcuts import render
from django.forms import modelformset_factory
import time
from geopy.distance import geodesic
from .models import *


def delete_passenger_data():
    Passenger.objects.all().delete()


def delete_driver_data():
    Driver.objects.all().delete()


def delete_place_data():
    Place.objects.all().delete()


def delete_rank_data():
    Rank.objects.all().delete()


def clear_all_data(request, passenger_form, driver_form, destination_form, passengers, drivers, places):
    delete_passenger_data()
    delete_place_data()
    delete_rank_data()
    return render(request, 'Drivers_Selection/collecting_data_template.html',
                  {'passenger_form': passenger_form, 'driver_form': driver_form, 'destination_form': destination_form,
                   'passengers': passengers, 'drivers': drivers, 'destination': places})


def remove_old_destination():
    places = Place.objects.all()
    for place in places:
        if place.is_destination:
            place.is_destination = False
            place.save()
    return


def save_data_passenger(instances):
    for instance in instances:
        instance.starting_place = Place.objects.create(address=instance.address, city=instance.city,
                                                       zip_code=instance.zip_code,
                                                       country_code=instance.country_code, is_destination=False,
                                                       is_valid=False)
        instance.starting_place.set_coordinates()
        if instance.starting_place.is_valid:
            print(instance.starting_place.coordinates)
            instance.save()
    return


# returns passengers with coordinates set
def get_all_passengers():
    passengers = Passenger.objects.all()
    for passenger in passengers:
        if passenger.starting_place.is_valid is False:
            passenger.starting_place.set_coordinates()
    return passengers


# returns drivers with coordinates set
def get_all_drivers():
    drivers = Driver.objects.all()
    for driver in drivers:
        if driver.starting_place.is_valid is False:
            driver.starting_place.set_coordinates()
    return drivers


# returns places with coordinates set
def get_all_places():
    places = Place.objects.all()
    for place in places:
        if place.is_valid is False:
            place.set_coordinates()
    return places


def get_index_from_queryset_from_id(queryset, element_id):
    for index, el in enumerate(queryset):
        if el.id == element_id:
            return index


def get_json_drivers(drivers):
    drivers_json_str = "["
    for driver in drivers:
        drivers_json_str += json.dumps(driver.to_json())
        drivers_json_str += ','
    drivers_json_str = drivers_json_str[:-1]
    drivers_json_str += "]"
    return drivers_json_str


def get_enrivomental_impact(fuel_type):
    #    ELECTRICAL = 'EC'
    #    DIESEL = 'DS'
    #    PETROL = 'PT'
    #    GAS = 'GS'
    if fuel_type == "ec" or fuel_type == "EC" or fuel_type == "Ec" or fuel_type == "eC":
        return 10
    if fuel_type == "gs" or fuel_type == "GS" or fuel_type == "Gs" or fuel_type == "gS":
        return 0.7
    if fuel_type == "pt" or fuel_type == "PT" or fuel_type == "Pt" or fuel_type == "pT":
        return 0.5
    if fuel_type == "ds" or fuel_type == "DS" or fuel_type == "Ds" or fuel_type == "dS":
        return 0.2
    return 0.1


# returns the number of the first drivers that must be selected for rank_elements scores in order to provide a lift for every passenger
def get_enough_drivers(rank_elements, drivers):
    # get passengers number
    passengers_number = Passenger.objects.count()
    i = 0
    for rank_element in rank_elements:
        driver_seats = drivers.get(id=rank_element.id_element).available_seats
        passengers_number -= drivers.get(id=rank_element.id_element).available_seats
        i += 1
        if passengers_number <= 0:
            return i
    return 0


def create_rank_from_scores(rank_name, drivers, scores):
    rows_number = len(drivers)
    if Rank.objects.filter(name=rank_name).exists():
        Rank.objects.filter(name=rank_name).delete()
    rank_ref = Rank.objects.create(name=rank_name)
    ordered_scores = list()
    for index in range(rows_number):
        tmp_max = max(scores)
        index_max = scores.index(tmp_max)
        ordered_scores.append(tmp_max)
        scores[index_max] = -1
        print(ordered_scores[index], drivers[index_max].last_name)
        RankElement.objects.create(rank=rank_ref, position_in_rank=index + 1, id_element=drivers[index_max].id,
                                   last_name_element=drivers[index_max].last_name,
                                   score=round(ordered_scores[index], 4))


def relativize_scores_and_rank(rank_name, drivers, absolute_scores):
    val_max = max(absolute_scores)
    relative_scores = [x / val_max for x in absolute_scores]
    for element in relative_scores:
        if element < -1:
            element = -1
    create_rank_from_scores(rank_name, drivers, relative_scores)


def calculate_and_store_passengers_distance_scores(drivers, passengers, passengers_matrix):
    rows_number = len(drivers)
    absolute_scores = list()
    for index, driver in enumerate(drivers):
        absolute_scores.append(0)
    for indexd, driver in enumerate(drivers):
        for indexp, passenger in enumerate(passengers):
            if passengers_matrix[indexp][indexd] != 0:
                absolute_scores[indexd] += 1 / pow(passengers_matrix[indexp][indexd], 2)
    relativize_scores_and_rank("DP", drivers, absolute_scores)
    return absolute_scores


def calculate_and_store_destination_distance_scores(drivers, destination_matrix):
    rows_number = len(drivers)
    absolute_scores = list()
    absolute_scores = destination_matrix[0]
    relativize_scores_and_rank("DD", drivers, absolute_scores)
    return absolute_scores


def calculate_and_store_enviromental_impact_scores(drivers):
    absolute_scores = list()
    for driver in drivers:
        if get_enrivomental_impact(driver.fuel_type) == 10:
            absolute_scores.append(100)
        else:
            e = get_enrivomental_impact(driver.fuel_type)
            c = pow(driver.fuel_consumption, -1) * 100
            absolute_scores.append(e * c)
    relativize_scores_and_rank("EI", drivers, absolute_scores)
    return absolute_scores


def calculate_and_store_available_seats_scores(drivers):
    absolute_scores = list()
    for driver in drivers:
        absolute_scores.append(driver.available_seats)
    relativize_scores_and_rank("AS", drivers, absolute_scores)
    return absolute_scores


def calculate_and_store_habit_scores(drivers):
    absolute_scores = list()
    for driver in drivers:
        absolute_scores.append(driver.habit)
    relativize_scores_and_rank("Ha", drivers, absolute_scores)
    return absolute_scores


def calculate_and_store_total_scores(drivers):
    rows_number = len(drivers)
    total_scores = [0.0 for i in range(rows_number)]
    tmp_ranks = Rank.objects.all()
    ranks = list()
    for tmp in tmp_ranks:
        if tmp.name == "PD" or tmp.name == "EI" or tmp.name == "DD" or tmp.name == "AS" or tmp.name == "Ha":
            ranks.append(tmp)
    for rank in ranks:
        rank_elements = RankElement.objects.filter(rank=rank.id)
        for rank_element in rank_elements:
            total_scores[get_index_from_queryset_from_id(drivers, rank_element.id_element)] += rank_element.score
    create_rank_from_scores("TS", drivers, total_scores)


def calculate_and_store_long_distance_drivers_scores(drivers, absolute_dd_scores, TSrank):
    val_max = max(absolute_dd_scores)
    relative_dd_scores = [(x * 5 / val_max) for x in absolute_dd_scores]
    for rank_element in TSrank:
        relative_dd_scores[get_index_from_queryset_from_id(drivers, rank_element.id_element)] += rank_element.score
    create_rank_from_scores("LDD", drivers, relative_dd_scores)


def calculate_and_store_short_distance_drivers_scores(drivers, absolute_dd_scores, TSrank):
    val_max = max(absolute_dd_scores)
    relative_ld_scores = [(5 - x * 5 / val_max) for x in absolute_dd_scores]
    for rank_element in TSrank:
        relative_ld_scores[get_index_from_queryset_from_id(drivers, rank_element.id_element)] += rank_element.score
    create_rank_from_scores("SDD", drivers, relative_ld_scores)


def select_needed_drivers_from_rank(rank_elements, drivers):
    needed_drivers = list()
    enough_drivers = get_enough_drivers(rank_elements, drivers)
    for x, rank_element in enumerate(rank_elements):
        if x == enough_drivers:
            break
        needed_drivers.append(rank_element)
    return needed_drivers


def collecting_data_view(request):
    passengerFormSet = modelformset_factory(Passenger, form=PassengerForm, fields=(
        'first_name', 'last_name', 'address', 'city', 'zip_code', 'country_code'))
    driverFormSet = modelformset_factory(Driver, form=DriverForm, fields=(
        'first_name', 'last_name', 'address', 'city', 'zip_code', 'country_code', 'car_name', 'fuel_type',
        'fuel_consumption', 'available_seats', 'habit'))
    destinationFormSet = modelformset_factory(Place, form=PlaceForm,
                                              fields=('address', 'city', 'zip_code', 'country_code'))

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

    # no coordinates needed for already accepted record

    if request.method == "POST" and 'destination submit' in request.POST:
        destination_form = destinationFormSet(request.POST)
        instances = destination_form.save(commit=False)
        for instance in instances:
            remove_old_destination()
            instance.is_destination = True
            instance.set_coordinates()
            if instance.is_valid:
                instance.save()
    destination_form = destinationFormSet(queryset=Passenger.objects.none())

    places = Place.objects.all()
    passengers = Passenger.objects.all()
    drivers = Driver.objects.all()

    if request.method == "POST" and 'remove data' in request.POST:
        clear_all_data(request, passenger_form, driver_form, destination_form, passengers, drivers, places)



    return render(request, 'Drivers_Selection/collecting_data_template.html',
                  {'passenger_form': passenger_form, 'driver_form': driver_form, 'destination_form': destination_form,
                   'passengers': passengers, 'drivers': drivers, 'places': places})


def create_scores_view(request):
    drivers = get_all_drivers()
    passengers = get_all_passengers()
    places = get_all_places()
    destination = None
    for dest in places:
        if dest.is_destination:
            destination = dest
    destination.set_coordinates()

    print(destination.address)
    print(destination.coordinates)
    #   building the passengers_distance_matrix aka passenger_matrix
    rows_number = len(drivers)
    p_cols_number = len(passengers)
    i = 0
    j = 0
    passengers_matrix = [[0 for x in range(rows_number)] for y in range(p_cols_number)]
    for i, driver in enumerate(drivers):
        for j, passenger in enumerate(passengers):
            passengers_matrix[j][i] = round(geodesic(driver.starting_place.coordinates,
                                                     passenger.starting_place.coordinates).km, 4)
            time.sleep(1)
    json_drivers = get_json_drivers(drivers)

    destination_matrix = [[0 for x in range(rows_number)] for y in range(1)]
    for index, driver in enumerate(drivers):
        destination_matrix[0][index] = round(geodesic(driver.starting_place.coordinates,
                                                      destination.coordinates).km, 4)
        print(destination_matrix[0][index])

    calculate_and_store_passengers_distance_scores(drivers, passengers, passengers_matrix)

    calculate_and_store_destination_distance_scores(drivers, destination_matrix)

    calculate_and_store_enviromental_impact_scores(drivers)

    calculate_and_store_available_seats_scores(drivers)

    calculate_and_store_habit_scores(drivers)

    #   check operations
    ranks = Rank.objects.all()
    for rank in ranks:
        rank_elements = RankElement.objects.filter(rank=rank.id)
        print(rank.name)
        for rank_element in rank_elements:
            print(rank_element.position_in_rank, drivers.get(id=rank_element.id_element).last_name, rank_element.score)

    return render(request, 'Drivers_Selection/show_tables_template.html',
                  {'passengers': passengers, 'drivers': drivers, 'destination': destination,
                   'passengers_matrix': passengers_matrix, 'drivers_number': rows_number,
                   'passengers_number': p_cols_number, 'json_drivers': json_drivers,
                   'destination_matrix': destination_matrix})


def show_scores_view(request):
    drivers = get_all_drivers()
    DPrank = RankElement.objects.filter(rank=Rank.objects.get(name="DP"))
    EIrank = RankElement.objects.filter(rank=Rank.objects.get(name="EI"))
    DDrank = RankElement.objects.filter(rank=Rank.objects.get(name="DD"))
    ASrank = RankElement.objects.filter(rank=Rank.objects.get(name="AS"))
    Harank = RankElement.objects.filter(rank=Rank.objects.get(name="Ha"))
    partial_ranks = Rank.objects.exclude(name="TS")
    return render(request, 'Drivers_Selection/show_scores_template.html',
                  {'DPrank': DPrank, 'EIrank': EIrank, 'DDrank': DDrank, 'ASrank': ASrank, 'Harank': Harank,
                   'drivers': drivers})


def show_final_scores_view(request):
    drivers = get_all_drivers()
    calculate_and_store_total_scores(drivers)
    TSrank = RankElement.objects.filter(rank=Rank.objects.get(name="TS"))

    TS_needed_drivers = select_needed_drivers_from_rank(TSrank, drivers)

    for element in TS_needed_drivers:
        print(element)

    #   building the drivers_distance_matrix aka driver_matrix
    rows_number = len(drivers)
    absolute_dd_score = [0 for x in range(rows_number)]
    drivers_matrix = [[0 for x in range(rows_number)] for y in range(rows_number)]
    for i, driver_ext in enumerate(drivers):
        for j, driver_int in enumerate(drivers):
            if j > i:
                drivers_matrix[j][i] = round(geodesic(driver_ext.starting_place.coordinates,
                                                      driver_int.starting_place.coordinates).km, 4)
                drivers_matrix[i][j] = drivers_matrix[j][i]
            absolute_dd_score[i] += drivers_matrix[j][i]
            time.sleep(1)

    calculate_and_store_long_distance_drivers_scores(drivers, absolute_dd_score, TSrank)
    LDDrank = RankElement.objects.filter(rank=Rank.objects.get(name="LDD"))
    LDD_needed_drivers = select_needed_drivers_from_rank(LDDrank, drivers)

    calculate_and_store_short_distance_drivers_scores(drivers, absolute_dd_score, TSrank)
    SDDrank = RankElement.objects.filter(rank=Rank.objects.get(name="SDD"))
    SDD_needed_drivers = select_needed_drivers_from_rank(SDDrank, drivers)

    return render(request, 'Drivers_Selection/show_final_scores_template.html',
                  {'TSrank': TSrank, 'drivers': drivers, 'TS_needed_drivers': TS_needed_drivers, "LDDrank": LDDrank,
                   "LDD_needed_drivers": LDD_needed_drivers, "SDDrank": SDDrank,
                   "SDD_needed_drivers": SDD_needed_drivers})
