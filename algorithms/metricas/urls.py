from django.urls import path, include
from .views import metrics_algorithm

#Importar Dashboards
from . import (dash_app)

urlpatterns = [
    path('', metrics_algorithm, name="apriori"),
]
