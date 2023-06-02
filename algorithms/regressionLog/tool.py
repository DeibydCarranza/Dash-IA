import dash
from dash import dash_table,dcc,html
import base64
import pandas as pd
import os
from .. import components as comp
import dash_bootstrap_components as dbc


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
            render,df_filtered = render_results(df)
            return render, df, df_filtered
    except Exception as e:
        print(e)
        return html.Div([
            'Archivo erroneo, solo archivos .csv'
        ])

    return render, None, None



""" Generate table """
def render_results(df):
    # Create Data Table
    table = comp.create_data_table(df, True)

    # Tratamiento de los datos, suprime las columnas que tiene valores no numéricos
    df_filtered = comp.validar_columnas_numericas(df)


    # Omitir las variables de clase que corresponden a Y 
    columnas = [col for col in df_filtered.columns if col not in ['Diagnosis', 'Outcome']]

    # Create Layout
    res = html.Div(
        children=[
            table,

            html.Div("Veamos qué pasa"),
            html.Div([
                dcc.Dropdown(
                    options=[{'label': col, 'value': col} for col in columnas],
                    id='columns-dropdown-1',
                    placeholder="Selecciona las variables a mantener",
                    multi=True,
                    optionHeight=50

                ), 
                html.Div(id='columns-output-container-1')
            ]),

            comp.mod_params_train(1),
            
            html.Button('Entrenar', id='btn-train', n_clicks=0),

            html.Div("",style={'margin-bottom':'40px'}),

            #Sección para poder desplegar las gráficas de correlaciones
            html.Div([
                html.Button("Mostrar/Ocultar", id="toggle-button-1"),
                html.Div(id="acordeon-content-1")
            ])
            


        ],
        className='render-container',
        style={
            'width': '100%',
        })
    return res,df_filtered



"""Create Pandas DataFrame from local CSV."""
def write_on_file(decoded,path_file):
    with open(path_file, 'w') as f:
            f.write(decoded.decode("utf-8"))
