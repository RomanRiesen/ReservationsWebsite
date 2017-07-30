from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


#Gets dates and returns HttpResponse with it.
def getdates():
    return HttpResponse(["28.1.2019", "29.1.2019", "30.1.2019", "32.1.2019", "33.1.2019", "34.1.2019", "35.1.2019", "36.1.2019"])

def Index(response):
    with open('../dateSelection.html', 'r') as f:
        s = f.read()

    return HttpResponse(s)
