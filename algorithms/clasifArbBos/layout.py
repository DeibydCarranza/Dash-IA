import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import dcc, html,Input, Output, State
import dash
from .. import components as comp
import pandas as pd
import plotly.express as px       
import plotly.graph_objects as go
from dash import dcc, html,dash_table

from sklearn.metrics import roc_curve
from sklearn.metrics import RocCurveDisplay
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc


def tab_for_methods():

    layout = html.Div([
            dcc.Tabs(id="tabs_methods", value='tab_method_algor',children=[
                dcc.Tab(label='Clasificación por árbol de decisión', value='tab-1', children=[
                    
                    # Llama a los inputs propios del árbol (0-> indice, False->Tipo árbol)
                    comp.params_tree_fores(0,False),
                    dmc.Button('Generar carga de inputs', id='generate-button-tree', n_clicks=0,variant="gradient"),
                    html.Div(id='input-values-container-tree')

                ]),
                dcc.Tab(label='Clasificación por bosque aleatorio', value='tab-2',children=[
                    # Llama a los inputs propios del árbol (1-> indice, False->Tipo árbol)
                    comp.params_tree_fores(1,True),
                    dmc.Button('Generar carga de inputs', id='generate-button-forest', n_clicks=0,variant="gradient"),
                    html.Div(id='input-values-container-forest')

                ]),
            ],style={'margin-bottom':'60px','margin-top':'30px'}
            )
       ])
    return layout
