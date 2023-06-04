import dash
from dash import dcc, html,Input, Output, callback, State
from .. import components
import os
from datetime import date
from . import tool as tl 
from . import layout as lay
from django_plotly_dash import DjangoDash
import matplotlib.pyplot as plt   
import seaborn as sns     
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify             
import yfinance as yf


app = DjangoDash('section_pronosArbBosq')


app.layout = html.Div(children=[
    lay.dropdown_list_yfinance(),
    html.Div(id='output-data-upload'),
    html.Div(id='output-container-date-picker-range'), #sOLO PARA VISUALIZAR LAS FECHAS EN LA PANTALLA
],
style={'width': '100%', 'height': '100%'}
)   



"""  --------  Callbacks  ----------"""

""" Empresa seleccionada por dropdwon principal """
@app.callback([Output("selected-value-yfinance", "children"), 
               Output("output-data-upload", "children")],
            [Input("list_yfinance_select", "value")]
)
def select_value(value):
    if value:
        children = [
            lay.section_params_date()
        ]
        return "Has seleccionado " + value, children
    else:
        return "No has seleccionado ninguna empresa", []


""" Devolver la fecha escogida para la primera evaluación """
@app.callback(
    Output('output-container-date-picker-range', 'children'),
    Input('btn_proc_date', 'n_clicks'),
    State('my-date-picker-range', 'start_date'),
    State('my-date-picker-range', 'end_date'),
    State('input_interval', 'value')
)
def update_output(n_clicks, start_date, end_date, interval):
    if n_clicks is None:
        return dash.no_update
    
    if start_date is None or end_date is None:
        return "Seleccione un rango de fechas y un intervalo en días."
    
    if interval is None or interval == '':
        return "Ingrese un intervalo en días válido."
    
    start_date_object = date.fromisoformat(start_date)
    end_date_object = date.fromisoformat(end_date)

    # Formateando las fechas a YYYY-MM-DD
    start_date_formatted = start_date_object.strftime('%Y-%-m-%-d')
    end_date_formatted = end_date_object.strftime('%Y-%-m-%-d')


    # string_prefix = 'You have selected: '
    # if start_date is not None:
    #     start_date_object = date.fromisoformat(start_date)
    #     start_date_string = start_date_object.strftime('%B %d, %Y')
    #     string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    # if end_date is not None:
    #     end_date_object = date.fromisoformat(end_date)
    #     end_date_string = end_date_object.strftime('%B %d, %Y')
    #     string_prefix = string_prefix + 'End Date: ' + end_date_string
    # if len(string_prefix) == len('You have selected: '):
    #     return 'Select a date to see it displayed here'
    
    return f"Fecha de inicio: {start_date_formatted}, Fecha de fin: {end_date_formatted}, Intervalo: {interval} días"

