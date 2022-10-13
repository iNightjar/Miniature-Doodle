from django.shortcuts import render
from django.http.response import JsonResponse
from .models import Guest, Movie, Reservation


# Create your views here.

#1 without rest framework, and no model query, FBV
def no_rest_no_model(request):

    guest = [
        {
            'id': 1,
            "Name" : "Omar", 
            "mobile": 789456,
        },
        {
            'id': 2,
            "Name": "ysssin",
            "mobile": 74123,
        }
    ]

    return JsonResponse(guest, safe=False)



#2 model data default django without rest
def no_rest_from_model(request):


    data =Guest.objects.all()
    response = {
        'guests' : list(data.values('name', 'mobile'))
    }

    return JsonResponse(response)




