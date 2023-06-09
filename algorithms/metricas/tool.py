import dash
from dash import dash_table,dcc,html
import base64
import pandas as pd
import numpy as np
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
            print(render)
            return render,df 
    except Exception as e:
        print(e)
        return html.Div([
            'Archivo erroneo, solo archivos .csv'
        ])

    return render,None

""" Generate table """
def render_results(df):
    # Create Data Table
    table = comp.create_data_table(df,False)

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

def convert_to_dataframe(data):
    if isinstance(data, pd.DataFrame):
        return data
    elif isinstance(data, np.ndarray):
        return pd.DataFrame(data)
    else:
        raise ValueError("El parámetro de entrada no es un DataFrame ni un arreglo de NumPy.")

def extract_titles_columns(df):
    column_names = df.columns.tolist()
    print(column_names)
    return column_names
    
def select_items_df(array_items):
    items_select = [{"value": item, "label": item} for item in array_items]
    return items_select

def drop_tag(df_original,columnas_a_excluir):
    df_nuevo = df_original.loc[:, ~df_original.columns.isin(columnas_a_excluir)]
    return df_nuevo