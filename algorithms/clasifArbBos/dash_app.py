import dash
from dash import dcc, html,Input, Output, callback, State
from .. import components
import os
from . import tool as tl
from . import layout as lay
from . import method as met
from django_plotly_dash import DjangoDash
import dash_mantine_components as dmc
from sklearn.tree import export_text


app = DjangoDash('section_clasifArbBosq')
path_file = os.path.join(os.path.dirname(__file__), '../data/file.csv')
df = None
df_filtered = None
columna_filtrada = None
columns_values_global = [] 

X_t = None
X_val = None
Y_t = None
Y_val = None

n_estimators_glo = None
ClasiBA = None
Y_ClasiBA = None
clasifiAD = None
choose_Estimator_glo = None
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
    global df, df_filtered,columna_filtrada
    if list_of_contents is None:
        return html.Div('No se seleccionó ningún archivo.')
    else:
        render, df, df_filtered, columna_filtrada = tl.parse_contents(list_of_contents, list_of_names, path_file)

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
    global columns_values_global, X_t, X_val, Y_t, Y_val
    columns_values_global = columns_values
    
    # Si no se ha presionado "Entrenar" y no se han ingresado mínimo 2 columnas en dropdwon 
    if n_clicks is not None and columns_values is not None and len(columns_values) > 1:
        #Se establece un valor por defecto en el tamaño
        if size_train is None:
            size_train = 20
        X_t, X_val, Y_t, Y_val = met.variablesClasePredict(df,columns_values,columna_filtrada,(size_train/100),random_state,shuffle)
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
    global X_t, X_val, Y_t, Y_val, clasifiAD
    if n_clicks > 0:
        res_layoutAD, clasifiAD = met.trainingTrees(columns_values_global, X_t, X_val, Y_t, Y_val, max_depth, min_samples_split, min_samples_leaf, random_state)
        return [
            res_layoutAD
        ]
    else:
        return []

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
    global n_estimators_glo, ClasiBA, Y_ClasiBA
    n_estimators_glo = n_estimators
    if n_clicks > 0:
        res_layoutBA, ClasiBA, Y_ClasiBA = met.trainingForest(columns_values_global,X_t, X_val, Y_t, Y_val, max_depth,min_samples_split,min_samples_leaf,random_state ,n_estimators)
        return [
            res_layoutBA
        ]
    else:
        return []


# Estableciendo núm estimadores para el bosque 
@app.callback(Output('tree-image-forest', 'children'),
              [Input('btn-n-estimators', 'n_clicks')],
              [State('input_n_estimators', 'value')])
def update_output_bosque(n_clicks, choose_Estimator):
    global n_estimators_glo, ClasiBA, Y_ClasiBA,choose_Estimator_glo
    if n_clicks > 0:
        # Validar el rango del valor del Input
        if choose_Estimator is not None and 0 < choose_Estimator < n_estimators_glo:
            choose_Estimator_glo = choose_Estimator
            Estimador = ClasiBA.estimators_[choose_Estimator]
            tree = components.plotTree(Estimador,columns_values_global,Y_ClasiBA)

            layout = html.Div([
                html.Img(src='data:image/png;base64,{}'.format(tree), style={'width': '100%', 'height': 'auto'}),
                dmc.Button("Generar Reporte", id="btn-descarga-bosque",variant="gradient"),
                dcc.Download(id="download-reporte-bosque")
            ]),
            return layout
        else:
            return f"El valor debe ser mayor a 0 y menor a {n_estimators_glo}."
    else:
        return None



@app.callback(
    Output("download-reporte-bosque", "data"),
    [Input("btn-descarga-bosque", "n_clicks")],
    prevent_initial_call=True
)
def descargar_reporte_bosque(n_clicks):
    global choose_Estimator_glo, ClasiBA
    Estimador = ClasiBA.estimators_[choose_Estimator_glo]
    contenido = export_text(Estimador,feature_names =columns_values_global)
    return dict(content=contenido, filename="reporteBosque.txt")


@app.callback(
    Output("download-reporte-arbol", "data"),
    [Input("btn-descarga-arbol", "n_clicks")],
    prevent_initial_call=True
)
def descargar_reporte_arbol(n_clicks):
    global clasifiAD
    contenido = export_text(clasifiAD,feature_names =columns_values_global)
    return dict(content=contenido, filename="reporteArbol.txt")



