from django.urls import path
from cars.views import CarsLocationList, CarsGuidList

app_name = 'cars'

urlpatterns = [
    path('', CarsLocationList.as_view(), name='get-cars'),
    path('/guids', CarsGuidList.as_view(), name='get-guids')
]