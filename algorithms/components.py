from dash import dcc, html,dash_table
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

""" Generate update component (just html) """
upload_component = html.Div([
       dcc.Upload(
       id='upload-data',
       children=html.Div([
              'Carga de archivo ',
              html.A('Select CSV File')
       ]),
       style={
              'margin'
              'height': '60px',
              'lineHeight': '60px',
              'borderWidth': '2px',
              'borderStyle': 'dashed',
              'borderRadius': '5px',
              'textAlign': 'center',
              'margin': '50px 10px'
              'padding-bottom: 10%'
       },
       # Permitir cargar múltiples archivos
       multiple=False
       ),
       html.Div(id='output-data-upload'),
])

""" Create and return dash_table """
def create_data_table(df, indexFlag):
       if indexFlag:
              df_with_index = df.reset_index()
              columns = [{"name": "Index", "id": "index"}] + [{"name": i, "id": i} for i in df.columns]
              data = df_with_index.to_dict("records")
       else:
              columns = [{"name": i, "id": i} for i in df.columns]
              data = df.to_dict("records")

       table = dash_table.DataTable(
              id="database-table",
              columns=columns,
              data=data,
              sort_action="native",
              sort_mode="native",
              page_size=10,
              style_table={'overflowX': 'scroll', 'overflowY': 'scroll', 'color': '#3c3c3c'}
       )
       return table

""" Create and return correlational interactive graph """
def interactive_table(df):
    df_filtered = df.iloc[:, 1:]
    color_column = df_filtered.columns[0]
    fig = px.scatter_matrix(df_filtered, color=color_column)
    fig.update_layout(
           height=900,
           title='Matriz de correlación',
       )

    return dcc.Graph(figure=fig)

"""Validar que el dataframe solo tiene valores numéricos, si no elimina las columnas extra"""
def validar_columnas_numericas(df):
       columnas_numericas = []
       for columna in df.columns:
              if df[columna].dtype in [int, float]:
                     columnas_numericas.append(columna)
       
       df_numerico = df[columnas_numericas]
       return df_numerico

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
              height=700,
              width=700,
              xaxis_showgrid=False,
              yaxis_showgrid=False,
              template='plotly_white'
       )

       return dcc.Graph(figure=fig)


""" Input de size_train, random_state, shuffle"""
def mod_params_train(index):
    layout = html.Div([
        html.Div("Por defecto se han prestablecido valores, modifícalos a tu gusto"),
        dcc.Input(
            id=f"input_size_train_{index}", type="number", placeholder="Size train",
            min=1, max=100, step=0.1, value=None
        ),
        dcc.Input(
            id=f"input_random_state_{index}", type="number", placeholder="Valor random", value=None
        ),
        dcc.RadioItems(
            id=f"shuffle_radio_{index}",
            options=[
                {'label': 'True', 'value': 'True'},
                {'label': 'False', 'value': 'False'},
            ],
            value='True', inline=True
        )
    ])
    return layout