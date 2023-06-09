# PyPl
import dash
from dash import Input, Output,State, callback,dash_table, html,ctx,dcc
from dash.exceptions import PreventUpdate
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
df_without_tag = None
df_feature = None
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
                        label="Archivo",
                        description="Carga un dataset",
                        children=[components.upload_component,
                                  layouts.select_input]
                    ),
                    dmc.StepperStep(
                        label="Selecciónn de caracteristicas",
                        description="Reduciendo la dimensionalidad",
                        children= [layouts.matrix_cluster,
                                    layouts.MultiSelect_to_featuring,
                                    html.Div(id='Output-Graph_feature')]
                    ),
                    dmc.StepperStep(
                        label="Estandarización",
                        description="Generando todas las variables tengan el mismo impacto",
                        children=layouts.standarizar
                    ),
                    dmc.StepperStep(
                        label="Clustering",
                        description="Aplicando algoritmo",
                        children=[layouts.clustering]
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
    global df_feature
    if step == 2: # limitamos su ejecución a solo el step 2 (3)
        if not ctx.triggered:
            return {'display': 'none'},''

        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        print(button_id)
        if button_id == 'btn-nclicks-nor':
            estandarizar = mt.normalizar(df_feature)
        elif button_id == 'btn-nclicks-esc':
            estandarizar = mt.escalar(df_feature)
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
# Matrix Y Mapa de calor
@app.callback(
    Output('output_tabs_clustering', 'children'),
    [Input('tab_clustering', 'value'),
     Input('store_tag', 'data')]
)
def render_content(typeGraph,tag):
    global df,df_without_tag
    if typeGraph == "despersion":
        return tl.interactive_pairplot(df,df_without_tag,tag)
    elif typeGraph == "correlacion":
        return tl.interactive_correlation_matrix(df_without_tag)
    else: 
        raise PreventUpdate
#Display items on multiselect
@app.callback(
    Output('input_multiselect','data'),
    Input('store_select','data')
)
def fill_multiselectiong(step):
    global df_without_tag
    if step == 1:
         data_array = tl.select_items_df(tl.extract_titles_columns(df_without_tag))
         return data_array
    else: 
        raise PreventUpdate
#Generate matrix to work
@app.callback(
    Output('Output-Graph_feature', 'children'),
    [Input('generate_matrix_ok', 'n_clicks'),
     Input('input_multiselect','value')]
)
def print_text(n_clicks,value):
    global df_feature
    ctx = dash.callback_context
    if not ctx.triggered:
        print('else')
        raise PreventUpdate
    button_id = ctx.triggered[0]['prop_id']
    if button_id == "generate_matrix_ok.n_clicks":
        df_feature = tl.matrix_redimensionada(df_without_tag,value)
        matrix = tl.render_results(df_feature)
        print(type(df_feature))
        return matrix
    else:
        print('else')
        raise PreventUpdate
# Logic
@app.callback(
    [Output('output_tabs_logic_Clu', 'children'),
     Output('store_logic','data')],
    [Input('tap_logic_clustering', 'value')]
)
def render_content(type_Algorith):
    global df_without_tag
    if type_Algorith == "j":
        return [layouts.buttons_j],type_Algorith
    elif type_Algorith == "p":
        return None
    else: 
        raise PreventUpdate
# Buttons J to graph
@app.callback(
    [Output('output_b_j', 'children'),
     Output('select_clustering','data'),
     Output('div_panorama','style')],
    [Input('send_info_graphJ', 'n_clicks'), #clicks
     Input('store_select', 'data'), #step
     Input('store_logic', 'data'),  #type algorithm
     Input('store_metric', 'data'), # matric
     Input('store_minkowski', 'data')], # lambda
     State('numClusters', 'value')
)
def update_output(n_clicks,step,type_Algorith,metric,l,numClusters):
    global estandarizar,df
    ctx = dash.callback_context
    if step == 3 and type_Algorith == 'j':
        if not ctx.triggered:
            raise PreventUpdate
        button_id = ctx.triggered[0]['prop_id']
        if button_id == "send_info_graphJ.n_clicks":
            if len(numClusters) > 0:
                # print table with clusters
                df,table = mt.creat_cluster_tags(df,estandarizar,numClusters,metric)
                # asignar distinct(clusterH)
                data_array = tl.select_items_df(tl.extract_values_columns(df,'clusterH'))
                print(data_array)
                return table,data_array,{'display': 'block'}
            else:
                return 'Llena los campos',None,{'display': 'none'}

#Metricas
@app.callback([Output('input-to-minkowski', 'style'),
               Output('output-valor', 'style'),
               Output('store_metric', 'data')], 
               Input("framework-select-metricas", "value"))
def select_value(type):
    global estandarizar
    if type == 'minkowski':
        return  {'display': 'block'},{'display': 'block'},type
    elif type != None and type != 'minkowski':
        return {'display': 'none'},{'display': 'none'},type
    else:
         return {'display': 'none'},{'display': 'none'},None
#Selecting lambda
@app.callback(
    [Output('output-valor', 'children'),
     Output('store_minkowski', 'data')],
    Input('lambda', 'value')
)
def leer_valor(valor_lambda):
    global estandarizar
    if  valor_lambda != '0':
        # matriz = mt.matriz_distancia('Minkowski',float(valor_lambda),estandarizar)
        # matriz = tl.render_results(matriz)
        return 'Valor valido',valor_lambda
    elif valor_lambda =='0':
        return 'Debe ser mayor a 0', None
    else:
        return 'El campo de entrada está vacío',None

# Display tables to specific cluster
@app.callback(
    Output("output_select_clustering", "children"),
    Input("select_clustering", "value")
)
def display_cluster(value):
    global df
    if value == '':
        raise PreventUpdate  # No hay cambio de valor, no se ejecuta el callback
    else:
        df_where = tl.where_cluster_is(df,int(value))
        table_where = tl.render_results(df_where)
        return table_where
    
@app.callback(
    Output("output_panorama_general", "children"),
    [Input("info_general", "n_clicks"),
     Input('store_metric','data')]
)
def display_general_cluster(nclicks,metric):
    global df
    ctx = dash.callback_context
    if metric is not None or len(metric)>0:
        if not ctx.triggered:
            raise PreventUpdate
        button_id = ctx.triggered[0]['prop_id']
        if button_id == "info_general.n_clicks":
            df_resumem = mt.panorama_general_cluster(df)
            table_resume = tl.render_results(df_resumem)
            return table_resume
        else:
            raise PreventUpdate
    else:
        return 'Primero aplica la closterización'