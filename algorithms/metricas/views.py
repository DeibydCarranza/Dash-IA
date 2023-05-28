from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

# Create your views here.
def metrics_algorithm(request):
    return render(request, 'metricas.html')