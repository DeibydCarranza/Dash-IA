import dash
from dash import dcc, html,Input, Output, State
from .. import components as comp
from . import method as met
from datetime import date
from . import tool as tl 
from . import layout as lay
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify             
import yfinance as yf


app = DjangoDash('section_pronosArbBosq')

min_step = 0
max_step = 4
active = 0

X_t = None
X_val = None
Y_t = None
Y_val = None

CompanyHist = None
df = None
selected_ticker = None

""" ——————————————— Body ——————————————"""
app.layout= html.Div(
    [
            dcc.Store(id="store_select"),
            dmc.Stepper(
                id="stepper-basic-usage",
                active=active,
                breakpoint="sm",
                children=[
                    dmc.StepperStep(
                        label="Selección de mercado",
                        description="Acciones a analizar sobre una empresa",
                        children=[lay.dropdown_list_yfinance(),dcc.Store(id="ticker-search")]
                    ),
                    dmc.StepperStep(
                        label="Historial de acciones",
                        description="Visualizando un periodo de tiempo",
                        children= [html.Div(id='output-data-upload'),html.Div(id='output-container-date-picker-range')]
                    ),
                    dmc.StepperStep(
                        label="Aplicación del algoritmo",
                        description="Selección del tipo de algoritmo y ejecución",
                        children=[
    comp.mod_params_train(1),
    dmc.Button('Entrenar', id='btn-train', n_clicks=0, variant="gradient"),
    html.Div("", style={'margin-bottom': '40px'}),
    html.Div(id='columns-output-container-1'),  # Primera salida del callback
    html.Div(id='model-validation-layout')  # Segunda salida del callback
]
                    ),
                    dmc.StepperStep(
                        label="Nuevos pronósticos",
                        description="Generación de predicciones",
                        children=[]
                    ),
                    dmc.StepperCompleted(
                        children=dmc.Text(
                            "Se han completado todos los pasos pendientes",
                            align="center",
                        )
                    ),
                ],
            ),
            dmc.Group(
                position="center",
                mt="xl",
                children=[
                    dmc.Button("Back", id="back-basic-usage", variant="default"),
                    dmc.Button("Next step", id="next-basic-usage"),
                ],
            ),
    ],style={'width': '100%', 'height': '100%'}
)

"""—————————— callbacks ———————————————————"""
""" Select Steper """
@app.callback(
    [Output("stepper-basic-usage", "active"),
     Output("store_select","data")],
    [Input("back-basic-usage", "n_clicks"),
    Input("next-basic-usage", "n_clicks")],
    State("stepper-basic-usage", "active"),
    prevent_initial_call=True,
)
def update(back, next_, current):
    ctx = dash.callback_context
    if not ctx.triggered:
        return ''

    button_id = ctx.triggered[0]['prop_id']
    step = current if current is not None else active
    if button_id == "back-basic-usage.n_clicks":
        step = step - 1 if step > min_step else step
    else:
        step = step + 1 if step < max_step else step
    return step,step


""" Empresa seleccionada por dropdwon principal """
@app.callback([Output("selected-value-yfinance", "children"), 
               Output("output-data-upload", "children"),
               Output("ticker-search","data")],
            [Input("list_yfinance_select", "value")]
)
def select_value(value):
    if value:
        children = [
            lay.section_params_date()
        ]
        return "Has seleccionado " + value, children,value
    else:
        return "No has seleccionado ninguna empresa", [],None


""" Devolver la fecha escogida para la primera evaluación """
@app.callback(
    Output('output-container-date-picker-range', 'children'),
    [Input('btn_proc_date', 'n_clicks'),
    Input("ticker-search","data")],
    [State('my-date-picker-range', 'start_date'),
    State('my-date-picker-range', 'end_date'),
    State('input_interval', 'value')]
)
def update_output(n_clicks, ticker,start_date, end_date, interval):
    if n_clicks is None:
        return dash.no_update
    
    if start_date is None or end_date is None:
        return "Seleccione un rango de fechas y un intervalo en días."
    
    if interval is None or interval == '':
        return "Ingrese un intervalo en días válido."
    
    global df,CompanyHist
    df = yf.Ticker(str(ticker))

    # Leyendo y formateando las fechas a YYYY-MM-DD
    start_date_object = date.fromisoformat(start_date)
    end_date_object = date.fromisoformat(end_date)
    start_date_formatted = start_date_object.strftime('%Y-%-m-%-d')
    end_date_formatted = end_date_object.strftime('%Y-%-m-%-d')

    graph, CompanyHist = tl.table_historial(df,ticker,start_date_formatted,end_date_formatted,interval)
    
    return graph

""" Paso de columnas para ser procesadas mediante dropdown"""
@app.callback(
    [Output('columns-output-container-1', 'children'), Output('model-validation-layout', 'children')],
    [Input('btn-train', 'n_clicks')],
    [State('input_size_train_1', 'value'),
     State('input_random_state_1', 'value'),
     State('boolean-switch_1', 'checked'),
     State('model-validation-layout', 'children')]
)
def update_output_columns(n_clicks, size_train, random_state, shuffle, current_validation_layout):
    global  X_t, X_val, Y_t, Y_val
    print("\t\t------162 dashpp")
    # Si no se ha presionado "Entrenar" y no se han ingresado mínimo 2 columnas en dropdwon 
    if n_clicks is not None:
        #Se establece un valor por defecto en el tamaño
        if size_train is None:
            size_train = 20
        print("\t\t------169 dashpp")
        X_t, X_val, Y_t, Y_val = met.variablesClasePredict(CompanyHist,(size_train/100),random_state,shuffle)
        layout_models = comp.tab_for_methods()
        return f'Carga exitosa de entrenamiento', layout_models

    return f'No has seleccionado ninguna variable para entrenar', current_validation_layout




