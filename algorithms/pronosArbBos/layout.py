import dash
from dash import dcc, html,Input, Output, callback, State
from .. import components as comp
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from . import tool as tl 
from django_plotly_dash import DjangoDash
import matplotlib.pyplot as plt   
import numpy as np    
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify  
import plotly.graph_objs as go           
from datetime import date
import io
import base64


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
            initial_visible_month=date(2020, 1, 1),
            end_date=date.today(),
            clearable=True,
            start_date_placeholder_text="DD/MM/AAAA",
            end_date_placeholder_text="DD/MM/AAAA"
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

""" Comparación de real vs estimado en acciones"""
def generar_grafica(Y_test,Y_Pronostico):
    plt.figure(figsize=(20, 5))
    plt.plot(Y_test, color='purple', marker='+', label='Real')
    plt.plot(Y_Pronostico, color='red', marker='+', label='Estimado')
    plt.xlabel('Fecha')
    plt.ylabel('Precio de las acciones')
    plt.title('Pronóstico de las acciones')
    plt.grid(True)
    plt.legend()

    # Guardar la gráfica en un búfer de memoria
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Convertir la gráfica en una cadena base64
    imagen_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    # Devolver el componente html.Img con la imagen
    return html.Img(src='data:image/png;base64,{}'.format(imagen_base64),style={"width": "100%"})


""" Reporte de pronóstico"""
def pronostic_report(Pronostico,Y_test,Y_Pronostico):
    importancia_variables = Pronostico.feature_importances_
    mae = mean_absolute_error(Y_test, Y_Pronostico)
    mse = mean_squared_error(Y_test, Y_Pronostico)
    rmse = mean_squared_error(Y_test, Y_Pronostico, squared=False)
    score = r2_score(Y_test, Y_Pronostico)

    layout = html.Div(
        children=[
            html.Div(f"Importancia variables: {importancia_variables}"),
            html.Div(f"MAE: {mae:.4f}"),
            html.Div(f"MSE: {mse:.4f}"),
            html.Div(f"RMSE: {rmse:.4f}"),
            html.Div(f"Exactitud: {(score*100):.4f}%")
        ]
    )
    return layout

""" Sección donde se renderizan las tablas, gráficas y componentes propios del algoritmo ->method.py"""
def section_graphs_interactive(report,Y_Prono, Y_test,Pronostico,columns_values, isForest):

    figure =  generar_grafica(Y_test,Y_Prono)

    # ---- Impresión del árbol. Si es un bosque, requiere #estimadores
    tree_layout = typeGraphTree(isForest, Pronostico,columns_values,Y_Prono)

    # ---- Acordeon que engloba lo anterior
    acordeon = accordionMatrixScoreGraphs(figure,report,tree_layout)

    # Layoput principal que será devuelto
    layout = html.Div([
        acordeon,
        html.Div(id="cmp-rendimientos-rocs"),
    ])

    return layout

""" Condicionando la gráfica de árbol al tipo de pronóstico"""
def typeGraphTree(isForest, Pronostico, columns_values, Y_Prono):
    if isForest:
        tree_layout = html.Div([
            dcc.Input(
                id=f"input_n_estimators",
                type="number", placeholder="n_estimators",className="input-field",
                min=1,step=1,value=None,           
            ),
            dmc.Button('Generar Bosque', id='btn-n-estimators', n_clicks=0,variant="gradient"),

            html.Div(id="tree-image-forest"),
        ])
    else:
        tree = comp.plotTree(Pronostico,columns_values,Y_Prono)
        tree_layout = html.Div([
            html.Img(src='data:image/png;base64,{}'.format(tree), style={'width': '100%', 'height': 'auto'}),
            dmc.Button("Generar Reporte", id="btn-descarga-arbol",variant="gradient"),
            dcc.Download(id="download-reporte-arbol")
        ])
    return tree_layout

""" Acordeon desplegable con elementos individuales """
def accordionMatrixScoreGraphs(figure,report, tree_layout):
    acordeon = dmc.Accordion(
        value="flexibility",
        children=[
            dmc.AccordionItem([
                    dmc.AccordionControl("Conformación del modelo"),
                    dmc.AccordionPanel(
                        dmc.Group([
                            figure
                        ])
                    ),
                ],
                value="matrizClasifi",
            ),
            dmc.AccordionItem([
                    dmc.AccordionControl("Reporte de clasificación"),
                    dmc.AccordionPanel(
                        dmc.Group([
                            report
                        ])
                    ),
                ],
                value="reporteRendimiento",
            ),
            dmc.AccordionItem([
                    dmc.AccordionControl("Graficando árbol y reporte"),
                    dmc.AccordionPanel(
                        dmc.Group([
                            tree_layout
                        ])
                    ),
                ],
                value="arbolGrafica",
            ),
        ],
        styles={
            "root": {
                "backgroundColor": dmc.theme.DEFAULT_COLORS["gray"][0],
                "borderRadius": 5,
            },
            "item": {
                "backgroundColor": "rgba(255, 0, 141, 0.08)",
                "border": "1px solid #a1a1a1",
                "position": "relative",
                "zIndex": 0,
                "transition": "transform 150ms ease",
                "&[data-active]": {
                    "transform": "scale(1.03)",
                    "backgroundColor": "white",
                    "boxShadow": 5,
                    "borderColor": dmc.theme.DEFAULT_COLORS["gray"][4],
                    "borderRadius": 5,
                    "zIndex": 1,
                },
            },
            "chevron": {
                "&[data-rotate]": {
                    "transform": "rotate(-90deg)",
                },
            },
        },
    )
    return acordeon

def pronostico():
    layout = dmc.Card(
        children=[
            dmc.CardSection(
                dmc.Image(
                    src="https://economipedia.com/wp-content/uploads/Consejos-para-invertir-en-acciones.jpg",
                    height=160,
                )
            ),
            dmc.Group(
                [
                    dmc.Text("Predicción de las acciones", weight=500),
                    dmc.Badge("Sugerencia", color="red", variant="light"),
                ],
                position="apart",
                mt="md",
                mb="xs",
            ),
            html.Div([
                html.H1("Pronóstico de Acciones"),
                html.Div([
                    html.Label("Open:"),
                    dcc.Input(id="open-input", type="number",min=0,step=0.1),
                    html.Label("High:"),
                    dcc.Input(id="high-input", type="number",min=0,step=0.1),
                    html.Label("Low:"),
                    dcc.Input(id="low-input", type="number",min=0,step=0.1),
                ]),
                dmc.Text(id='resultado-output',size="sm",color="dimmed")
            ]),
            dmc.Button(
                "Realizar pronóstico",
                variant="light",
                color="blue",
                fullWidth=True,
                mt="md",
                radius="md",
                id='pronosticar-button'
            ),
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        style={"width": 350},
    )
    return layout