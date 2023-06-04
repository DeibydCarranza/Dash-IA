import dash
from dash import dcc, html,Input, Output, callback, State
from .. import components
import os
from . import tool as tl 
from django_plotly_dash import DjangoDash
import matplotlib.pyplot as plt   
import seaborn as sns     
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify  
import plotly.graph_objs as go           
from datetime import date


""" Dropdown principal para seleccionar el tipo de empresa a analizar """
def dropdown_list_yfinance():
    tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'FB', 'TSLA', 'NVDA', 'JPM', 'V', 
               'BABA', 'WMT', 'JNJ', 'PG', 'UNH', 'INTC', 'HD', 'MA', 'PYPL', 'DIS', 
               'CMCSA', 'VZ', 'CSCO', 'PFE', 'NFLX', 'ADBE', 'ABT', 'BAC', 'KO', 'NKE', 'ABBV']

    select_component = html.Div([
        dmc.Select(
            data=tickers,
            searchable=True,
            id="list_yfinance_select",
            nothingFound="No options found",
            label="Selección de empresa",
            style={"width": 500},
            icon=DashIconify(icon="radix-icons:magnifying-glass"),
            rightSection=DashIconify(icon="radix-icons:chevron-down"),
            placeholder="Selecciona una empresa"
        ),
        dmc.Text(id="selected-value-yfinance"),
    ])
    return select_component

""" Selector de 2 fechas """
def selector_date():
    layout = html.Div([
        dcc.DatePickerRange(
            id='my-date-picker-range',
            min_date_allowed=date(1995, 8, 5),
            max_date_allowed=date.today(),
            initial_visible_month=date.today(),
            end_date=date.today(),
            clearable=True,
        )
        ])
    return layout

""" Sección para agrupar fecha e input """
def section_params_date():

    layout = html.Div([
        dbc.Row(
            children=[
                dbc.Col(html.Div([
                    html.Label("Selección de fecha"),
                    selector_date()
                    ]), width=4),
                dbc.Col(html.Div([
                        html.Label("Intervalo de días"),
                        dcc.Input(id="input_interval", type="number", placeholder="Intervalo en días",min="1")
                    ]), width=4),
                dbc.Col(html.Div([
                    html.Label("Procesamiento de datos"),
                    dmc.Button("Procesar",color="lime",variant="gradient", id="btn_proc_date")]
                    ), width=4),
            ],
        )
    ])
    return layout



""" Generación de gráfica de precios en un periodo con 4 análisis"""
def render_prices(CompanyHist,ticker):
    trace_open = go.Scatter(
        x=CompanyHist.index,
        y=CompanyHist["Open"],
        mode="lines",
        name="Open"
    )
    trace_high = go.Scatter(
        x=CompanyHist.index,
        y=CompanyHist["High"],
        mode="lines",
        name="High"
    )
    trace_low = go.Scatter(
        x=CompanyHist.index,
        y=CompanyHist["Low"],
        mode="lines",
        name="Low"
    )
    trace_close = go.Scatter(
        x=CompanyHist.index,
        y=CompanyHist["Close"],
        mode="lines",
        name="Close"
    )
    
    layout = go.Layout(
        title=f"Histórico de precios de {ticker}",
        xaxis={"title": "Fecha"},
        yaxis={"title": "Precio"}
    )
    
    figure = go.Figure(data=[trace_open, trace_high, trace_low, trace_close], layout=layout)
    graph_figure = dcc.Graph(figure=figure)
    return graph_figure