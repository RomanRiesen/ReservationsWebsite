from django.views import generic
from django.template import loader
from django.http import HttpResponse
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render

from django.core.validators import validate_email
from django import forms
from django.utils.crypto import get_random_string

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

    if seatsJson == "" or email == "" or date == "":
        return HttpResponse("Empty Values", status=400)

    try:
        validate_email(request.POST.get("email", ""))
    except forms.ValidationError:
        return HttpResponse("Bad Email", status=400)


    #FIXME captcha missing


    #FIXME create link better!!!
    while True:
        userHash = get_random_string(length=32)#about as many possible strings as atoms in the universe. so checking for uniqueness isn't entirely necessary. But still.
        if (len(Reservation.objects.filter(reservation_hash = userHash)) is 0):
            break

    emailJson = render_to_string('confirmationEmail.json', {'confirmationLink': request.META['HTTP_HOST']+'/index/emailVerification/'+userHash})
    print(emailJson)
    emailObj = json.loads(emailJson)
    try:
        send_mail(
        emailObj['subject'],
        emailObj['text'],
        emailObj['from'],
        [email],
        fail_silently=False,
        )
    except ConnectionRefusedError:
        return HttpResponse("Email Failed", status=418)


    seats = json.loads(seatsJson)
    for s in seats:
        #FIXME iterate over same seatNames, then compare PerformanceDates. But how to select PerformanceDate_datums I do not know
        for obj in Reservation.objects.filter(datum__datum = date):
            if obj.seatName == s:
                return HttpResponse("Seats Unavailable", status=400)


    #insert new Reservation
    Reservation.objects.bulk_create(
        [Reservation(
            email = email,
            seatName = seat,
            datum = PerformanceDate.objects.filter(datum = date)[0],
            reservation_hash = userHash) for seat in seats
         ]
    )
    #returns the reservationEntered.html file if captcha works
    return render(request, 'reservationEntered.html')



def getreservation(request, date):
    dates = Reservation.objects.filter(datum__datum = date)
    reservedSeats = []
    for d in dates:
        reservedSeats.append(d.seatName)
    response = json.dumps(reservedSeats)
    return HttpResponse(response)


def emailVerification(request, userHash):
    print("emailVerification", userHash)
    #set reservation_confirmed to true for all Reservations, where reservation_hash is the same.
    for r in Reservation.objects.filter(reservation_hash = userHash):
        if  r.reservation_confirmed:
            return render(request, 'reservationConfirmation.html', {"alreadyReserved":"true"})
        r.reservation_confirmed = True
        #r.reservation_hash = ""
        r.save()
    return render(request, 'reservationConfirmation.html', {"alreadyReserved":"false"})
