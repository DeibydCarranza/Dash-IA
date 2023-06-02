from django.urls import path, include
from .views import regression_algorithm
from django.views.generic import TemplateView


#Importar Dashboards
from . import (dash_app)

urlpatterns = [
    path('', regression_algorithm, name="regression_path"),
    path('receta_cancer/', TemplateView.as_view(template_name='receta_cancer.html'), name='receta_C'),
]
