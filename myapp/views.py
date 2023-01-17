from django.shortcuts import render

# Create your views here.

# This is a request-response. We create a dictionary so that the HTML template can understand Python.
# The render function sends the request and plants the result to home.html.
def home(request):
    data = dict()
    import datetime
    time = datetime.datetime.now()
    data["time_of_day"] = time
    data["xy"] = "xy"
    print(time)
    return render(request, "home.html", context=data)