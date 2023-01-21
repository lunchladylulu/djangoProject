import folium as folium

from myapp.models import Currency, Rates, City, Itinerary


def get_currency_list():
    currency_list = list()
    import requests
    from bs4 import BeautifulSoup
    url = "https://thefactfile.org/countries-currencies-symbols/"
    response = requests.get(url)
    #if not response.status_code == 200:
    #      return currency_list
    soup = BeautifulSoup(response.text)
    data_lines = soup.find_all('tr')
    for line in data_lines:
        try:
            detail = line.find_all('td')
            currency = detail[2].get_text().strip()
            iso = detail[3].get_text().strip()
            if (currency, iso) in currency_list:
                continue
            currency_list.append((currency, iso))
        except:
            continue
    return currency_list

def add_currencies(currency_list):
    for currency in currency_list:
        currency_name = currency[0]
        currency_symbol = currency[1]
        if len(currency_symbol) > 3:
            continue
        try:
            c = Currency.objects.get(iso=currency_symbol)
        except:
            c = Currency(long_name=currency_name, iso=currency_symbol)
        c.name = currency_name
        c.save() #To test out the code, replace this by print(c)


def get_currency_rates(iso_code):
    url = "http://www.xe.com/currencytables/?from=" + iso_code
    import requests
    from bs4 import BeautifulSoup
    x_rate_list = list()
    try:
        page_source = BeautifulSoup(requests.get(url).content)
    except:
        return x_rate_list
    data = page_source.find('tbody')
    data_lines = data.find_all('tr')
    for line in data_lines:
        symbol = line.find('th').get_text()
        data=line.find_all('td')
        try:
            x_rate = float(data[2].get_text().strip())
            x_rate_list.append((symbol,x_rate))
        except:
            continue
    return x_rate_list


def update_xrates(currency):
    try:
        new_rates = get_currency_rates(currency.iso)
        for new_rate in new_rates:
            from datetime import datetime, timezone
            time_now = datetime.now(timezone.utc)
            try:
                rate_object = Rates.objects.get(currency=currency, x_currency=new_rate[0])
                rate_object.rate = new_rate[1]
                rate_object.last_update_time = time_now
            except:
                rate_object = Rates(currency=currency, x_currency=new_rate[0], rate=new_rate[1],last_update_time=time_now)
            rate_object.save()
    except:
        pass


def DMS_to_decimal(dms_coordinates):
    degrees = int(dms_coordinates.split('°')[0])
    minutes = int(dms_coordinates.split('°')[1].split("'")[0])
    try:
        seconds = int(dms_coordinates.split('°')[1].split("'")[1][:2])
    except:
        seconds = 0.0
    decimal = degrees + minutes/60 + seconds/3600
    try:
        if dms_coordinates[-1] == "S":
            decimal = -decimal
    except:
        pass
    try:
        if dms_coordinates[-1] == "W":
            decimal = -decimal
    except:
        pass
    return decimal


def get_lat_lon(city_name):
    import requests
    from bs4 import BeautifulSoup
    try:
        city = City.objects.get(name=city_name)
        lat = city.latitude
        lon = city.longitude
        wiki_link = ""
    except:
        url = "https://en.wikipedia.org/wiki/"
        url += city_name.replace(" ","_")
        wiki_link = url
        try:
            text = requests.get(url).text
            soup = BeautifulSoup(text)
            lat = soup.find('span', class_="latitude").get_text()
            lon = soup.find('span', class_="longitude").get_text()
            lat = DMS_to_decimal(lat)
            lon = DMS_to_decimal(lon)
        except:
            lat = 0.0
            lon = 0.0
    return lat,lon,wiki_link


def add_markers(m,visiting_cities):
    import folium
    lat_lon_list = list()
    for city_name in visiting_cities:
        lat,lon,wiki_link = get_lat_lon(city_name)
        print(city_name,lat,lon,wiki_link)
        if lat != 0.0 and lon != 0.0 and wiki_link != "":
            icon = folium.Icon(color="blue",prefix="fa",icon="plane")
            popup = "<a href="
            popup += wiki_link
            popup += ">" + city_name+ "</a>"
            marker = folium.Marker((lat,lon),icon=icon,popup=popup)
            marker.add_to(m)
            lat_lon_list.append([lat,lon])
    #Add line. First rearrange lat lons by longitude
    lat_lon_list.sort(key=lambda x: x[1])
    line_string = list()
    for i in range(len(lat_lon_list)-1):
        line_string.append([lat_lon_list[i],lat_lon_list[i+1]])
    line = folium.PolyLine(line_string,color="red",weight=5)
    line.add_to(m)
    return m


def delete_trips():
    for trip in Itinerary.objects.all():
        trip.delete()


def add_trips():
    import csv
    from os import path
    basepath = path.dirname(__file__)
    filepath = path.abspath(path.join(basepath, "..", "static", "myapp", "itinerary_data.csv"))
    with open(filepath) as f:
        trip_list = list(csv.reader(f, delimiter=","))[1:]
    for trip in trip_list:
        t = Itinerary(length=int(trip[0]),
                      city=trip[1],
                      time_of_day=trip[2],
                      activity_type=trip[3],
                      day_1=trip[4],
                      day_2=trip[5],
                      day_3=trip[6],
                      day_4=trip[7])
        t.save()