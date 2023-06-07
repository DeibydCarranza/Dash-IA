import dash_mantine_components as dmc
from dash import dcc, html,Input, Output, State
from .. import components as comp
     
import plotly.graph_objects as go
from dash import dcc, html,dash_table


import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

""" Vista en 2 pestañas de los métodos presentes """
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


""" Sección donde se renderizan las tablas, gráficas y componentes propios del algoritmo ->method.py"""
def section_graphs_interactive(exactitud,report,Matriz_Clasificacion,TypeG,X_val,Y_val,Clasificacion,columns_values):

    print(Matriz_Clasificacion)
    num_filas, num_columnas = Matriz_Clasificacion.shape

    # ---- Matriz de clasificaciones
    table = comp.matrizClasif(Matriz_Clasificacion)

    # ---- Sección de reporte
    classification_report_div = html.Div([
            html.Pre(report, id="report-content", className="report-content"),
        ],
        style={"overflowX": "scroll"},
    )

    # ---- Calcular la curva ROC
    if num_columnas > 2:
        roc_curve_fig = comp.rocMultipleGraph(X_val, Y_val, Clasificacion)
        print("----------")
    else:
        roc_curve_fig = comp.rocBinaryGraph(X_val, Y_val, Clasificacion)

    # ---- Grid único del reporte y ROC
    Grid_layout = dbc.Container(
        dbc.Row(
            [
                dbc.Col(
                    classification_report_div,
                    width=6  # Ancho
                ),
                dbc.Col(
                    dcc.Graph(figure=roc_curve_fig),
                    width=6  # Ancho
                )
            ],
            justify="center"
        ),
        fluid=True  # Establecer el ancho completo del grid
    )

    # ---- Acordeon que engloba lo anterior
    acordeon = accordionMatrixScoreGraphs(table, exactitud, Grid_layout)

    # Mostrador de predicción
    #prediction_lay = accordion_diagnostic(columns_values)

    # Layoput principal que será devuelto
    layout = html.Div([
        acordeon,
        #prediction_lay
    ])

    return layout

""" Acordeon desplegable con elementos individuales """
def accordionMatrixScoreGraphs(table, exactitud, Grid_layout):
    acordeon = dmc.Accordion(
        value="flexibility",
        children=[
            dmc.AccordionItem([
                    
                    dmc.AccordionControl("Matriz de clasificación"),
                    dmc.AccordionPanel(
                        dmc.Group([
                            table
                        ])
                    ),
                ],
                value="matrizClasifi",
            ),
            dmc.AccordionItem([
                    dmc.AccordionControl("Reporte de clasificación y rendimiento"),
                    dmc.AccordionPanel(
                        dmc.Group([
                            html.H3(f'Exactitud: {exactitud}%'),
                            html.H3('Reporte de Clasificación:'),
                            Grid_layout
                        ])
                    ),
                ],
                value="reporteRendimiento",
            ),
            dmc.AccordionItem([
                    dmc.AccordionControl("Graficando árbol y reporte"),
                    dmc.AccordionPanel(
                        dmc.Group([
                            ## Graficando arbol y reporte
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


