from dash import Input, Output, callback, State
from .. import tool as tl 

""" Callbacks """
@callback(
       Output('output-data-upload', 'children'),
       Input('upload-data', 'contents'),
       State('upload-data', 'filename'))
def update_output(list_of_contents, list_of_names):
       print("Entro")
       children = [
              tl.parse_contents(list_of_contents, list_of_names)]
       return children