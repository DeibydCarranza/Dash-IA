import dash
from dash import dcc, html,Input, Output, callback, State
from .. import components
import os
from . import tool as tl
from . import layout as lay
from django_plotly_dash import DjangoDash

app = DjangoDash('section_clasifArbBosq')
path_file = os.path.join(os.path.dirname(__file__), '../data/file.csv')
df = None
df_filtered = None
claseFiltrada = None
columns_values_global = [] 

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
    global df, df_filtered,claseFiltrada
    if list_of_contents is None:
        return html.Div('No se seleccionó ningún archivo.')
    else:
        render, df, df_filtered, claseFiltrada = tl.parse_contents(list_of_contents, list_of_names, path_file)

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
    global columns_values_global
    columns_values_global = columns_values

    # Si no se ha presionado "Entrenar" y no se han ingresado mínimo 2 columnas en dropdwon 
    if n_clicks is not None and columns_values is not None and len(columns_values) > 1:
        print(size_train, random_state, shuffle)
        layout_models = lay.tab_for_methods()
        return f'Carga exitosa de entrenamiento', layout_models

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

# Define el callback para capturar los valores de los inputs para árbol
@app.callback(
    Output('input-values-container-tree', 'children'),
    [Input('generate-button-tree', 'n_clicks')],
    [State('input_max_depth_0', 'value'),
     State('input_min_samples_split_0', 'value'),
     State('input_min_samples_leaf_0', 'value'),
     State('input_random_state_0', 'value')]
)
def generate_input_values_tree(n_clicks, max_depth, min_samples_split, min_samples_leaf, random_state):
    if n_clicks > 0:
        valuesTree = {
            'max_depth': max_depth,
            'min_samples_split': min_samples_split,
            'min_samples_leaf': min_samples_leaf,
            'random_state': random_state
        }
        print(valuesTree)
        return valuesTree
    else:
        return ''

# Define el callback para capturar los valores de los inputs para Bosque
@app.callback(
    Output('input-values-container-forest', 'children'),
    [Input('generate-button-forest', 'n_clicks')],
    [State('input_max_depth_1', 'value'),
     State('input_min_samples_split_1', 'value'),
     State('input_min_samples_leaf_1', 'value'),
     State('input_random_state_1', 'value'),
     State('input_n_estimators_1', 'value')]
)
def generate_input_values_forest(n_clicks, max_depth, min_samples_split, min_samples_leaf, random_state, n_estimators):
    if n_clicks > 0:
        valuesForest = {
            'max_depth': max_depth,
            'min_samples_split': min_samples_split,
            'min_samples_leaf': min_samples_leaf,
            'random_state': random_state,
            'n_estimators': n_estimators
        }
        print(valuesForest)
        return valuesForest
    else:
        return ''