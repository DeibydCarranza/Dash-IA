import dash
from dash import dcc, html,Input, Output, callback, State
from .. import components
import os
from . import tool as tl 
from django_plotly_dash import DjangoDash

# Iniciando aplicación
app = DjangoDash('section_apriori')

path_file = os.path.join(os.path.dirname(__file__), '../data/file.csv')
print(path_file)

""" Componente dual Slider-Input. Los sufijos ayudan a no duplicarlos """
def mod_params_slide_input(mini, maxi, suffix="",step=0.1):
    input_id = "input-circular" + suffix
    slider_id = "slider-circular" + suffix

    section_mod = html.Div(
        children=[
            dcc.Slider(
                id=slider_id,
                min=mini,
                max=maxi,
                marks={i: str(i) for i in range(maxi + 1)},
                value=(maxi / 3)
            ),
            dcc.Input(
                id=input_id,
                type="number",
                min=mini,
                max=maxi,
                value=(maxi / 3),
                step = step
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
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
        value = input_value if trigger_id == input_id else slider_value
        return value, value

    return section_mod

""" Bloque de slider/Input, se considera sufijos para identificarlos """
def block_params():
    section_mod1 = mod_params_slide_input(0, 1, "-1")
    section_mod2 = mod_params_slide_input(0, 2, "-2")
    section_mod3 = mod_params_slide_input(0, 6, "-3",1)

    # Variables para almacenar los valores de los componentes
    value_1 = (section_mod1.children[0].value, section_mod1.children[1].value)
    value_2 = (section_mod2.children[0].value, section_mod2.children[1].value)
    value_3 = (section_mod3.children[0].value, section_mod3.children[1].value)
    print(value_1)


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
            # Aquí puedes procesar los valores como desees
            return html.Div(f"Values: {input_val_1}, {input_val_2}, {input_val_3}")

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

# Sección de retorno a renderizar
app.layout = html.Div(children=[
    components.upload_component,

    
],  
    style={'width': '100%', 'height': '100%'}
)   

section_patrams =  block_params()
# ---- Callbacks -----------

# Carga de archivo y renderizado de los elementos hijos
@app.callback(
        Output('output-data-upload', 'children'),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename')
)
def update_output(list_of_contents, list_of_names):
    if list_of_contents is None:
        return html.Div('No se seleccionó ningún archivo.')
    else:
        children = [
            tl.parse_contents(list_of_contents, list_of_names, path_file),
            section_patrams
        ]
        return children

