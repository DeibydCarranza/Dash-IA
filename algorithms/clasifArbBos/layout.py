import dash_mantine_components as dmc
from dash import dcc, html,Input, Output, State
from .. import components as comp
     
import plotly.graph_objects as go
from dash import dcc, html,dash_table

import dash_bootstrap_components as dbc


""" Sección donde se renderizan las tablas, gráficas y componentes propios del algoritmo ->method.py"""
def section_graphs_interactive(exactitud,report,Matriz_Clasificacion,Y_Clasi,X_val,Y_val,Clasificacion,columns_values, isForest):

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
                    width=6
                ),
                dbc.Col(
                    dcc.Graph(figure=roc_curve_fig),
                    width=6
                )
            ],
            justify="center"
        ),
        fluid=True  # Establecer el ancho completo del grid
    )

    # ---- Impresión del árbol. Si es un bosque, requiere #estimadores
    tree_layout = typeGraphTree(isForest, Clasificacion,columns_values,Y_Clasi)

    # ---- Acordeon que engloba lo anterior
    acordeon = accordionMatrixScoreGraphs(table, exactitud, Grid_layout,tree_layout)

    # Mostrador de predicción
    prediction_lay = accordion_diagnostic(columns_values)

    # Layoput principal que será devuelto
    layout = html.Div([
        acordeon,
        html.Div(id="cmp-rendimientos-rocs"),

        prediction_lay
    ])

    return layout


""" Condicionando la gráfica de árbol al tipo de clasificación"""
def typeGraphTree(isForest, Clasificacion, columns_values, Y_Clasi):
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
        tree = comp.plotTree(Clasificacion,columns_values,Y_Clasi)
        tree_layout = html.Div([
            html.Img(src='data:image/png;base64,{}'.format(tree), style={'width': '100%', 'height': 'auto'}),
            dmc.Button("Generar Reporte", id="btn-descarga-arbol",variant="gradient"),
            dcc.Download(id="download-reporte-arbol")
        ])
    return tree_layout



""" Acordeon desplegable con elementos individuales """
def accordionMatrixScoreGraphs(table, exactitud, Grid_layout, tree_layout):
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

""" Sección tipo acordeon que muestra la predicción a los pacientes """
def accordion_diagnostic(columns_values,):
    obj_description = [
        {
            "id": "salud",
            "image": "https://img.freepik.com/vector-premium/pronostico-comercial-prediccion-mercado-valores-inversion-o-superpoder-ver-futuro-adivino-ver-concepto-oportunidad-mano-hombre-negocios-poder-magico-ver-pronostico-bola-magica-cristal_212586-1252.jpg",
            "label": "Pronóstico por medio de IA",
            "description": "Clasificación con base a los datos recopilados",
        },
    ]

    def create_accordion_label(label, image, description):
        return dmc.AccordionControl(
            dmc.Group(
                [
                    dmc.Avatar(src=image, radius="xl", size="lg"),
                    html.Div(
                        [
                            dmc.Text(label),
                            dmc.Text(description, size="sm", weight=400, color="dimmed"),
                        ]
                    ),
                ]
            )
        )

    def create_accordion_content(content):
        return dmc.AccordionPanel(content)

    accordion = dmc.Accordion(
        chevronPosition="right",
        variant="contained",
        children=[
            dmc.AccordionItem(
                [
                    create_accordion_label(
                        obj_description[0]["label"], obj_description[0]["image"], obj_description[0]["description"]
                    ),
                    create_accordion_content(
                            pronostico(columns_values)
                    ),   
                ],
                value=obj_description[0]["id"],
            )
        ],
    )

    return accordion

def pronostico(columns_values):
    layout = html.Div(children=[])
    input_elements = []

    for column in columns_values:
        input_element = dcc.Input(
            type="number",
            placeholder="Ingrese un valor",
            id="input-prono-{}".format(column),
            required=True,
            min="0"
        )
        input_elements.append(html.Div([
            html.Label(column),
            input_element
        ]))
    layout.children = input_elements

    submit_button = html.Button("Enviar", id="submit-button", n_clicks=0)
    layout.children.append(submit_button)
    layout.children.append(html.Div(id="output-container-prono"))

    # ------------Sección donde se muestran los resultados

    return layout
