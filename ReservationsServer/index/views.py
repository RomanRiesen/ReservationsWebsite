from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.http import JsonResponse

import json
from datetime import date

from .models import PerformanceDate

# Create your views here
#returns the first html page (the one on which you select which date)
def index(response):
    with open('../dateSelection.html', 'r') as f:
        s = f.read()
        return HttpResponse(s)

#Gets dates and returns HttpResponse with it.
def getdates(response, onlyGetDatesInTheFuture = True):
    dates = PerformanceDate.objects.order_by('datum')
    #Remove all the passed dates
    if onlyGetDatesInTheFuture:
        dates = dates.filter(datum__gte = date.today())

    response = []
    #Make into isoformat to easier create the JavaScript date objects later
    #for d in dates:
    #    response.append({"date":d.datum.isoformat(), "allReserved":d.noMoreFreeSeats})

    for d in dates:
        response.append(d.datum.isoformat())

    return HttpResponse(JsonResponse(response, safe=False))



#does captcha verification
#and returns contents of the actual seatreservation site, if captcha is valid
def captcha(response):
    pass
