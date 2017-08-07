from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.http import JsonResponse
from django.template import loader

import json
from datetime import date

from .models import PerformanceDate

# Create your views here
#returns the first html page (the one on which you select which date)
def index(request):
    #with open('/index/templates/index.html', 'r') as f:
    #    s = f.read()
    #    return HttpResponse(s)
    return render(request, 'index.html', {})

def dateselection(request):
    return render(request, 'dateselection.html', {})


#Gets dates and returns HttpResponse with it.
def getdates(request, onlyGetDatesInTheFuture = True):
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
def captcha(request):
    pass






#loads after the date selection
#returns the seatreservation.html file if captcha works
# adds to session that user is verified.
def sitzreservation(request):
    return render(request, 'sitzreservation.html', {})


#if user is verified to not be a bot
#send the data of the seats.
def sitzverteilung(request):
    with open('../seatsORIGINAL.json', 'r') as f:
        s = f.read()
        return HttpResponse(s)


def reserved(request):
    s = "Reservation Succesfull!"
    return HttpResponse(s)
