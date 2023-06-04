import dash
from dash import dash_table,dcc,html
import base64
import pandas as pd
import os
from .. import components as comp
import yfinance as yf
from . import layout as lay



""" Generando el historial en rango de fechas """
def table_historial(ticker):
    df = yf.Ticker(str(ticker))

    CompanyHist = df.history(start='2019-01-01', end='2023-05-25', interval='1d')
    html.Div(id='output-container-date-picker-range'),
    graph_figure= lay.render_prices(CompanyHist,ticker)
    
    
    return graph_figure




""" Generate table """
def render_results(df):
    # Create Data Table
    table = comp.create_data_table(df,False)

    # Create Layout
    res = html.Div(
        children=[
            table
        ],
        className='render-container',
        style={
            'width': '100%',
        }
    )
    return res