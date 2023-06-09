import dash
from dash import dcc, html, Input, Output, callback, State
from .. import components
import os
from . import tool as tl
from django_plotly_dash import DjangoDash
from . import method as met
import dash_mantine_components as dmc


columns_values_global = [] 
col_tot_Can = ['Diagnosis','Radius', 'Texture','Area','Smoothness','Compactness', 'Concavity', 'ConcavePoints','Symmetry','FractalDimension']
col_tot_Diab = ['Pregnancies','Glucose','BloodPressure','SkinThickness','Insulin','BMI','DiabetesPedigreeFunction','Age','Outcome'] 

# ---------- Iniciando aplicación ---------------
app = DjangoDash('section_regression')
path_file = os.path.join(os.path.dirname(__file__), '../data/file.csv')
df = None
df_filtered = None
callback_values ={}

# ------- Funciones -----------

def create_show_inputs_function(column):
    @app.callback(
        Output("output-container-prono-{}".format(column), "children"),
        [Input("input-prono-{}".format(column), "value")]
    )
    def show_inputs(input1):      
        # Si el valor del input no es nulo, almacena la clave-valor en el diccionario
        if input1 is not None:
            callback_values[column] = input1
        
        return u'Input 1 {}'.format(input1)

    return show_inputs


for column in col_tot_Can:
    show_inputs_function = create_show_inputs_function(column)
for column in col_tot_Diab:
    show_inputs_function = create_show_inputs_function(column)

## ----------  Sección a renderizar   ----------
app.layout = html.Div(
    children=[
        dmc.Text("Carga de archivo", weight=700,style={"fontSize": 25,'text-align': 'center', 'margin-bottom': '30px', 'margin-top': '50px'}),
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

# Realizando la clasificación de elementos
@app.callback(
    Output("output-container-prono", "children"),
    [Input("pronosticar-button", "n_clicks")]
)
def show_callback_values(n_clicks):
    if n_clicks is not None and n_clicks > 0:
        # Leer los valores del diccionario callback_values
        values = callback_values.values()
        columns = callback_values.keys()
        print(callback_values)
        if any(value is None or value == '' for value in values):
            return "Ingrese los valores de todos los campos"
        
        resultado = met.pronosticar(values,columns)# Mostrar los valores en el contenedor de salida
        return f"De acuerdo a los datos, la clasificación con los datos mostrados es el grupo {resultado}, considere que solo es un posible escenario a futuro. Igualmente revise la el significado de dicha clasificación"
    
    return "Ingrese los valores de todos los campos"