from django.urls import path
from cars.views import (CarsLocationList, CarsGuidList, IncidentsViewSet,
                        CountCarsList, AverageCarsList, AverageWeekdayCarsList,
                        CountWeekdayCarsList, CountByWeekdayCarsList,
                        CountIncidentsList)

app_name = 'cars'

urlpatterns = [
    path('', CarsLocationList.as_view(), name='get-cars'),
    path('/guids', CarsGuidList.as_view(), name='get-guids'),
    path('/incidents', IncidentsViewSet.as_view({'get': 'list'})),
    path('/incidents/<int:pk>', IncidentsViewSet.as_view({'put': 'update',
                                                          'delete': 'destroy',
                                                          'patch': 'partial_update'
                                                          })),
    path('/count-incidents', CountIncidentsList.as_view(), name='count-incidents'),                                                        
    path('/count-cars', CountCarsList.as_view(), name='count-cars'),
    path('/average-hourly-cars', AverageCarsList.as_view(), name='average-cars'),
    path('/average-weekdays-hourly-cars', AverageWeekdayCarsList.as_view(),
         name='average-weekday-cars'),
    path('/weekdays-count-cars', CountWeekdayCarsList.as_view(),
         name='weekday-count-cars'),
    path('/by-weekday-count-cars', CountByWeekdayCarsList.as_view(),
         name='by-weekday-count-cars')
]
