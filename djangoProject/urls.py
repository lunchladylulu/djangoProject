"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.contrib import admin
from django.urls import path

from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('home', views.home, name="home1"),
    path('maintenance', views.maintenance, name='maintenance'),
    path('currencies', views.view_currencies, name='currencies'),
    path('currency-selection', views.currency_selection, name="currency_selector"),
    path('exchange_rate_info', views.exch_rate, name="exchange_rate_info"),
    path('register', views.register_new_user, name="register_user"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('voyagevault_home', views.voyagevault_home, name="voyagevault_home"),
    path('trip_result', views.get_itinerary, name="trip_result"),
    path('home', views.home, name='home'),
    path('map', views.map, name="map"),
    path('west_coast', views.west_coast, name="west_coast"),
    path('east_coast', views.east_coast, name="east_coast"),
    path('form', views.form, name="form"),
    path('form_submit', views.form_submit, name="form_submit"),
    path('reviews/', views.reviews, name='reviews'),
    path('reviews/add', views.add_review, name='add_review'),
]
