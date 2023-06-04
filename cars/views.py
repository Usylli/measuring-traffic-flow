from django.core.serializers import serialize
from django.db.models.functions import ExtractHour
from django.db.models import Count, Avg
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from cars.serializers import (CarsListSerializer,
                              IncidentsSerializer,
                              IncidetnGeoJsonSerializer)
from cars.models import CarsLocation, Incidents


class CarsLocationList(generics.ListAPIView):
    serializer_class = CarsListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        guid = self.request.query_params.get('guid')
        start_date = self.request.query_params.get('sd')
        end_date = self.request.query_params.get('ed')
        if guid is None:
            return CarsLocation.objects.filter(guid='11686700327246500000')

        return CarsLocation.objects.filter(
            guid=guid,
            datetime__range=(start_date, end_date)
        ).order_by('datetime')


class CarsGuidList(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        cars = CarsLocation.objects.all().order_by('guid').distinct('guid')
        guids = []
        for car in cars:
            guids.append(car.guid)
        return Response(guids)


class IncidentsViewSet(viewsets.ModelViewSet):
    queryset = Incidents.objects.all()
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return serialize("geojson", self.get_queryset(), geometry_field="Point")

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return IncidetnGeoJsonSerializer
        else:
            return IncidentsSerializer

    def get_queryset(self):
        start_date = self.request.query_params.get('sd', None)
        end_date = self.request.query_params.get('ed', None)
        if start_date is None and end_date is None:
            return Incidents.objects.all()
        return Incidents.objects.filter(
            datetime__range=(start_date, end_date)
        ).order_by('datetime')


class CountIncidentsList(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        incidents = {}
        queryset = Incidents.objects.all()
        for incident in queryset:
            incidents[incident.comment] = 0
        for incident in queryset:
            incidents[incident.comment] += 1
        return Response(incidents)


class CountCarsList(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        date = self.request.query_params.get('date')
        cars = CarsLocation.objects.filter(
            datetime__date=date).values('guid').distinct().count()
        return Response(cars)


class AverageCarsList(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        cars = CarsLocation.objects.order_by('datetime')
        times = {
            0: 0, 1: 0,
            2: 0, 3: 0,
            4: 0, 5: 0,
            6: 0, 7: 0,
            8: 0, 9: 0,
            10: 0, 11: 0,
            12: 0, 13: 0,
            14: 0, 15: 0,
            16: 0, 17: 0,
            18: 0, 19: 0,
            20: 0, 21: 0,
            22: 0, 23: 0
        }
        for car in cars:
            hour = car.datetime.hour + 6
            if hour > 23:
                hour = hour - 24
            times[hour] += 1
        for i in range(0, 24):
            times[i] = times[i] / 7
        return Response(times)


class AverageWeekdayCarsList(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        cars = CarsLocation.objects.order_by('datetime')
        times = {}
        times['weekday'] = {
            0: 0, 1: 0,
            2: 0, 3: 0,
            4: 0, 5: 0,
            6: 0, 7: 0,
            8: 0, 9: 0,
            10: 0, 11: 0,
            12: 0, 13: 0,
            14: 0, 15: 0,
            16: 0, 17: 0,
            18: 0, 19: 0,
            20: 0, 21: 0,
            22: 0, 23: 0
        }
        times['weekend'] = {
            0: 0, 1: 0,
            2: 0, 3: 0,
            4: 0, 5: 0,
            6: 0, 7: 0,
            8: 0, 9: 0,
            10: 0, 11: 0,
            12: 0, 13: 0,
            14: 0, 15: 0,
            16: 0, 17: 0,
            18: 0, 19: 0,
            20: 0, 21: 0,
            22: 0, 23: 0
        }
        for car in cars:
            hour = car.datetime.hour + 6
            if hour > 23:
                hour = hour - 24
            if car.datetime.weekday() == 5 or car.datetime.weekday() == 6:
                times['weekend'][hour] += 1
            else:
                times['weekday'][hour] += 1
        for i in range(0, 24):
            times['weekday'][i] = times['weekday'][i] / 5
            times['weekend'][i] = times['weekend'][i] / 2
        return Response(times)


class CountWeekdayCarsList(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        cars = CarsLocation.objects.all()
        weekdays = 0
        weekends = 0
        for car in cars:
            if car.datetime.weekday() == 5 or car.datetime.weekday() == 6:
                weekends += 1
            else:
                weekdays += 1
        return Response({'weekends_count': weekends, 'weekdays_count': weekdays})


class CountByWeekdayCarsList(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        cars = CarsLocation.objects.all()
        weekday = {
            0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0
        }
        for car in cars:
            weekday[car.datetime.weekday()] += 1

        return Response(weekday)
