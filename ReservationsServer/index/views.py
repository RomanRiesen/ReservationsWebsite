from django.views import generic
from django.template import loader
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render

from django.core.validators import validate_email
from django import forms

import json
from datetime import date

from .models import PerformanceDate, Reservation

from .emailHelper import *

# Create your views here

#
def intro(request):
    #with open('/index/templates/index.html', 'r') as f:
    #    s = f.read()
    #    return HttpResponse(s)
    return render(request, 'welcomePage.html', {'seatReservationLocation': 'index',})

#returns the first html page (the one on which you select which date)
def index(request):
    #with open('/index/templates/index.html', 'r') as f:
    #    s = f.read()
    #    return HttpResponse(s)
    return render(request, 'index.html')

def dateselection(request):
    return render(request, 'dateselection.html')


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
def sitzreservation(request):
    return render(request, 'sitzreservation.html')


#send the data of the seats.
def sitzverteilung(request):
    with open('../seatsORIGINAL.json', 'r') as f:
        s = f.read()
        return HttpResponse(s)


def reserved(request):
    try:
        seatsJson = request.POST["seats"]
        email = request.POST["email"]
        date = request.POST["date"]
    except KeyError:
        #vital data ommited
        return HttpResponse("Missing Values", status=400)

    try:
        validate_email(request.POST.get("email", ""))
    except forms.ValidationError:
        return HttpResponse("Bad Email", status=400)


    if seatsJson == "" or email == "" or date == "":
        return HttpResponse("Empty Values", status=400)

    #FIXME captcha missing

    try:
        send_mail(
        'Lalalal',
        'Here is the message.',
        'RomanRiesen@gmail.com',
        ['roman.r97@gmx.ch'],
        fail_silently=False,
        )
    except ConnectionRefusedError:
        return HttpResponse("Email Failed", status=418)


    #FIXME check if a seat is already reserved!
    seats = json.loads(seatsJson)
    for s in seats:
        for obj in Reservation.objects.values():
            if obj['seatName'] == s  and obj['datum'] == date:
                return HttpResponse("Seats Unavailable", status=400)


    #insert new Reservation
    Reservation.objects.bulk_create(
        [Reservation(email = email, seatName = seat, datum = date) for seat in seats]
    )
    #returns the reservationEntered.html file if captcha works
    return render(request, 'reservationEntered.html')



def getreservation(request, date):
    dates = Reservation.objects.filter(datum = date)
    reservedSeats = []
    for d in dates:
        reservedSeats.append(d.seatName)
    response = json.dumps(reservedSeats)
    return HttpResponse(response)
