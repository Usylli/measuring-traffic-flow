from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from cars.serializers import CarsListSerializer
from cars.models import CarsLocation


class CarsLocationList(generics.ListAPIView):
    serializer_class = CarsListSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        guid = self.request.query_params.get('guid')
        start_date = self.request.query_params.get('sd')
        end_date = self.request.query_params.get('ed')
        if guid is None:
            return CarsLocation.objects.filter(guid='11686700327246500000')
        #2020-12-08 11:15:00
        return CarsLocation.objects.filter(guid=guid, datetime__range=(start_date, end_date)).order_by('datetime')


class CarsGuidList(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        cars = CarsLocation.objects.all().order_by('guid').distinct('guid')
        guids = []
        for car in cars:
            guids.append(car.guid)
        return Response(guids)