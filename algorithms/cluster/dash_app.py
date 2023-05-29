import dash
from dash import dcc, html,Input, Output, callback, State
from .. import components
import os
from . import tool as tl 
from django_plotly_dash import DjangoDash

app = DjangoDash('section_cluster')
path_file = os.path.join(os.path.dirname(__file__), '../data/file.csv')


app.layout = html.Div(children=[
    components.upload_component
],
style={'width': '100%', 'height': '100%'}
)   

@app.callback(
        Output('output-data-upload', 'children'),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename')
)
def update_output(list_of_contents, list_of_names):
    if list_of_contents is None:
        return html.Div('No se seleccionó ningún archivo.')
    else:
        children = [
            tl.parse_contents(list_of_contents, list_of_names, path_file)
        ]
        return children