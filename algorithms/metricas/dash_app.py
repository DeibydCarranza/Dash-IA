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
    layouts.standarizar
    ],
    style={'width': '100%', 'height': '100%'}
)   
"""—————————— callbacks ———————————————————"""
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
    
@app.callback(
    Output('container-button-timestamp', 'children'),
    [Input('btn-nclicks-nor', 'n_clicks'),
     Input('btn-nclicks-esc', 'n_clicks'),
     Input('btn-nclicks-view', 'n_clicks')]
)
def update_output(btn1_clicks, btn2_clicks, btn3_clicks):
    ctx = dash.callback_context
    global estandarizar
    global df
    if not ctx.triggered:
        return ''

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'btn-nclicks-nor':
        estandarizar = mt.normalizar(df)
    elif button_id == 'btn-nclicks-esc':
        estandarizar = mt.escalar(df)
    elif button_id == 'btn-nclicks-view':
        estandarizar = tl.convert_to_dataframe(estandarizar) # numpy to dataframe        
        return tl.render_results(estandarizar)
    return ''