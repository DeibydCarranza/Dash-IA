from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

# Create your views here.
def regression_algorithm(request):
    return render(request, 'regression.html')

import pandas as pd
import plotly.express as px
import os

# def interactive_table(request):

#     BCancer = BCancer.iloc[:, 1:]
#     fig = px.scatter_matrix(BCancer, color='Diagnosis')
#     fig.update_layout(height=800, width=800)
#     fig_html = fig.to_html(full_html=False)
#     return render(request, 'interactive_table.html', {'fig_html': fig_html})
import pandas as pd
import plotly.express as px

def interactive_table(request):
    path_file = os.path.join(os.path.dirname(__file__), '../../data_preload/WDBCOriginal_M_RL.csv')
    BCancer = pd.read_csv(path_file)
    BCancer_filtered = BCancer.iloc[:, 1:]  # Filtrar las columnas a partir de la columna con índice 2
    fig = px.scatter_matrix(BCancer_filtered, color='Diagnosis')
    fig.update_layout(height=800, width=800)
    fig_html = fig.to_html(full_html=False)
    return render(request, 'interactive_table.html', {'fig_html': fig_html})