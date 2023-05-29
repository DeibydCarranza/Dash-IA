from django.urls import path, include
from .views import cluster_algorithm

#Importar Dashboards
from . import (dash_app)

urlpatterns = [
    path('', cluster_algorithm, name="cluster"),
]
