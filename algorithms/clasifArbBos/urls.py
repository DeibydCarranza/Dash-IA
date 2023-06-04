from django.urls import path, include
from .views import clasifArbBos_algorithm

#Importar Dashboards
from . import (dash_app)

urlpatterns = [
    path('', clasifArbBos_algorithm, name="clasifArb"),
]
