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
            return render, df
    except Exception as e:
        print(e)
        return html.Div([
            'Archivo erroneo, solo archivos .csv'
        ])

    return render, None



""" Generate table """
def render_results(df):
    # Create Data Table
    table = comp.create_data_table(df, True)

    # Tratamiento de los datos, suprime las columnas que tiene valores no numéricos
    dff = comp.validar_columnas_numericas(df)
    graph_corr = comp.interactive_table(dff)
    correlation_matriz = comp.interactive_correlation_matrix(dff)

    # Create Layout
    res = html.Div(
        children=[
            table,

            dcc.Tabs(id="tabs-example-graph", value='tab-matrices-graph',children=[
                    dcc.Tab(label='Matriz de correlaciones', value='tab-1-example-graph', children=[
                            graph_corr
                            ]
                    ),
                    dcc.Tab(label='Mapa de calor', value='tab-2-example-graph',children=[
                            correlation_matriz
                        ]),
                ]
            ),
            
            html.Div("Veamos qué pasa"),
        ],
        className='render-container',
        style={
            'width': '100%',
        })
    return res



"""Create Pandas DataFrame from local CSV."""
def write_on_file(decoded,path_file):
    with open(path_file, 'w') as f:
            f.write(decoded.decode("utf-8"))
