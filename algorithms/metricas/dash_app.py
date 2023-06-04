# PyPl
import dash
from dash import Input, Output,State, callback,dash_table, html,ctx
import os 
from django_plotly_dash import DjangoDash
# Owner
from .. import components
from . import layouts
from . import tool as tl
from . import method as mt
path_file = os.path.join(os.path.dirname(__file__), '../data/file.csv')

df = None
estandarizar = None
""" ———————— Instancia de la app ————————"""
app = DjangoDash('section_metricas')
# to get acces fili project

""" ——————————————— Body ——————————————"""
app.layout = html.Div(children=[
    components.upload_component,
    layouts.standarizar,
    layouts.select_algorithm,
    layouts.p_to_minkowski
    ],
    style={'width': '100%', 'height': '100%'}
)   
"""—————————— callbacks ———————————————————"""
# DragandDrop
@app.callback(
        [Output('button-container-est', 'style'),
        Output('output-data-upload', 'children')],
        [Input('upload-data', 'contents')],
        [State('upload-data', 'filename')]
)
def update_output(list_of_contents, list_of_names):
    global df
    if list_of_contents is None:
        return {'display': 'none'}, html.Div('No se seleccionó ningún archivo.')
    else:
        render, df = tl.parse_contents(list_of_contents, list_of_names, path_file)
        return {'display': 'block'}, [render]
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
     

