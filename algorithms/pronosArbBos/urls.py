from django.urls import path, include
from .views import pronosArbBos_algorithm

#Importar Dashboards
from . import (dash_app)

urlpatterns = [
    path('', pronosArbBos_algorithm, name="pronosArbBos"),
]
