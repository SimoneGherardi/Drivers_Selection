import geopy
from django import forms
from django.contrib.gis.db import models
from django.forms import ModelForm
from geopy import Point
from geopy.geocoders import Nominatim
from django.contrib.postgres.fields import ArrayField


class Car(models.Model):
    # to be changed
    car_name = models.CharField(max_length=50)
    fuel_type = models.CharField(max_length=50)
    fuel_consumption = models.FloatField


class Place(models.Model):
    address = models.CharField(max_length=100)
    coordinates = geopy.point.Point
    city = models.CharField(max_length=100, default='')
    country_code = models.CharField(max_length=2, default='')
    zip_code = models.CharField(max_length=20, default='')
    is_valid = models.BooleanField(default=False)
    is_destination = models.BooleanField(default=False)

    def set_coordinates(self):
        geo_locator = Nominatim(user_agent="distance_collector")
        nom = Nominatim(domain='localhost:8000', scheme='http')
        my_query = dict({'street': self.address, 'city': self.city, 'postalcode': self.zip_code})
        nominatim_data = geo_locator.geocode(query=my_query, exactly_one=True, timeout=20,
                                             country_codes=self.country_code)
        if nominatim_data is None:
            print("Wrong Address Format")
            self.is_valid = False
            return None

        self.is_valid = True
        self.coordinates = nominatim_data.point
        #        print(self.coordinates)

        return self


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)


class Passenger(Person):
    address = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    zip_code = models.CharField(max_length=20, default='')
    country_code = models.CharField(max_length=2, default='')
    starting_place = models.ForeignKey(Place, related_name='starting_place', on_delete=models.PROTECT, null=True)
#    destination_place = models.ForeignKey(Place, related_name='destination_place', on_delete=models.PROTECT, null=True)
    time_of_appearance = models.TimeField
    endurance_time = models.DurationField
    habit = models.FloatField(default=0)


class Driver(Passenger):

    #    ELECTRICAL = 'EC'
    #    DIESEL = 'DS'
    #    PETROL = 'PT'
    #    GAS = 'GS'
    #    FUEL_TYPE_CHOICES = (
    #        ('EC', 'Electrical'),
    #        ('DS', 'Diesel'),
    #        ('PT', 'Petrol'),
    #        ('GS', 'Gas'),
    #    )

    is_driving = models.BooleanField
    car_name = models.CharField(max_length=50, default='')
    fuel_type = models.CharField(max_length=2, default='')
    fuel_consumption = models.FloatField(default=0)
    available_seats = models.IntegerField(default=0)

    #   better use Serializer
    def to_json(self):
        return {"last_name": self.last_name, "first_name": self.first_name}


class Trip(models.Model):
    passengers = models.ManyToManyField(Passenger, related_name='not_driving_passengers')
    drivers = models.ManyToManyField(Driver, related_name='driving_passengers')
    destination = Place
    date = models.DateField
    arrival_time = models.TimeField

    def add_passenger(self, passenger):
        self.passengers.add(passenger)

    def add_driver(self, driver):
        self.drivers.add(driver)


class PassengerForm(ModelForm):
    class Meta:
        model = Passenger
        fields = ['first_name', 'last_name', 'address', 'city', 'zip_code', 'country_code', 'habit']


class DriverForm(ModelForm):
    #    fuel_type = forms.ChoiceField(widget=forms.RadioSelect, choices=FUEL_TYPE_CHOICES)

    class Meta:
        model = Driver
        fields = ['first_name', 'last_name', 'address', 'city', 'zip_code', 'country_code', 'car_name', 'fuel_type',
                  'fuel_consumption', 'available_seats', 'habit']


class PlaceForm(ModelForm):
    class Meta:
        model = Place
        fields = ['address', 'city', 'zip_code', 'country_code']


class Matrix(models.Model):
    name = models.CharField(max_length=100, default='')

    def get_val(self, row_index, col_index):
        cell = Cell.objects.get(row=row_index, col=col_index)
        return cell.val


class Cell(models.Model):
    matrix = models.ForeignKey(Matrix, on_delete=models.CASCADE)
    row = models.IntegerField(default=0)
    col = models.IntegerField(default=0)
    val = models.FloatField(default=0)


class Rank(models.Model):
    name = models.CharField(max_length=100, default='')


class RankElement(models.Model):
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE)
    position_in_rank = models.IntegerField(default=0)
    id_element = models.IntegerField(default=0)
    score = models.FloatField(default=0)
