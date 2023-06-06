import dash
from dash import dash_table,dcc,html
import base64
import pandas as pd
import numpy as np
from .. import components as comp
import plotly.express as px


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


def interactive_pairplot(df):
    fig = px.scatter_matrix(df, dimensions=df.columns, color='comprar')   
    fig.update_traces(marker=dict(size=3)) 
    fig.update_layout(
        height=800,
        width = 600,
        title='Densidad y gráficas de dispersión',
        font=dict(size=10),
        plot_bgcolor='#F9F9F9',
        paper_bgcolor='#F9F9F9',
        showlegend=True,
        hovermode='closest',
        hoverlabel=dict(bgcolor="white", font_size=10),
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
    )
    
    return dcc.Graph(figure=fig)

def extract_titles_columns(df):
    column_names = df.columns.tolist()
    print(column_names)
    return column_names

def select_items_df(array_items):
    items_select = [{"value": item, "label": item} for item in array_items]
    return items_select

def drop_column(df,column_name):
    df = df.drop(column_name,axis=1)
    return df