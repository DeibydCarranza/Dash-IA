from dash import dcc, html,dash_table
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_curve, auc
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt
import base64
import io

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
              'padding-bottom: 10%',
              'background-color':'#ff008d14',
              'margin-bottom': '4rem',
              'font-weight': '700',
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
    fig.update_traces(marker=dict(size=3)) 

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

"""" Coorelational Matrix & heatmap"""
def correlational_matrix(df):
       graph_corr = interactive_table(df)
       correlation_matriz = interactive_correlation_matrix(df)

       layout = html.Div([
              dcc.Tabs(id="tabs-example-graph", value='tab-matrices-graph',children=[
                     dcc.Tab(label='Matriz de correlaciones', value='tab-1-example-graph', children=[
                            graph_corr
                     ]),
                     dcc.Tab(label='Mapa de calor', value='tab-2-example-graph',children=[
                            correlation_matriz
                     ]),
              ],style={'margin-bottom':'70px'}
              )
       ])
       return layout

""" Input de size_train, random_state, shuffle"""
def mod_params_train(index):
    layout = dbc.Container([
        html.Div("Por defecto se han prestablecido valores, modifícalos a tu gusto si así lo deseas"),
        dbc.Row([
            dbc.Col([
                html.Label("Tamaño de entrenamiento %"),
                dcc.Input(
                    id=f"input_size_train_{index}",
                    type="number",
                    placeholder="Size train %",
                    min=1,
                    max=100,
                    step=0.1,
                    value=None,
                    className="input-field"
                )
            ], width=4),
            dbc.Col([
                html.Label("Semilla random"),
                dcc.Input(
                    id=f"input_random_state_{index}",
                    type="number",
                    placeholder="Valor random",
                    value=None,
                    className="input-field"
                )
            ], width=4),
            dbc.Col([
                html.Label("Shuffle"),
                dmc.Switch(id=f"boolean-switch_{index}",onLabel="True",offLabel="False",checked=True,size="xl", color="red")
            ], width=4)
        ], className="input-row")
    ], className="input-container")

    return layout


""" Input de size_train, random_state, shuffle"""
""" Index->unique for ID, type_algorithm->to create or not 1 input extra for  'ForestDesicion'"""
def params_tree_fores(index,type_algorithm):
    layout = dbc.Container([
        html.Div("Al dejarlos vacíos trabajarás con valores por defecto"),
        dbc.Row([
            dbc.Col([
                html.Label("Profundidad del árbol"),
                dcc.Input(
                    id=f"input_max_depth_{index}",
                    type="number", placeholder="max_depth",className="input-field",
                    min=1,step=1,value=None,           
              )], width=3),
            dbc.Col([
                html.Label("Mínimo de divisiones "),
                dcc.Input(
                    id=f"input_min_samples_split_{index}",
                    type="number", placeholder="min_samples_split",className="input-field",
                    min=2,step=1,value=2,           
              )], width=3),
            dbc.Col([
                html.Label("Hojas permitidas como muestras"),
                dcc.Input(
                    id=f"input_min_samples_leaf_{index}",
                    type="number", placeholder="min_samples_leaf",className="input-field",
                    min=1,step=1,value=1,           
              )], width=3),
            dbc.Col([
                html.Label("Número de aleatoriedad"),
                dcc.Input(
                    id=f"input_random_state_{index}",
                    type="number", placeholder="random_state",className="input-field",
                    min=0,step=1,value=None,           
              )], width=3),          
        ], className="input-row")
    ], className="input-container")

    if type_algorithm:
        layout.children[1].children.append(
            dbc.Col([
                html.Label("Número de estimadores"),
                dcc.Input(
                    id=f"input_n_estimators_{index}",
                    type="number",placeholder="n_estimators",className="input-field",
                    min=1,step=1, value=100,
                )
            ], width=3)
        )

    return layout

""" Matriz de clasificación para todo tipo de casos"""
def matrizClasif(Matriz_Clasificacion):

    table = html.Table([
        html.Thead(
            html.Tr([html.Th('Clasificación')] + [html.Th(col) for col in Matriz_Clasificacion.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(Matriz_Clasificacion.index[i])] + [
                html.Td(Matriz_Clasificacion.iloc[i, j]) for j in range(len(Matriz_Clasificacion.columns))
            ]) for i in range(len(Matriz_Clasificacion))
        ])
    ])
    return table

""" Gráfica ROC para 2 características """
def rocBinaryGraph(X_val, Y_val, Clasificacion):
    roc_curve_fig = go.Figure()

    fpr, tpr, _ = roc_curve(Y_val, Clasificacion.predict_proba(X_val)[:, 1])

    roc_curve_fig = go.Figure(
        data=go.Scatter(
            x=fpr,
            y=tpr,
            mode='lines',
            name='Curva ROC',
            line=dict(color='blue'),
        ),
    )

    roc_curve_fig.update_layout(
        title='Curva ROC',
        xaxis=dict(title='Tasa de Falsos Positivos'),
        yaxis=dict(title='Tasa de Verdaderos Positivos'),
    )
    return roc_curve_fig



""" Gráfica ROC para múltiples características """
def rocMultipleGraph(X_val, Y_val, Clasificacion):
    y_score = Clasificacion.predict_proba(X_val)
    y_test_bin = label_binarize(Y_val, classes=[1, 2, 3])
    n_classes = y_test_bin.shape[1]

    roc_curves = []
    fpr = dict()
    tpr = dict()
    roc_auc = dict()

    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_test_bin[:, i], y_score[:, i])
        roc_auc = auc(fpr[i], tpr[i])
        roc_curve_trace = go.Scatter(x=fpr[i], y=tpr[i], mode='lines',
                                    name='ROC curve (AUC = {:0.2f})'.format(roc_auc))
        roc_curves.append(roc_curve_trace)

    diagonal_trace = go.Scatter(x=[0, 1], y=[0, 1], mode='lines',
                                name='Random', line=dict(dash='dash'))
    roc_curves.append(diagonal_trace)

    roc_curve_fig = go.Layout(
        title='Rendimiento',
        xaxis=dict(title='False Positive Rate'),
        yaxis=dict(title='True Positive Rate'),
        showlegend=True,
        legend=dict(x=0.7, y=0.1),
        hovermode='closest'
    )
    return go.Figure(data=roc_curves, layout=roc_curve_fig)


""" Imprimiendo árbol """
""" Considerar que en bosques el DataFrame (Clasificación) requiere estimadores """
def plotTree(Clasificacion, columns_values, Y_Clasificacion):

    plot_tree(Clasificacion,
                    feature_names=columns_values,
                    class_names=Y_Clasificacion.astype(str))

    # Guardar la figura en un objeto de tipo BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Codificar la imagen en base64
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return image_base64    

""" Vista en 2 pestañas de los métodos presentes AD/BA"""
def tab_for_methods():

    layout = html.Div([
            dcc.Tabs(id="tabs_methods", value='tab_method_algor',children=[
                dcc.Tab(label='Clasificación por árbol de decisión', value='tab-1', children=[
                    
                    # Llama a los inputs propios del árbol (0-> indice, False->Tipo árbol)
                    params_tree_fores(0,False),
                    dmc.Button('Generar carga de inputs', id='generate-button-tree', n_clicks=0,variant="gradient"),
                    html.Div(id='input-values-container-tree')

                ]),
                dcc.Tab(label='Clasificación por bosque aleatorio', value='tab-2',children=[
                    # Llama a los inputs propios del árbol (1-> indice, False->Tipo árbol)
                    params_tree_fores(1,True),
                    dmc.Button('Generar carga de inputs', id='generate-button-forest', n_clicks=0,variant="gradient"),
                    html.Div(id='input-values-container-forest')

                ]),
            ],style={'margin-bottom':'60px','margin-top':'30px'}
            )
       ])
    return layout