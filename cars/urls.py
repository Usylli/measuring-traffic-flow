from django.urls import path
from cars.views import CarsLocationList, CarsGuidList, IncidentsViewSet

app_name = 'cars'

urlpatterns = [
    path('', CarsLocationList.as_view(), name='get-cars'),
    path('/guids', CarsGuidList.as_view(), name='get-guids'),
    path('/incidents', IncidentsViewSet.as_view({'get': 'list'})),
    path('/incidents/<int:pk>', IncidentsViewSet.as_view({'put': 'update',
                                                          'delete': 'destroy',
                                                          'patch': 'partial_update'
                                                        })),                      
]