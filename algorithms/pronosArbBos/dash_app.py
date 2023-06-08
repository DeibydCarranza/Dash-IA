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
from sklearn.tree import export_text

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

n_estimators_glo = None
PronoBA = None
Y_PronoBA = None
PronoAD = None
choose_Estimator_glo = None

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
                            html.Div(id='columns-output-container-1'), 
                            html.Div(id='model-validation-layout')
                        ]
                    ),
                    dmc.StepperStep(
                        label="Nuevos pronósticos",
                        description="Generación de predicciones",
                        children=[lay.pronostico()]
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
    print(interval)
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
    global  X_t, X_val, Y_t, Y_val,CompanyHist
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


# Define el callback para capturar los valores de los inputs para árbol
@app.callback(
    Output('input-values-container-tree', 'children'),
    [Input('generate-button-tree', 'n_clicks')],
    [State('input_max_depth_0', 'value'),
     State('input_min_samples_split_0', 'value'),
     State('input_min_samples_leaf_0', 'value'),
     State('input_random_state_0', 'value')]
)
def generate_input_values_tree(n_clicks, max_depth, min_samples_split, min_samples_leaf, random_state):  
    global X_t, X_val, Y_t, Y_val, PronoAD
    if n_clicks > 0:
        res_layoutAD, PronoAD = met.trainingTrees(X_t, X_val, Y_t, Y_val, max_depth, min_samples_split, min_samples_leaf, random_state)
        return [
            res_layoutAD
        ]
    else:
        return []

# Define el callback para capturar los valores de los inputs para Bosque
@app.callback(
    Output('input-values-container-forest', 'children'),
    [Input('generate-button-forest', 'n_clicks')],
    [State('input_max_depth_1', 'value'),
     State('input_min_samples_split_1', 'value'),
     State('input_min_samples_leaf_1', 'value'),
     State('input_random_state_1', 'value'),
     State('input_n_estimators_1', 'value')]
)
def generate_input_values_forest(n_clicks, max_depth, min_samples_split, min_samples_leaf, random_state, n_estimators):
    global n_estimators_glo, PronoBA, Y_PronoBA
    n_estimators_glo = n_estimators
    if n_clicks > 0:
        res_layoutBA, PronoBA, Y_PronoBA = met.trainingForest(X_t, X_val, Y_t, Y_val, max_depth,min_samples_split,min_samples_leaf,random_state ,n_estimators)
        return [
            res_layoutBA
        ]
    else:
        return []

# Estableciendo núm estimadores para el bosque 
@app.callback(Output('tree-image-forest', 'children'),
              [Input('btn-n-estimators', 'n_clicks')],
              [State('input_n_estimators', 'value')])
def update_output_bosque(n_clicks, choose_Estimator):
    global n_estimators_glo, PronoBA, Y_PronoBA,choose_Estimator_glo
    if n_clicks > 0:
        # Validar el rango del valor del Input
        if choose_Estimator is not None and 0 < choose_Estimator < n_estimators_glo:
            choose_Estimator_glo = choose_Estimator
            Estimador = PronoBA.estimators_[choose_Estimator]
            tree = comp.plotTree(Estimador,['Open', 'High', 'Low'],Y_PronoBA)

            layout = html.Div([
                html.Img(src='data:image/png;base64,{}'.format(tree), style={'width': '100%', 'height': 'auto'}),
                dmc.Button("Generar Reporte", id="btn-descarga-bosque",variant="gradient"),
                dcc.Download(id="download-reporte-bosque")
            ]),
            return layout
        else:
            return f"El valor debe ser mayor a 0 y menor a {n_estimators_glo}."
    else:
        return None

# Descargando el bosque generado en .txt
@app.callback(
    Output("download-reporte-bosque", "data"),
    [Input("btn-descarga-bosque", "n_clicks")],
    prevent_initial_call=True
)
def descargar_reporte_bosque(n_clicks):
    global choose_Estimator_glo, PronoBA
    Estimador = PronoBA.estimators_[choose_Estimator_glo]
    contenido = export_text(Estimador,feature_names =['Open', 'High', 'Low'])
    return dict(content=contenido, filename="reporteBosque.txt")

# Descargando el árbol generado en .txt
@app.callback(
    Output("download-reporte-arbol", "data"),
    [Input("btn-descarga-arbol", "n_clicks")],
    prevent_initial_call=True
)
def descargar_reporte_arbol(n_clicks):
    global PronoAD
    contenido = export_text(PronoAD,feature_names =['Open', 'High', 'Low'])
    return dict(content=contenido, filename="reporteArbol.txt")

@app.callback(
    Output('resultado-output', 'children'),
    [Input('pronosticar-button', 'n_clicks')],
    [State('open-input', 'value'),
     State('high-input', 'value'),
     State('low-input', 'value')]
)
def actualizar_pronostico(n_clicks, open_value, high_value, low_value):
    resultado = met.pronosticar(PronoBA,open_value, high_value, low_value)
    if resultado is not None:
        resultado_str = str(resultado).replace('[', '').replace(']', '')
        return f"De acuerdo a los datos, el pronóstico que se espera en el siguiente intervalo es {resultado_str}, considere que solo es un posible escenario a futuro"
    else:
        return "Ingrese los valores de Open, High y Low."