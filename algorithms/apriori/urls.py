
from django.urls import path, include
from .views import apriori_algorithm

#Importar Dashboards
from . import (dash_app)

urlpatterns = [
    path('', apriori_algorithm, name="apriori"),
]
