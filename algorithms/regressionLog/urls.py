from django.urls import path, include
from .views import regression_algorithm

#Importar Dashboards
from . import (dash_app)

urlpatterns = [
    path('', regression_algorithm, name="regression_path")
]
