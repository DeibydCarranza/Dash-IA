import dash_mantine_components as dmc
from dash_iconify import DashIconify

import pandas as pd
import plotly.express as px       
import plotly.graph_objects as go
from dash import dcc, html,dash_table

from sklearn.metrics import roc_curve
from sklearn.metrics import RocCurveDisplay
import dash_bootstrap_components as dbc

def section_graphs_interactive(exactitud,report,Matriz_Clasificacion,TypeG,X_validation,Y_validation,ClasificacionRL):
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






    layout = html.Div([
        # Gráfica de validación
        dcc.Graph(figure=graph_vali),

        # Tabla
        table,

        # Exactitud
        html.H3(f'Exactitud: {exactitud}'),

        # Grid con las secciones classification_report_div y dcc.Graph(figure=roc_curve_fig)
        html.H3('Reporte de Clasificación:'),

        Grid_layout
    ])

    return layout