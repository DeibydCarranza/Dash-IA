import dash
from dash import dash_table,dcc,html
import base64
import pandas as pd
import os
from .. import components as comp
from . import method as met

""" Save data on file, generete dataframe and return dash_tabe """
def parse_contents(contents, filename,path_file):
    _, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    print("\t--------------------")
    try:
        if 'csv' in filename:
            # writin on file
            write_on_file(decoded,path_file)        
            print(path_file)
            # generating dataframe
            df = pd.read_csv(path_file, header=None) ##Considerar si lleva o no encabezado
            # Generate html component
            render = render_results(df)
            return render,df
    except Exception as e:
        print(e)
        return html.Div([
            'Archivo erroneo, solo archivos .csv'
        ])

    return render,None


""" Generate table & frecuence graph"""
def render_results(df):
    # Create Data Table
    table = comp.create_data_table(df,False)
    grap_frec = met.graphFrecu(df)
    
    # Create Layout
    res = html.Div(
        children=[
            table,
            dcc.Graph(id="graph-distribution", figure=grap_frec)
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
