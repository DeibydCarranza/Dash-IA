import dash
from dash import dash_table,dcc,html
import base64
import pandas as pd
import os
from .. import components as comp
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

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
            render,df_filtered,columna_filtrada = render_results(df)
            return render, df, df_filtered,columna_filtrada
    except Exception as e:
        print(e)
        return html.Div([
            'Archivo erroneo, solo archivos .csv'
        ])

    return render, None, None, None



""" Generate table """
def render_results(df):
    # Create Data Table
    table = comp.create_data_table(df, True)

    # Tratamiento de los datos, suprime las columnas que tiene valores no numéricos
    df_filtered = comp.validar_columnas_numericas(df)


    # Omitir las variables de clase que corresponden a Y 
    columnas = [col for col in df_filtered.columns if col not in ['Diagnosis', 'Outcome', 'SITUACION', 'fetal_health']]
    columna_filtrada = [col for col in df.columns if col in ['Diagnosis', 'Outcome', 'SITUACION', 'fetal_health']]

    # Create Layout
    res = html.Div(
        children=[
            table,

            html.Div("Ingresa al menos 2 características a evaluar"),
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
            
            dmc.Button('Entrenar', id='btn-train', n_clicks=0,variant="gradient"),

            html.Div("",style={'margin-bottom':'40px'}),

            #Sección para poder desplegar las gráficas de correlaciones
            html.Div([
                dmc.Button("Apoyo para seleccionar columnas", id="toggle-button-1",variant="gradient"),
                html.Div(id="acordeon-content-1")
            ]),
            
            html.Div(id='model-validation-layout')



        ],
        className='render-container',
        style={
            'width': '100%',
        })
    return res,df_filtered,columna_filtrada

"""Create Pandas DataFrame from local CSV."""
def write_on_file(decoded,path_file):
    with open(path_file, 'w') as f:
            f.write(decoded.decode("utf-8"))
