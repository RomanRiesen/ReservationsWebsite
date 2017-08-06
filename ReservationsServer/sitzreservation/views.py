from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

#page after the date selection
#returns the seatreservation.html file if captcha works
# adds to session that user is verified.
def sitzreservation(response):
    with open('../index.html', 'r') as f:
        s = f.read()
        return HttpResponse(s)
