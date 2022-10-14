from sre_constants import SRE_INFO_LITERAL
from django.shortcuts import render
from django.http.response import JsonResponse
from .models import Guest, Movie, Reservation
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import Guest, GuestSerializer, Movie, MovieSerializer, Reservation, ReservationSerializer
from rest_framework import status, filters
from rest_framework.views import APIView
# from tickets import serializer
from django.http import Http404
from tickets import serializers
from rest_framework import generics, mixins, viewsets

# Create your views here.

# 1 without rest framework, and no model query, FBV


def no_rest_no_model(request):

    guest = [
        {
            'id': 1,
            "Name": "Omar",
            "mobile": 789456,
        },
        {
            'id': 2,
            "Name": "ysssin",
            "mobile": 74123,
        }
    ]

    return JsonResponse(guest, safe=False)


# 2 model data default django without rest
def no_rest_from_model(request):

    data = Guest.objects.all()
    response = {
        'guests': list(data.values('name', 'mobile'))
    }

    return JsonResponse(response)


# list == GET
# create == POST
# pk query == GET


# update == PUT
# Delete, Destroy == DELETE


# 3 function based views FBV

# 3.1 GET POST
@api_view(['GET', 'POST'])
def FBV_List(request):
    # GET
    if request.method == 'GET':
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)
    # POST
    elif request.method == 'POST':
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

# 3.2 GET PUT DELETE


@api_view(['GET', 'PUT', 'DELETE'])
def FBV_pk(request, pk):
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # GET
    if request.method == 'GET':
        # guests = Guest.objects.all()      No need to query the database
        serializer = GuestSerializer(guest)
        return Response(serializer.data)

    # PUT
    elif request.method == 'PUT':
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    if request.method == 'DELETE':
        # guests = Guest.objects.all()
        # serializer = GuestSerializer(guests, many=True)
        guest.delete()
        return Response(statu=status.HTTP_204_NO_CONTENT)


# CBV Class based views
# 4.1 list and create == GET and POST
class CBV_List(APIView):
    def get(self, request):
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.data,
            status=status.HTTP_400_BAD_REQUEST
        )


# CBV Class based views
# 4.2 GET PUT DELETE class based views == pk
class CBV_pk(APIView):

    def get_object(self, pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest)
        return Response(serializer.data)

    def put(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        guest = self.get_object(pk) 
        guest.delete()        
        return Response(status= status.HTTP_204_NO_CONTENT)


# DRY Dont Repeat Your Self .. Mixins
#5 Mixins

#5.1 Mixins  list
class mixins_list(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request):
        return self.list(request)


    def post(self, request):
        return self.create(request)

    
#5.2 mixins get put delete
class mixins_pk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
   
    def get(self, request, pk):
        return self.retrieve(request)

    def put(self, request, pk):
        return self.update(request)

    def delete(self, request, pk):
        return self.destroy(request)


#6 Generics
#6.1 GET POST
class generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

#6.2 GET PUT DELETE
class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer



#7 View Sets
class viewsets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

# creating viewsets for other models too

class viewsets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    # filter_backends = [filters.SearchFilter]
    filter_backends = [filters.SearchFilter] 
    search_fields = ['movie']

class viewsets_reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    ## setting fliters to search for reservations
    # filter_backends = [filters.SearchFilter] 
    # search_fields = ['reservation']

#8 Find Movie with FBV to allow more customizations
@api_view(['GET'])
def find_movie(request):
    movies = Movie.objects.filter(
        hall = request.data['hall'],
        movie = request.data['movie'],
    )
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


#9 Create New Reservation
@api_view(['POST'])
def new_reservation(request):
    movie = Movie.objects.get(
        hall=request.data['hall'],
        movie=request.data['movie'],
    )
    # in case of new guests who wanna see or book a movie
    guest = Guest()
    guest.name = request.data['name']
    guest.mobile = request.data['mobile']
    guest.save()  # save the instance to database

    reservation = Reservation()
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()

    # POST Request to create reservation in Reservation db Table
    return Response(status=status.HTTP_201_CREATED)
