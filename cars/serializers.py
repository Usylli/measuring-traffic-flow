from rest_framework.serializers import ModelSerializer, SerializerMethodField
from cars.models import CarsLocation, Incidents


class CarsListSerializer(ModelSerializer):
    class Meta:
        model = CarsLocation
        fields = ['guid', 'datetime', 'latitude', 'longitude']

class IncidentsSerializer(ModelSerializer):
    class Meta:
        model = Incidents
        fields = '__all__'


class IncidetnGeoJsonSerializer(ModelSerializer):
    geometry = SerializerMethodField()

    def get_geometry(self, obj):
        return {
            'type': 'Point',
            'coordinates': [obj.latitude, obj.longitude]
        }

    class Meta:
        model = Incidents
        fields = ('id', 'datetime', 'geometry', 'comment')