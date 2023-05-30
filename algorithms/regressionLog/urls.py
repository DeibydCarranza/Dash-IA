from django.urls import path, include
from .views import regression_algorithm,interactive_table

#Importar Dashboards
from . import (dash_app)

urlpatterns = [
    path('', regression_algorithm, name="regression_path"),
    path('interactive-table/', interactive_table, name='interactive_table'),

]
