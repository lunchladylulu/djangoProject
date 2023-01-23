from django.db.models import Q

from .models import Review
import folium as folium
import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from myapp import support_functions
from myapp.models import Currency, AccountHolder, Itinerary
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

# This is a request-response. We create a dictionary so that the HTML template can understand Python.
# The render function sends the request and plants the result to home.html.
# Aka what do we want the action to do? One function for each html page.

from django.http import HttpResponseRedirect
from django.urls import reverse


def home(request):
    data = dict()
    import datetime
    time = datetime.datetime.now()
    data["time_of_day"] = time
    data["xy"] = "xy"
    print(time)
    return render(request, "home.html", context=data)


def maintenance(request):
    data = dict()
    try:
        choice = request.GET['selection']
        if choice == "currencies":
            support_functions.add_currencies(support_functions.get_currency_list())
            c_list = Currency.objects.all()
            print("Got c_list", len(c_list))
            data['currencies'] = c_list
            return HttpResponseRedirect(reverse('currencies'))

        elif choice == "fill_trip_db":
            support_functions.add_trips()
        elif choice == "delete_trip_db":
            support_functions.delete_trips()
    except:
        pass
    return render(request, "maintenance.html", context=data)


def view_currencies(request):
    data = dict()
    c_list = Currency.objects.all()
    data['currencies'] = c_list
    return render(request, 'currency-selection.html', context=data)


def currency_selection(request):
    data = dict()
    currencies = Currency.objects.all()
    data['currencies'] = currencies
    return render(request, "currency_selector.html", data)


def exch_rate(request):
    data = dict()
    try:
        currency1 = request.GET['currency_from']
        currency2 = request.GET['currency_to']
        c1 = Currency.objects.get(iso=currency1)
        c2 = Currency.objects.get(iso=currency2)
        try:
            user = request.user
            if user.is_authenticated:
                account_holder = AccountHolder.objects.get(user=user)
                account_holder.currencies_visited.add(c1)
                account_holder.currencies_visited.add(c2)
                data['currencies_visited'] = account_holder.currencies_visited.all()
        except:
            pass
        support_functions.update_xrates(c1)
        data['currency1'] = c1
        data['currency2'] = c2
        try:
            rate = c1.rates_set.get(x_currency=c2.iso).rate
            data['rate'] = rate
        except:
            data['rate'] = "Not Available"
    except:
        pass
    return render(request, "exchange_detail.html", data)


def register_new_user(request):
    context = dict()
    form = UserCreationForm(request.POST)
    if form.is_valid():
        new_user = form.save()
        dob = request.POST["dob"]
        acct_holder = AccountHolder(user=new_user, date_of_birth=dob)
        acct_holder.save()
        return render(request, "home.html", context=dict())
    else:
        form = UserCreationForm()
        context['form'] = form
        return render(request, "registration/register.html", context)


def voyagevault_home(request):
    data = dict()
    import datetime
    time = datetime.datetime.now()
    data["time_of_day"] = time
    data["xy"] = "xy"
    print(time)
    return render(request, "voyagevault_home.html", context=data)


def map1(request):
    m = folium.Map()
    data = dict()
    # RESET CODE GOES HERE
    try:
        request.GET['city_list']
        number_of_cities = int(request.GET['number_of_cities'])
        visiting_cities = list()
        for i in range(number_of_cities):
            name = "city" + str(i)
            city_name = request.GET[name]
            visiting_cities.append(city_name)
        m = support_functions.add_markers(m, visiting_cities)
        data['visiting_cities'] = visiting_cities
        m = m._repr_html_
        data['m'] = m
        return render(request, "map.html", data)
    except:
        pass
    # CITY NAMES AND NUMBER OF CITIES CODE GOES HERE
    return render(request, "map.html", context=data)


def map(request):
    m = folium.Map()  # add import folium at the top of views.py
    data = dict()
    try:
        request.GET['reset']
        print("resetting")
        data['number_of_cities'] = 0
        data['m'] = m._repr_html_
        return render(request, "map.html", context=data)
    except:
        pass
    try:
        number_of_cities = int(request.GET["number_of_cities"])
        if number_of_cities > 0:
            names = list()
            for i in range(number_of_cities):
                names.append("city" + str(i))
            data['names'] = names
            data['number_of_cities'] = number_of_cities
        m = m._repr_html_
        data['m'] = m
    except:
        data['number_of_cities'] = 0
        m = m._repr_html_
        data['m'] = m
    return render(request, "map.html", context=data)


def get_itinerary(request):
    data = dict()

    # result = Itinerary.objects.get(length=2, city="Los Angeles")
    length_input = int(request.GET['length'])
    city_input = request.GET['destination']
    data['length_input'] = length_input
    data['city_input'] = city_input

    results = Itinerary.objects.filter(length=length_input, city=city_input)
    data['trip_results'] = results
    return render(request, 'trip_result.html', context=data)


def west_coast(request):
    data = dict()
    temp_list = []

    data['west_coast_itineraries'] = "This is where a list of the itineraries will go."

    results = Itinerary.objects.filter(Q(city="Los Angeles") | Q(city="San Francisco"))
    for result in results:
        if (str(result.length) + " days in " + result.city) not in temp_list:
            temp_list.append((str(result.length) + " days in " + result.city))
        continue

    data['trip_results'] = results
    data['list_of_itineraries'] = temp_list

    return render(request, 'west_coast.html', context=data)


def form(request):
    data = dict()
    data['city_list'] = ['Los Angeles', 'San Francisco', 'New York', 'Chicago']
    data['len'] = [1, 2, 3, 4]
    data['time_of_day_list'] = ['morning', 'afternoon', 'evening']
    data['activity_type_list'] = ['food and drink', 'activity']
    return render(request, 'form.html', context=data)


def form_submit(request):
    data = dict()
    if request.method == 'POST':
        support_functions.fill_db_trips(request.POST)
    return render(request, 'form_submit.html', context=data)


def add_review(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            heading = request.POST['heading']
            review_body = request.POST['review_body']
            user = request.user
            review = Review(heading=heading, review_body=review_body, user=user)
            review.save()
            return redirect('reviews')
        else:
            return render(request, 'add_review.html')
        pass
    else:
        messages.warning(request, "Please log in to add a review.")
        return redirect('login')


def reviews(request):
    reviews = Review.objects.all()
    return render(request, 'reviews.html', {'user': request.user, 'reviews': reviews})


def east_coast(request):
    data = dict()
    temp_list = []

    data['east_coast_itineraries'] = "This is where a list of the itineraries will go."

    results = Itinerary.objects.filter(Q(city="New York") | Q(city="Chicago"))
    for result in results:
        if (str(result.length) + " days in " + result.city) not in temp_list:
            temp_list.append((str(result.length) + " days in " + result.city))
        continue

    data['trip_results'] = results
    data['list_of_itineraries'] = temp_list

    return render(request, 'west_coast.html', context=data)
