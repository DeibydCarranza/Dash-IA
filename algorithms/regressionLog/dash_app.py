import dash
from dash import dcc, html, Input, Output, callback, State
from .. import components
import os
from . import tool as tl
from django_plotly_dash import DjangoDash
from . import method as met


columns_values_global = [] 

# ---------- Iniciando aplicación ---------------
app = DjangoDash('section_regression')
path_file = os.path.join(os.path.dirname(__file__), '../data/file.csv')
df = None
df_filtered = None


# ------- Funciones -----------




## ----------  Sección a renderizar   ----------
app.layout = html.Div(
    children=[
        components.upload_component,
    ],
    style={'width': '100%', 'height': '100%'}
)

# ---- Callbacks individuales -----------

# Carga de archivo y renderizado de los elementos hijos
@app.callback(
    Output('output-data-upload', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_output(list_of_contents, list_of_names):
    global df, df_filtered
    if list_of_contents is None:
        return html.Div('No se seleccionó ningún archivo.')
    else:
        render, df, df_filtered = tl.parse_contents(list_of_contents, list_of_names, path_file)

        children = [
            render
        ]
        return children

# Paso de columnas para ser procesadas mediante dropdown
@app.callback(
    [Output('columns-output-container-1', 'children'), Output('model-validation-layout', 'children')],
    [Input('btn-train', 'n_clicks')],
    [State('columns-dropdown-1', 'value'),
     State('input_size_train_1', 'value'),
     State('input_random_state_1', 'value'),
     State('boolean-switch_1', 'checked'),
     State('model-validation-layout', 'children')]
)
def update_output_columns(n_clicks, columns_values, size_train, random_state, shuffle, current_validation_layout):
    # Resto del código...
    global columns_values_global
    columns_values_global = columns_values
    # Seleccionamos la variable de resultados manualmente
    claseSalida = 'Diagnosis' if 'Diagnosis' in df.columns else 'Outcome'

    if n_clicks is not None and columns_values is not None and len(columns_values) > 0:
        #Se establece un valor por defecto en el tamaño
        if size_train is None:
            size_train = 20
        met.variablesClasePredict(df, columns_values, claseSalida, (size_train / 100), random_state, shuffle)

        layout_validation = met.modelValidation(columns_values, app)
        return f'Carga exitosa de entrenamiento', layout_validation

    return f'No has seleccionado ninguna variable para entrenar', current_validation_layout


# Toggle display
@app.callback(
    Output("acordeon-content-1", "children"),
    [Input("toggle-button-1", "n_clicks")]
)
def toggle_acordeon(n_clicks):
    if n_clicks is None:
        return []
    elif n_clicks % 2 == 1:
        return [
            components.correlational_matrix(df_filtered)
        ]
    else:
        return []



# --------  Debe leer los valores de inputs y mostrar un string o en este caso 
# -------- Un HTML renderizado con los valores
@app.callback(
    Output("output-container-prono", "children"),
    [Input("submit-button", "n_clicks")],
    [State("input-prono-{}".format(column), "value") for column in columns_values_global]
)
def show_inputs(n_clicks, *values):
    global columns_values_global 
    print(values,*values)

    print("-----------------------")
    if n_clicks is None:
        return ""
    else:
        print(columns_values_global,values)
        print(" | ".join((str(val) for val in values if val)))
        return html.Div([
            html.Label("Inputs:"),
            html.Ul([
                html.Li(f"{column}: {value}") for column, value in zip(columns_values_global, values)
            ])
        ])


""" Prueba de que con un elemento específico sí funciona"""
# @app.callback(
#     Output("output-container-prono", "children"),
#     [Input("input-prono-Radius", "value")]
# )
# def show_inputs(input1):
#     print("-----------------------")
#     print(columns_values_global,input1)
#     return u'Input 1 {}'.format(input1)