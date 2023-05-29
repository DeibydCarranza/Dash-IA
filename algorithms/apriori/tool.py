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
    try:
        if 'csv' in filename:
            # writin on file
            write_on_file(decoded,path_file)        
            print(path_file)
            # generating dataframe
            df = pd.read_csv(path_file, header=None) ##Considerar si lleva o no encabezado
            # Generate html component
            render = render_results(df)
            return render
    except Exception as e:
        print(e)
        return html.Div([
            'Archivo erroneo, solo archivos .csv'
        ])

    return render



""" Generate table """
def render_results(df):
    # Create Data Table
    table = comp.create_data_table(df)
    grap_frec = met.graphFrecu(df)
    results_df = met.application(df,0.01,0.3,2.3)

    # Convertir el DataFrame en una lista de diccionarios
    res_data = results_df.to_dict('records')
    res_data = [data for data in res_data if isinstance(data, dict)]

    # Generar los títulos de la tabla y sus filas
    title_row = html.Tr([html.Th(col) for col in res_data[0].keys()] + [html.Th("Acciones")])
    titles = html.Thead(title_row)
    card_rows = []
    for index, data in enumerate(res_data):
        card_rows.extend(generate_card(data, index,res_data))

    # Generar el cuerpo de la tabla con las filas de tarjetas
    card_body = html.Tbody(card_rows)
    table_rules = html.Table([titles, card_body], id="titulos")
    cards_container = html.Div(table_rules, className='cards-container')
    
    # Create Layout
    res = html.Div(
        children=[
            table,
            dcc.Graph(id="graph-distribution", figure=grap_frec), 
            cards_container
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


""" Generación de los componentes tipo tabla donde se muestran las reglas """
def generate_card(data, index,res_data): 
    if not data:
        return None

    id_str = f"toggle-button-{index}"
    description = html.Div(
        html.P('Tomando como antecedente ' +str(res_data[index]['Antecedente']+' existe un aumento de posibilidades de  '
            +str(res_data[index]['Elevación'])+ ' veces para consumir igualmente '+str(res_data[index]['Consecuente'])+'. Tal que se tiene una confianza del '
            +str(res_data[index]['Confianza'])+' considerando una importancia de la regla del '+str(res_data[index]['Soporte'])),
               id=f"descript-{index}",
               style={'display': 'none'},
               className="description_rule"),
    )
    button = html.Button(
        id=id_str,
        className='toggle-button',
        **{"data-target": index},
        children='Ver detalles',
        n_clicks=0,
        style={'margin-left': '10px'},
    )
    description_row = html.Tr([
        html.Td(
            html.Table(
                html.Tr(html.Td(description, colSpan='7')),
                className="nested-table"
            ),
            className="single-column-table",
            colSpan='7'
        )
    ], id=f"description-row-{index}")

    return [html.Tr([
                html.Td(str(value)) for value in data.values()
            ] + [html.Td(button)]),
            description_row]