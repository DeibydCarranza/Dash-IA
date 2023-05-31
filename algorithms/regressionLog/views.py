from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

# Create your views here.
def regression_algorithm(request):
    return render(request, 'regression.html')
