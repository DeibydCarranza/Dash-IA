# PyPl
import dash
from dash import Input, Output,State, callback,dash_table, html,ctx,dcc
import os 
from django_plotly_dash import DjangoDash
from dash.exceptions import PreventUpdate
import dash_mantine_components as dmc
# Owner
from .. import components
from . import layouts
from . import tool as tl
from . import method as mt
path_file = os.path.join(os.path.dirname(__file__), '../data/file.csv')

df = None
df_without_tag = None
estandarizar = None
""" ———————— Instancia de la app ————————"""
app = DjangoDash('section_metricas')
# to get acces fili project

min_step = 0
max_step = 3
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
                        label="Archivo",
                        description="Carga un dataset",
                        children=[components.upload_component,
                                  layouts.select_input]
                    ),
                    dmc.StepperStep(
                        label="Estandarización",
                        description="Generando todas las variables tengan el mismo impacto",
                        children=layouts.standarizar
                    ),
                    dmc.StepperStep(
                        label="Metricas",
                        description="Aplicando algoritmo",
                        children=[layouts.select_algorithm,
                                   layouts.p_to_minkowski,
                                   layouts.compare]
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
# Upload files
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
    Output('container-button-timestamp','children'),
    [Input('btn-nclicks-nor', 'n_clicks'),
     Input('btn-nclicks-esc', 'n_clicks'),
     Input('btn-nclicks-view', 'n_clicks'),
     Input('store_select','data')]
)
def update_output(btn1_clicks, btn2_clicks, btn3_clicks,step):
    ctx = dash.callback_context
    global estandarizar
    global df_without_tag
    if step == 1: # limitamos su ejecución a solo el step 2 (3)
        if not ctx.triggered:
            return {'display': 'none'}
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        print(button_id)
        if button_id == 'btn-nclicks-nor':
            estandarizar = mt.normalizar(df_without_tag)
        elif button_id == 'btn-nclicks-esc':
            estandarizar = mt.escalar(df_without_tag)
        elif button_id == 'btn-nclicks-view':
            estandarizar = tl.convert_to_dataframe(estandarizar) # numpy to dataframe        
            return tl.render_results(estandarizar)
        else:
            raise PreventUpdate
# Upload tag
@app.callback(
    [Output("output_delete_tag", "children"),
     Output("store_tag", "data")],
    Input("select_tag_clu", "value")
)
def select_value(value):
    global df,df_without_tag
    if value == '':
        raise PreventUpdate  # No hay cambio de valor, no se ejecuta el callback
    else:
        tag = [value]
        df_without_tag = tl.drop_tag(df,tag)
        render = tl.render_results(df_without_tag)
        return render,value
# Metricas
@app.callback([Output('input-to-minkowski', 'style'),
               Output('selected-value-metricas', "children"),
               Output('output-valor', 'style'),
               Output('store_metric','data')], 
               Input("framework-select-metricas", "value"))
def select_value(type):
    global estandarizar
    if type == 'minkowski':
        return  {'display': 'block'}, '', {'display': 'block'},type
    elif type != None and type != 'minkowski':
        matriz = mt.matriz_distancia(type,None,estandarizar)
        matriz = tl.render_results(matriz)
        return {'display': 'none'}, matriz,{'display': 'none'},type
    else:
         return {'display': 'none'}, '',{'display': 'none'},None

@app.callback(
    [Output('output-valor', 'children'),
     Output('store_lambda', 'data')],
    [Input('button-leer-valor', 'n_clicks')],
    [State('lambda', 'value')]
)
def leer_valor(n_clicks, valor_lambda):
    global estandarizar
    if n_clicks is not None:
        if valor_lambda and valor_lambda != '0':
            matriz = mt.matriz_distancia('Minkowski',float(valor_lambda),estandarizar)
            matriz = tl.render_results(matriz)
            return matriz,valor_lambda
        elif valor_lambda and valor_lambda =='0':
            return 'Lambda no puede ser 0',None
        else:
            return 'El campo de entrada está vacío',None
    return ''
# Compare
@app.callback(
    Output('output_comparation', 'children'),
    [Input('comparar_send', 'n_clicks'), #clicks
     Input('store_select', 'data'), #step
     Input('store_metric','data'),
     Input('store_lambda', 'data')], #metric
    [State('element1', 'value'),
     State('elemento2', 'value'),]
)
def update_output(n_clicks,step,metric,l,element1,element2):
    global estandarizar,df
    ctx = dash.callback_context
    if step == 2:
        if not ctx.triggered:
            raise PreventUpdate
        button_id = ctx.triggered[0]['prop_id']
        if int(element1) > 0:
            element1 = int(element1)-1
        else:
            element1 = int(element1)
        if int(element2) > 0:
            element2 = int(element2)-1
        else:
            element2 = int(element2)
        if element1 > (estandarizar.shape[1]) or element2 >(estandarizar.shape[1]):
            return 'Solo numeros del 1 al '+str((estandarizar.shape[1]+1))
        if button_id == "comparar_send.n_clicks":
            if element1 >= 0 and element2 >= 0:
                result = mt.compare_elementos(estandarizar,metric,l,element1,element2)
                return  dmc.Alert(
                            result,
                            title="Alert of result",
                        )

            else:
                return 'Llena los campos'