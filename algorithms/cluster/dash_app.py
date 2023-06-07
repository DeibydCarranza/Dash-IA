# PyPl
import dash
from dash import Input, Output,State, callback,dash_table, html,ctx,dcc
import os 
from django_plotly_dash import DjangoDash
import dash_mantine_components as dmc
# Owner
from .. import components
from . import layouts
from . import tool as tl
from . import method as mt
path_file = os.path.join(os.path.dirname(__file__), '../data/file.csv')

df = None
estandarizar = None
""" ———————— Instancia de la app ————————"""
app = DjangoDash('section_cluster')
# to get acces fili project

min_step = 0
max_step = 4
active = 0
""" ——————————————— Body ——————————————"""
app.layout= html.Div(
    [
            dcc.Store(id="store_select"),
            dmc.Stepper(
                id="stepper-basic-usage",
                active=active,
                breakpoint="sm",
                children=[
                    dmc.StepperStep(
                        label="Upload files",
                        description="Draw and drop your files",
                        children=[components.upload_component,layouts.select_input]
                    ),
                    dmc.StepperStep(
                        label="Feature Selection",
                        description="Reducing the dimensionality of the dataframe",
                        children= layouts.matrix_cluster
                    ),
                    dmc.StepperStep(
                        label="Data Standardization",
                        description="Helping all variables have the same impact",
                        children=layouts.standarizar
                    ),
                    dmc.StepperStep(
                        label="Metrics",
                        description="Get full access",
                        children=[layouts.select_algorithm,
                                layouts.p_to_minkowski]
                    ),
                    dmc.StepperCompleted(
                        children=dmc.Text(
                            "Completed, click back button to get to previous step",
                            align="center",
                        )
                    ),
                ],
            ),
            dmc.Group(
                position="center",
                mt="xl",
                children=[
                    dmc.Button("Back", id="back-basic-usage", variant="default"),
                    dmc.Button("Next step", id="next-basic-usage"),
                ],
            ),
    ],style={'width': '100%', 'height': '100%'}
)

"""—————————— callbacks ———————————————————"""
#Select
@app.callback(
    [Output("stepper-basic-usage", "active"),
     Output("store_select","data")],
    [Input("back-basic-usage", "n_clicks"),
    Input("next-basic-usage", "n_clicks")],
    State("stepper-basic-usage", "active"),
    prevent_initial_call=True,
)
def update(back, next_, current):
    ctx = dash.callback_context
    if not ctx.triggered:
        return ''

    button_id = ctx.triggered[0]['prop_id']
    step = current if current is not None else active
    if button_id == "back-basic-usage.n_clicks":
        step = step - 1 if step > min_step else step
    else:
        step = step + 1 if step < max_step else step
    return step,step


# DragandDrop
@app.callback(
        [Output('button-container-est', 'style'),
        Output('output-data-upload', 'children'),
        Output('tag', 'style'),
        Output('select_tag_clu', 'data')],
        [Input('upload-data', 'contents')],
        [State('upload-data', 'filename')]
)
def update_output(list_of_contents, list_of_names):
    global df
    if list_of_contents is None:
        return {'display': 'none'}, html.Div('No se seleccionó ningún archivo.'),{'display': 'none'},[]
    else:
        # Escribiendo en el archivo y retornando la tabla
        render, df = tl.parse_contents(list_of_contents, list_of_names, path_file)
        # leyendo los nombre las de las columnas y agrgandolos en un array
        data_array = tl.select_items_df(tl.extract_titles_columns(df))
        return {'display': 'block'}, [render],{'display': 'block'},data_array


# Estandarizar
@app.callback(
    [Output('select-metricas', 'style')
    , Output('container-button-timestamp','children')],
    [Input('btn-nclicks-nor', 'n_clicks'),
     Input('btn-nclicks-esc', 'n_clicks'),
     Input('btn-nclicks-view', 'n_clicks')]
)
def update_output(btn1_clicks, btn2_clicks, btn3_clicks):
    ctx = dash.callback_context
    global estandarizar
    global df
    if not ctx.triggered:
        return {'display': 'none'},''

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'btn-nclicks-nor':
        estandarizar = mt.normalizar(df)
    elif button_id == 'btn-nclicks-esc':
        estandarizar = mt.escalar(df)
    elif button_id == 'btn-nclicks-view':
        estandarizar = tl.convert_to_dataframe(estandarizar) # numpy to dataframe        
        return {'display': 'block'},tl.render_results(estandarizar)
    return {'display': 'none'},''

# Metricas
@app.callback([Output('input-to-minkowski', 'style'),
               Output('selected-value-metricas', "children"),
               Output('output-valor', 'style')], 
               Input("framework-select-metricas", "value"))
def select_value(type):
    global estandarizar
    if type == 'minkowski':
        return  {'display': 'block'}, '', {'display': 'block'}
    elif type != None and type != 'minkowski':
        matriz = mt.matriz_distancia(type,None,estandarizar)
        matriz = tl.render_results(matriz)
        return {'display': 'none'}, matriz,{'display': 'none'}
    else:
         return {'display': 'none'}, '',{'display': 'none'}

@app.callback(
    Output('output-valor', 'children'),
    [Input('button-leer-valor', 'n_clicks')],
    [State('lambda', 'value')]
)
def leer_valor(n_clicks, valor_lambda):
    global estandarizar
    if n_clicks is not None:
        if valor_lambda and valor_lambda != '0':
            matriz = mt.matriz_distancia('Minkowski',float(valor_lambda),estandarizar)
            matriz = tl.render_results(matriz)
            return matriz
        elif valor_lambda and valor_lambda =='0':
            return 'Lambda no puede ser 0'
        else:
            return 'El campo de entrada está vacío'
    return ''

@app.callback(
    Output('output_matrix_clu', 'children'),
    Input('stepper-state_clu', 'data')
)
def display_matrix(numSteper):
    global df
    print('*******************')
    print(numSteper)
    print(df)
    if numSteper == 1:
        matrix = tl.interactive_pairplot(df)
        print(tl.extract_titles_columns(df))
        return matrix
    else:
        return ''

# @app.callback(Output("output-data-upload", "children"),
#               Input("select_tag_clu", "value"))
# def select_value(value):
#     global df
#     # sobreescribiendo el df sin la etiqueta
#     df = tl.drop_column(df,value)
#     render = tl.render_results(df)
#     return render
    
