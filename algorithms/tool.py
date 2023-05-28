import dash
from dash import dash_table,dcc,html
import base64
import pandas as pd
import os

global path_file
path_file = os.path.join(os.path.dirname(__file__), '../',  'data', 'file.csv')

""" Save data on file, generete dataframe and return dash_tabe """
def parse_contents(contents, filename):
    _, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    global path_file
    print(path_file+"dddddddddddddddddddddddd")
    try:
        if 'csv' in filename:
            # writin on file
            write_on_file(decoded)        
            print(path_file)
            # generating dataframe
            print("--------------------")
            df = pd.read_csv(path_file, header=None) ##Considerar si lleva o no encabezado
            # Generate html component
            render = render_results(df)
    except Exception as e:
        print(e)
        return html.Div([
            'Archivo erroneo, solo archivos .csv'
        ])

    return render

""" Create and return dash_table """
def create_data_table(df):
    table = dash_table.DataTable(
        id="database-table",
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        sort_action="native",
        sort_mode="native",
        page_size=10,
        style_table={'overflowX': 'scroll','overflowY': 'scroll'}
    )
    return 

""" Generate table """
def render_results(df):
    # Create Data Table
    table = create_data_table(df)

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
def write_on_file(decoded):
    global path_file
    with open(path_file, 'w') as f:
            f.write(decoded.decode("utf-8"))
