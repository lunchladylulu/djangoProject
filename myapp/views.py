import folium as folium
import requests
from django.shortcuts import render

from myapp import support_functions
from myapp.models import Currency, AccountHolder, Itinerary
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

# This is a request-response. We create a dictionary so that the HTML template can understand Python.
# The render function sends the request and plants the result to home.html.
# Aka what do we want the action to do? One function for each html page.

def home(request):
    data = dict()
    import datetime
    time = datetime.datetime.now()
    data["time_of_day"] = time
    data["xy"] = "xy"
    data["page"] ="home"
    print(time)
    return render(request, "home.html", context=data)

# def maintenance(request):
#     data = dict()
#     return render(request,"maintenance.html",context=data)

from django.http import HttpResponseRedirect
from django.urls import reverse
def maintenance(request):
    data = dict()
    try:
        choice = request.GET['selection']
        if choice == "currencies":
            support_functions.add_currencies(support_functions.get_currency_list())
            c_list = Currency.objects.all()
            print("Got c_list",len(c_list))
            data['currencies'] = c_list
            return HttpResponseRedirect(reverse('currencies'))

        elif choice == "fill_trip_db":
            support_functions.add_trips()
        elif choice == "delete_trip_db":
            support_functions.delete_trips()
    except:
        pass
    return render(request,"maintenance.html",context=data)


# def add_currencies(currency_list):
#     for currency in currency_list:
#         currency_name = currency[0]
#         currency_symbol = currency[1]
#         try:
#             c= Currency.objects.get(iso=currency_symbol)
#         except:
#             c = Currency(long_name=currency_name, iso=currency_symbol)
#         c.name = currency_name
#         c.save() #To test out the code, replace this by print(c)


def view_currencies(request):
    data = dict()
    c_list = Currency.objects.all()
    data['currencies'] = c_list
    return render(request, 'currency-selection.html', context=data)


def currency_selection(request):
    data = dict()
    currencies =Currency.objects.all()
    data['currencies'] = currencies
    return render(request,"currency_selector.html",data)


def exch_rate(request):
    data=dict()
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
    return render(request,"exchange_detail.html",data)


def register_new_user(request):
    context = dict()
    form = UserCreationForm(request.POST)
    if form.is_valid():
        new_user = form.save()
        dob = request.POST["dob"]
        acct_holder = AccountHolder(user=new_user,date_of_birth=dob)
        acct_holder.save()
        return render(request,"home.html",context=dict())
    else:
        form = UserCreationForm()
        context['form'] = form
        return render(request, "registration/register.html", context)


def tripapp_home(request):
    data = dict()
    import datetime
    time = datetime.datetime.now()
    data["time_of_day"] = time
    data["xy"] = "xy"
    print(time)
    return render(request, "tripapp_home.html", context=data)





# def exch_rate(request):
#     data=dict()
#     try:
#         destination = request.GET['destination']
#         length = request.GET['length']
#         itinerary = Itinerary.objects.get(length = "1")
#         c2 = Currency.objects.get(iso=currency2)
#         support_functions.update_xrates(c1)
#         data['currency1'] = c1
#         data['currency2'] = c2
#         try:
#             rate = c1.rates_set.get(x_currency=c2.iso).rate
#             data['rate'] = rate
#         except:
#             data['rate'] = "Not Available"
#     except:
#         pass
#     return render(request,"exchange_detail.html",data)

def map1(request):
    m = folium.Map()
    data = dict()
    #RESET CODE GOES HERE
    try:
        request.GET['city_list']
        number_of_cities = int(request.GET['number_of_cities'])
        visiting_cities = list()
        for i in range(number_of_cities):
            name = "city"+str(i)
            city_name = request.GET[name]
            visiting_cities.append(city_name)
        m = support_functions.add_markers(m,visiting_cities)
        data['visiting_cities'] = visiting_cities
        m = m._repr_html_
        data['m'] = m
        return render(request,"map.html",data)
    except:
        pass
    #CITY NAMES AND NUMBER OF CITIES CODE GOES HERE
    return render(request,"map.html",context=data)


def map(request):
    m = folium.Map() #add import folium at the top of views.py
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
                names.append("city"+str(i))
            data['names'] = names
            data['number_of_cities'] = number_of_cities
        m = m._repr_html_
        data['m'] = m
    except:
        data['number_of_cities'] = 0
        m = m._repr_html_
        data['m'] = m
    return render(request,"map.html",context=data)



def get_itinerary(request):
    data = dict()

    #result = Itinerary.objects.get(length=2, city="Los Angeles")
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

    results = Itinerary.objects.filter(city="Los Angeles")
    for result in results:
        if (str(result.length) + " days in " + result.city) not in temp_list:
            temp_list.append((str(result.length) + " days in " + result.city))
        continue

    data['trip_results'] = results
    data['list_of_itineraries'] = temp_list

    return render(request, 'west_coast.html', context=data)


# def west_coast_link(request):
#
#     results = Itinerary.objects.filter(city="Los Angeles")
#     for itineraries in results:
#         if (str(result.length) + " days in " + result.city) not in temp_list:
#             temp_list.append((str(result.length) + " days in " + result.city))
#         continue
#
#     data['trip_results'] = results
#     data['list_of_itineraries'] = temp_list
#
#     return render(request, 'west_coast.html', context=data)


# def form(request):
#     data = dict()
#     data['temp'] = "temp"
#     return render(request, 'form.html', context=data)


def form(request):
    data=dict()
    # dob = request.POST["dob"]
    # return render(request,"fo.html",context=dict())
    # else:
    #     form = UserCreationForm()
    #     context['form'] = form
    #     return render(request, "registration/register.html", context)
    # len_input = request.GET['length_1']
    # cit_input = request.GET['city_1']
    # time_of_day_input = request.GET['time_of_day_1']
    # activity_type_input = request.GET['activity_type_1']
    # day_1_input = request.GET['day_1_1']
    # day_2_input = request.GET['day_2_1']
    # day_3_input = request.GET['day_3_1']
    # day_4_input = request.GET['day_4_1']
    #
    # Itinerary(length=len_input, city=cit_input, time_of_day = time_of_day_input, activity_type=activity_type_input,
    #             day_1=day_1_input, day_2=day_2_input,day_3=day_3_input, day_4=day_4_input).save()
    #
    # len_input = request.GET['length_2']
    # cit_input = request.GET['city_2']
    # time_of_day_input = request.GET['time_of_day_2']
    # activity_type_input = request.GET['activity_type_2']
    # day_1_input = request.GET['day_1_2']
    # day_2_input = request.GET['day_2_2']
    # day_3_input = request.GET['day_3_2']
    # day_4_input = request.GET['day_4_2']
    #
    # Itinerary(length=len_input, city=cit_input, time_of_day=time_of_day_input, activity_type=activity_type_input,
    #           day_1=day_1_input, day_2=day_2_input, day_3=day_3_input, day_4=day_4_input).save()
    #
    # len_input = request.GET['length_3']
    # cit_input = request.GET['city_3']
    # time_of_day_input = request.GET['time_of_day_3']
    # activity_type_input = request.GET['activity_type_3']
    # day_1_input = request.GET['day_1_3']
    # day_2_input = request.GET['day_2_3']
    # day_3_input = request.GET['day_3_3']
    # day_4_input = request.GET['day_4_3']
    #
    # Itinerary(length=len_input, city=cit_input, time_of_day=time_of_day_input, activity_type=activity_type_input,
    #           day_1=day_1_input, day_2=day_2_input, day_3=day_3_input, day_4=day_4_input).save()
    #
    # len_input = request.GET['length_4']
    # cit_input = request.GET['city_4']
    # time_of_day_input = request.GET['time_of_day_4']
    # activity_type_input = request.GET['activity_type_4']
    # day_1_input = request.GET['day_1_4']
    # day_2_input = request.GET['day_2_4']
    # day_3_input = request.GET['day_3_4']
    # day_4_input = request.GET['day_4_4']
    #
    # Itinerary(length=len_input, cit=cit_input, time_of_day=time_of_day_input, activity_type=activity_type_input,
    #           day_1=day_1_input, day_2=day_2_input, day_3=day_3_input, day_4=day_4_input).save()
    #
    # len_input = request.GET['length_5']
    # cit_input = request.GET['city_5']
    # time_of_day_input = request.GET['time_of_day_5']
    # activity_type_input = request.GET['activity_type_5']
    # day_1_input = request.GET['day_1_5']
    # day_2_input = request.GET['day_2_5']
    # day_3_input = request.GET['day_3_5']
    # day_4_input = request.GET['day_4_5']
    #
    # Itinerary(length=len_input, city=cit_input, time_of_day=time_of_day_input, activity_type=activity_type_input,
    #           day_1=day_1_input, day_2=day_2_input, day_3=day_3_input, day_4=day_4_input).save()
    #
    # len_input = request.GET['length_6']
    # cit_input = request.GET['city_6']
    # time_of_day_input = request.GET['time_of_day_6']
    # activity_type_input = request.GET['activity_type_6']
    # day_1_input = request.GET['day_1_6']
    # day_2_input = request.GET['day_2_6']
    # day_3_input = request.GET['day_3_6']
    # day_4_input = request.GET['day_4_6']
    #
    # Itinerary(length=len_input, cit=cit_input, time_of_day=time_of_day_input, activity_type=activity_type_input,
    #           day_1=day_1_input, day_2=day_2_input, day_3=day_3_input, day_4=day_4_input).save()

    return render(request, 'form.html', context=data)


def form_submit(request):
    data=dict()

    # len_input = request.GET['length_1']

    return render(request, 'form_submit.html', context=data)











