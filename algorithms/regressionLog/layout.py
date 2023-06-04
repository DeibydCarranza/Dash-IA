import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import dcc, html,Input, Output, callback, State
import dash

import pandas as pd
import plotly.express as px       
import plotly.graph_objects as go
from dash import dcc, html,dash_table

from sklearn.metrics import roc_curve
from sklearn.metrics import RocCurveDisplay
import dash_bootstrap_components as dbc
import math


""" Sección donde se renderizan las tablas, gráficas y componentes propios del algoritmo ->method.py"""
def section_graphs_interactive(exactitud,report,Matriz_Clasificacion,TypeG,X_validation,Y_validation,ClasificacionRL,columns_values,app):
        # Crear gráfica de barras interactiva con Plotly
    graph_vali = px.scatter(x=X_validation[:, 0], y=X_validation[:, 1], color=Y_validation)
    graph_vali.update_layout(
        title="Gráfica de validación",
        xaxis=dict(title="Negativo/Benigno"),
        yaxis=dict(title="Positivo/Maligno"),
    )


    Matriz_Clasificacion.insert(0, "Clasificación", Matriz_Clasificacion.index)

    # Crear la tabla de datos con la primera columna
    table = dash_table.DataTable(
        columns=[{"name": col, "id": col} for col in Matriz_Clasificacion.columns],
        data=Matriz_Clasificacion.to_dict("records"),
        style_data_conditional=[
            {
                "if": {"column_id": col},
                "backgroundColor": "lightblue",
                "fontWeight": "bold",
            }
            for col in Matriz_Clasificacion.columns
        ],
    )

    # Sección de reporte
    classification_report_div = html.Div(
        [
            html.Pre(report, id="report-content", className="report-content"),
        ],
        style={"overflowX": "scroll"},
    )

    # Calcular la curva ROC
    roc_curve_fig = go.Figure()
    fpr, tpr, _ = roc_curve(Y_validation, ClasificacionRL.predict_proba(X_validation)[:, 1])

    # Crear la gráfica ROC
    roc_curve_fig = go.Figure(
        data=go.Scatter(
            x=fpr,
            y=tpr,
            mode='lines',
            name='Curva ROC',
            line=dict(color='blue'),
        ),
    )

    # Establecer etiquetas y título de la gráfica
    roc_curve_fig.update_layout(
        title='Curva ROC - '+TypeG,
        xaxis=dict(title='Tasa de Falsos Positivos'),
        yaxis=dict(title='Tasa de Verdaderos Positivos'),
    )

    #Grid único del reporte y ROC
    Grid_layout = dbc.Container(
        dbc.Row(
            [
                dbc.Col(
                    classification_report_div,
                    width=6  # Ancho de la columna
                ),
                dbc.Col(
                    dcc.Graph(figure=roc_curve_fig),
                    width=6  # Ancho de la columna
                )
            ],
            justify="center"  # Alinear el contenido en el centro del grid
        ),
        fluid=True  # Establecer el ancho completo del grid
    )

    # Mostrador de predicción
    prediction_lay = accordion_diagnostic(columns_values,app)

    # Layoput principal que será devuelto
    layout = html.Div([
        # Gráfica de validación
        dcc.Graph(figure=graph_vali),

        # Tabla
        table,

        # Exactitud
        html.H3(f'Exactitud: {exactitud}'),

        # Grid con las secciones classification_report_div y dcc.Graph(figure=roc_curve_fig)
        html.H3('Reporte de Clasificación:'),

        Grid_layout,
        prediction_lay
    ])

    return layout

""" Sección tipo acordeon que muestra la predicción a los pacientes """
def accordion_diagnostic(columns_values,app):
    obj_description = [
        {
            "id": "salud",
            "image": "https://cdn-icons-png.flaticon.com/512/883/883309.png",
            "label": "Pronóstico por medio de IA",
            "description": "Precicción con base a los datos recopilados",
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
                            pronostico(columns_values,app)
                    ),   
                ],
                value=obj_description[0]["id"],
            )
        ],
    )

    return accordion




# def pronostico(columns_values,app):
#     layout = html.Div(children=[])

#     grid_children = []
#     for column in columns_values:
#         input_element = html.Div([dcc.Input(type="number", placeholder="Ingrese un valor", 
#                                   id=column, required=True, min="0"),
#                             html.Label(column)
#         ])

#     grid_children.append(dmc.Col(html.Div(input_element, style={"textAlign": "center"}), span=4))

#     grid_layout = dmc.Grid(children=grid_children,grow=True, gutter="xl")
#     layout.children.append(grid_layout)

#     return layout


# def pronostico(columns_values, app):
#     layout = html.Div(children=[])
#     input_elements = []

#     for column in columns_values:
#         input_element = dcc.Input(
#             type="number",
#             placeholder="Ingrese un valor",
#             id="input-prono-{}".format(column),
#             required=True,
#             min="0"
#         )
#         input_elements.append(html.Div([
#             html.Label(column),
#             input_element
#         ]))

#     # # Agregar el botón de envío al formulario
#     # submit_button = html.Button("Enviar", id="submit-button-prono")
#     # input_elements.append(submit_button)

#     # # Agregar los elementos de entrada y el botón al layout
#     layout.children = input_elements

#     # # Agregar el elemento de salida para mostrar el resultado
#     # output_div = html.Div(id="output-div")
#     # layout.children.append(output_div)

#     return layout

def pronostico(columns_values, app):
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

    layout.children.append(html.Div(children=[
            card_diasgnostic(0,1233)
    ]))
    return layout

def card_diasgnostic(grupo,score):
    card = dmc.Card(
        children=[
            dmc.CardSection(
                dmc.Image(
                    src="https://www.axiomafv.com/wp-content/uploads/2016/12/toma-de-decisiones-700x394.jpg",
                    height=160,
                )
            ),
            dmc.Group(
                [
                    dmc.Text("Resultados del pronóstico", weight=500),
                    dmc.Badge("Sugerencia", color="red", variant="light"),
                ],
                position="apart",
                mt="md",
                mb="xs",
            ),
            dmc.Text(
                "Con base a los datos introducidos, se pantlea la posibilidad de pertenecer al grupo "
                +str(grupo)+" con una exactitud del algoritmo del "+str(score),
                size="sm",
                color="dimmed",
            ),
            dmc.Button(
                "Descargar pronóstico",
                variant="light",
                color="blue",
                fullWidth=True,
                mt="md",
                radius="md",
            ),
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        style={"width": 400},
    )
    return card