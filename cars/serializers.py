from rest_framework.serializers import ModelSerializer
from cars.models import CarsLocation


class CarsListSerializer(ModelSerializer):
    class Meta:
        model = CarsLocation
        fields = ['guid', 'datetime', 'latitude', 'longitude']
