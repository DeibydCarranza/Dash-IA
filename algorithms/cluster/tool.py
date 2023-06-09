import dash
from dash import dash_table,dcc,html
import base64
import pandas as pd
import numpy as np
from .. import components as comp
import plotly.express as px
import seaborn as sns
import plotly.graph_objects as go
import matplotlib.pyplot as mplo

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

"""" Matriz de correlaciones """
def interactive_correlation_matrix(df):
       correlation_matrix = df.corr()
       mask = np.tri(correlation_matrix.shape[0], k=0)
       correlation_matrix = np.where(mask, correlation_matrix, np.nan)
       correlation_matrix = np.flipud(correlation_matrix)  # Invertir las filas de la matriz
       fig = go.Figure(data=go.Heatmap(
              z=correlation_matrix,
              x=df.columns,
              y=df.columns[::-1],
              colorscale='RdBu_r',
              zmin=-1,
              zmax=1,
              colorbar=dict(
              title='Correlación'
              ),
              hovertemplate='x: %{x}<br>y: %{y}<br>correlation: %{z}<extra></extra>'
       ))

       fig.update_layout(
              title='Matriz de correlación',
              height=500,
              width=500,
              xaxis_showgrid=False,
              yaxis_showgrid=False,
              template='plotly_white'
       )
       return dcc.Graph(figure=fig)

def interactive_pairplot(df_original,df_noTag,tag_to_color):
    print(df_noTag)
    fig = go.Figure(data=go.Splom(
                    dimensions = [dict(label=column, values=df_noTag[column]) for column in df_noTag.columns],
                    marker=dict(color=df_original[tag_to_color],
                                size=5,
                                colorscale='Bluered',
                                line=dict(width=0.5,color='rgb(230,230,230)')),
                    diagonal=dict(visible=True)))
    fig.update_layout(dragmode='select',
                    width=1000,
                    height=1000,
                    showlegend=False,
                    hovermode='closest')
    return dcc.Graph(figure=fig)

def matrix_redimensionada(df_standarAndNoTag,Array_attributs):
    MatrizHipoteca = np.array(df_standarAndNoTag[Array_attributs])
    df = pd.DataFrame(MatrizHipoteca)
    return df
def extract_values_columns(df, column):
    unique_values = sorted(df[column].unique())
    return unique_values
def where_cluster_is(df,number):
    df_where = df[df.clusterH == number]
    return df_where