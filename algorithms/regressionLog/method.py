import pandas as pd
import plotly.express as px       
import plotly.graph_objects as go
from dash import dcc, html,dash_table

import numpy as np 
from sklearn import model_selection
from sklearn import linear_model
from sklearn.metrics import classification_report
from sklearn.metrics import roc_curve
from sklearn.metrics import RocCurveDisplay
from sklearn.metrics import accuracy_score  
import dash_bootstrap_components as dbc


ClasificacionRL = None
X_validation= None
Y_validation = None
Y_ClasificacionRL = None
TypeG = "Diabetes"

# Variables predictoras y variables de clase
def variablesClasePredict(df,columns_values,claseSalida,size,random_s,shuffle):
    global TypeG
    if claseSalida == 'Diagnosis':
        df = df.replace({'M': 0, 'B': 1})
        TypeG = 'Cáncer'

    #Variables predictoras
    X = np.array(df[columns_values])

    #Variable clase
    Y = np.array(df[claseSalida])

    score = entrenamiento(X,Y,size,random_s,shuffle)

#Entrenamiendo del modelo
def entrenamiento(X,Y,size,random_s,shuffle):
    global ClasificacionRL,X_validation,Y_validation,Y_ClasificacionRL

    X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, 
                                                                test_size = size, 
                                                                random_state = random_s,
                                                                shuffle = shuffle)
    #Se entrena el modelo a partir de los datos de entrada
    ClasificacionRL = linear_model.LogisticRegression()
    ClasificacionRL.fit(X_train, Y_train)

    #Predicciones probabilísticas de los datos de prueba
    Probabilidad = ClasificacionRL.predict_proba(X_validation)

    #Clasificación final 
    Y_ClasificacionRL = ClasificacionRL.predict(X_validation)


# Validación del modelo
def modelValidation():
    global ClasificacionRL,X_validation,Y_validation,Y_ClasificacionRL
    ModeloClasificacion = ClasificacionRL.predict(X_validation)
    Matriz_Clasificacion = pd.crosstab(Y_validation.ravel(), 
                                   ModeloClasificacion, 
                                   rownames=['Reales'], 
                                   colnames=['Clasificación']) 
    
    exactitud = accuracy_score(Y_validation,Y_ClasificacionRL)

    report = classification_report(Y_validation, Y_ClasificacionRL)


    ## ------ Gráficas y Layout
    layout = section_graphs_interactive(exactitud,report,Matriz_Clasificacion)

    return layout



def section_graphs_interactive(exactitud,report,Matriz_Clasificacion):
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