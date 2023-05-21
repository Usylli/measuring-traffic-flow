from django.core.serializers import serialize
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from cars.serializers import CarsListSerializer, IncidentsSerializer, IncidetnGeoJsonSerializer
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
