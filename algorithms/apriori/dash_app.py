import dash
from dash import dcc, html,Input, Output, callback, State
from .. import components
import os
from . import tool as tl 
from django_plotly_dash import DjangoDash
from . import method as met
import pandas as pd
import io

#  ---------- Iniciando aplicación ---------------
app = DjangoDash('section_apriori')
df = None
path_file = os.path.join(os.path.dirname(__file__), '../data/file.csv')



# ------- Funciones -----------
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

""" Recuperando los valores de las reglas al modificar los parámetros"""
def show_rules(df, input_val_1, input_val_2, input_val_3):

    results_df = met.application(df, input_val_1, input_val_2, input_val_3)
    if not results_df.empty:
        # Convertir el DataFrame en una lista de diccionarios
        res_data = results_df.to_dict('records')
        res_data = [data for data in res_data if isinstance(data, dict)]

        # Generar los títulos de la tabla y sus filas
        title_row = html.Tr([html.Th(col) for col in res_data[0].keys()] + [html.Th("Acciones")])
        titles = html.Thead(title_row)
        card_rows = []
        for index, data in enumerate(res_data):
            card_rows.extend(generate_card(data, index, res_data))

        # Generar el cuerpo de la tabla con las filas de tarjetas
        card_body = html.Tbody(card_rows)
        table_rules = html.Table([titles, card_body], id="titulos")
        cards_container = html.Div(table_rules, className='cards-container')

        return html.Div([cards_container])
    else:
        return html.Div('No se encontraron reglas asociadas a los parámetros.')
    

""" Bloque de slider/Input, se considera sufijos para identificarlos """
def block_params():
    section_mod1 = mod_params_slide_input(0, 50, "-1")
    section_mod2 = mod_params_slide_input(0, 80, "-2")
    section_mod3 = mod_params_slide_input(0, 6, "-3")

    layout = html.Div(
        children=[
            section_mod1,
            section_mod2,
            section_mod3,
            html.Div(id="output-container"),  # Contenedor para mostrar los valores
            html.Button('Procesar', id='submit-val'),
        ],
        className='block-params-container'
    )
    return layout

""" Componente dual Slider-Input. Los sufijos ayudan a no duplicarlos """
def mod_params_slide_input(mini, maxi, suffix=""):
    input_id = "input-circular" + suffix
    slider_id = "slider-circular" + suffix

    section_mod = html.Div(
        children=[
            dcc.Slider(
                id=slider_id,
                min=mini,
                max=maxi,
                #step=stepSlider,
                marks={i: str(i) for i in range(maxi + 1)},
                value=(maxi / 3)
            ),
            dcc.Input(
                id=input_id,
                type="number",
                min=mini,
                max=maxi,
                value=(maxi / 3),
                step=0.001
            )
        ],
        className='slider-input-container'
    )
    @app.callback(
        [Output(input_id, "value"), Output(slider_id, "value")],
        [Input(input_id, "value"), Input(slider_id, "value")]
    )
    def update_output(input_value, slider_value):
        ctx = dash.callback_context
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else None
        value = input_value if trigger_id == input_id else slider_value
        return value, value
    return section_mod



## ----------  Seción a renderizar   ---------- 
section_patrams =  block_params()

# Sección de retorno a renderizar
app.layout = html.Div(children=[
    components.upload_component,
    html.Div(id="output-data-upload"),
    html.Div(id="section-params"),
    html.Div(id="submit-val"),    
    html.Div(id="output-container"),
], style={'width': '100%', 'height': '100%'})




#  - ---- Callbacks individuales -----------

# Carga de archivo y renderizado de los elementos hijos
@app.callback(
    Output('output-data-upload', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_output(list_of_contents, list_of_names):
    global df
    if list_of_contents is None:
        return html.Div('No se seleccionó ningún archivo.')
    else:
        render, df = tl.parse_contents(list_of_contents, list_of_names, path_file)
        children = [
            render,
            section_patrams
        ]
        return children

# Renderizado de valores como parámetros
@app.callback(
    Output("output-container", "children"),
    [Input("submit-val", "n_clicks")],
    [State("input-circular-1", "value"),
     State("input-circular-2", "value"),
     State("input-circular-3", "value"),
     State("slider-circular-1", "value"),
     State("slider-circular-2", "value"),
     State("slider-circular-3", "value")]
)
def process_values(n_clicks, input_val_1, input_val_2, input_val_3, slider_val_1, slider_val_2, slider_val_3):
    if n_clicks is None:
        return html.Div()
    else:
        global df
        return show_rules(df, input_val_1, input_val_2, input_val_3)