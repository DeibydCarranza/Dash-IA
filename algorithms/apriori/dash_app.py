import dash
from dash import dcc, html,Input, Output, callback, State
from .. import components
import os
from . import tool as tl 
from django_plotly_dash import DjangoDash
from . import method as met
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

#  ---------- Iniciando aplicación ---------------
app = DjangoDash('section_apriori')
df = None
path_file = os.path.join(os.path.dirname(__file__), '../data/file.csv')



# ------- Funciones -----------
""" Recuperando los valores de las reglas al modificar los parámetros"""
def show_rules(df, input_val_1, input_val_2, input_val_3):

    results_df = met.application(df, input_val_1, input_val_2, input_val_3)
    print(results_df)

    if not results_df.empty:
        # Crear una lista para almacenar los elementos del acordeón
        accordion_items = []

        for index, row in results_df.iterrows():
            regla = row['Regla']
            antecedente = row['Antecedente']
            consecuente = row['Consecuente']
            soporte = row['Soporte']
            confianza = row['Confianza']
            elevacion = row['Elevación']

            accordion_item = dmc.AccordionItem([
                    dmc.AccordionControl([
                        html.Table([
                            html.Tbody(
                                html.Tr([
                                    html.Td(regla, style={"width": "27%"}),
                                    html.Td(antecedente, style={"width": "15%"}),
                                    html.Td(consecuente, style={"width": "15%"}),
                                    html.Td(soporte, style={"width": "17%"}),
                                    html.Td(confianza, style={"width": "15%"}),
                                    html.Td(elevacion, style={"width": "19%"}),
                                ])
                            )
                        ])                        
                    ]),
                    dmc.AccordionPanel(
                        html.Div(
                            html.P('Tomando como antecedente ' +str(antecedente)+' existe un aumento de posibilidades de  '
                                +str(elevacion)+ ' veces para consumir igualmente '+str(consecuente)+'. Tal que se tiene una confianza del '
                                +str(confianza)+' considerando una importancia de la regla del '+str(soporte),
                                id=f"descript-{index}",
                                className="description_rule"),
                        )
                    ),
                ],
                value=f"item-{index}",
            )

            accordion_items.append(accordion_item)

        accordion = dmc.Accordion(children=accordion_items)
        cards_container = html.Div(accordion, className='cards-container')
        titulos = html.Table([
                            html.Thead(
                                html.Tr([
                                    html.Th("Regla", style={"width": "25%"}),
                                    html.Th("Antecedente", style={"width": "15%"}),
                                    html.Th("Consecuente", style={"width": "15%"}),
                                    html.Th("Soporte", style={"width": "15%"}),
                                    html.Th("Confianza", style={"width": "15%"}),
                                    html.Th("Elevación", style={"width": "15%"}),
                                ])
                            ),
                        ]) 
        return html.Div([titulos,cards_container])
    else:
        return html.Div('No se encontraron reglas asociadas a los parámetros.')


""" Bloque de slider/Input, se considera sufijos para identificarlos """
def block_params():
    texto1="Soporte"
    texto2="Confianza"
    texto3="Presentación"
    section_mod1 = mod_params_slide_input(0, 50, "-1",texto1)
    section_mod2 = mod_params_slide_input(0, 80, "-2",texto2)
    section_mod3 = mod_params_slide_input(0, 6, "-3",texto3)

    layout = html.Div(
        children=[
            section_mod1,
            section_mod2,
            section_mod3,
            dmc.Button('Procesar', id='submit-val',variant="gradient"),
            html.Div(id="output-container"),  # Contenedor para mostrar los valores
        ],
        className='block-params-container'
    )
    return layout

""" Componente dual Slider-Input. Los sufijos ayudan a no duplicarlos """
def mod_params_slide_input(mini, maxi, suffix="",texto=""):
    input_id = "input-circular" + suffix
    slider_id = "slider-circular" + suffix

    section_mod = html.Div(
        children=[
            dmc.Text(texto, weight=700),
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
            html.H1("Sección de parámetros", style={'text-align': 'center', 'margin-bottom': '30px', 'margin-top': '50px'}),
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