import dash
from dash import dash_table,dcc,html
import base64
import pandas as pd
import os
from .. import components as comp

""" Save data on file, generete dataframe and return dash_tabe """
def parse_contents(contents, filename,path_file):
    _, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # writin on file
            write_on_file(decoded,path_file)        
            print(path_file)
            # generating dataframe
            df = pd.read_csv(path_file) 
            # Generate html component
            render = render_results(df)
            return render
    except Exception as e:
        print(e)
        return html.Div([
            'Archivo erroneo, solo archivos .csv'
        ])

    return render



""" Generate table """
def render_results(df):
    # Create Data Table
    table = comp.create_data_table(df,True)

    # Create Layout
    res = html.Div(
        children=[
            table
        ],
        className='render-container',
        style={
            'width': '100%',
        }
    )
    return res

"""Create Pandas DataFrame from local CSV."""
def write_on_file(decoded,path_file):
    with open(path_file, 'w') as f:
            f.write(decoded.decode("utf-8"))
