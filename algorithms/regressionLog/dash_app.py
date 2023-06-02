import dash
from dash import dcc, html,Input, Output, callback, State
from .. import components
import os
from . import tool as tl 
from django_plotly_dash import DjangoDash
from . import method as met


#  ---------- Iniciando aplicación ---------------
app = DjangoDash('section_regression')
path_file = os.path.join(os.path.dirname(__file__), '../data/file.csv')
df = None
df_filtered = None


# ------- Funciones -----------






## ----------  Seción a renderizar   ---------- 
app.layout = html.Div(children=[
    components.upload_component
],
style={'width': '100%', 'height': '100%'}
)   


#  - ---- Callbacks individuales -----------

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
    Output('columns-output-container-1', 'children'),
    [Input('btn-train', 'n_clicks')],
    [State('columns-dropdown-1', 'value'),
     State('input_size_train_1', 'value'),
     State('input_random_state_1', 'value'),
     State('boolean-switch_1', 'on')]
)
def update_output_columns(n_clicks, columns_values, size_train, random_state, shuffle):
    #Seleccionamos la variable de resultados manualmente
    claseSalida = 'Diagnosis' if 'Diagnosis' in df.columns else 'Outcome'

    if n_clicks is not None and columns_values is not None and len(columns_values) >0:
        score = met.variablesClasePredict(df, columns_values, claseSalida, (size_train/100), random_state, shuffle)
        
        met.modelValidation()
        return f'Carga exitosa de entrenamiento'
    return f'No has seleccionado ninguna variable para entrenar'


# Toggle display
@app.callback(
    Output("acordeon-content-1","children"),
    [Input("toggle-button-1","n_clicks")]
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