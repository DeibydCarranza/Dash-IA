from dash import html,ctx,dcc
import dash_mantine_components as dmc

standarizar = html.Div(id='button-container-est',children=[
    dmc.Button('Normalizar', id='btn-nclicks-nor',variant="gradient", n_clicks=0),
    dmc.Button('Escalar', id='btn-nclicks-esc',variant="gradient", n_clicks=0),
    dmc.Button('View', id='btn-nclicks-view',variant="gradient", n_clicks=0),
    html.Div(id='container-button-timestamp')
])

select_algorithm = html.Div(id='select-metricas',children=
    [
        dmc.Select(
            id="framework-select-metricas",
            data=[
                {"value": "euclidean", "label": "Euclidiana"},
                {"value": "chebyshev", "label": "Chebyshev"},
                {"value": "cityblock", "label": "Manhattan"},
                {"value": "minkowski", "label": "Minkowski"},
            ],
            style={"width": 200, "marginBottom": 10},
        ),
        html.Div(id="selected-value-metricas")
    ]
)

p_to_minkowski = dmc.Group(id = 'input-to-minkowski', children = [
    dmc.TextInput(id='lambda',placeholder="Lambda", style={"width": 200}, disabled=False),
    dmc.Button("ok", id='button-leer-valor',variant="gradient"),
    html.Div(id='output-valor')
    ]
)

matrix_cluster = dmc.Accordion(
    id='tab_matrix_clustering',
    children=[
        dmc.AccordionItem(
            children=[
                dmc.AccordionControl("Apoyos Visuales"),
                dmc.AccordionPanel(
                    children=[
                        dmc.Tabs(
                            [
                                dmc.TabsList(
                                    position="center",
                                    grow=True,
                                    children=[
                                        dmc.Tab("Gráfica de Dispersión", value="despersion"),
                                        dmc.Tab("Matriz de Correlación", value="correlacion")
                                    ]
                                )
                            ],
                            id='tab_clustering',
                            value='',
                            color="blue",
                            variant='pills',
                            orientation="horizontal"
                        ),
                        html.Div(
                            id='output_tabs_clustering',
                            style={
                                "paddingTop": 10,
                                "display": "flex",
                                "justifyContent": "center",
                                "alignItems": "center"
                            }
                        )
                    ]
                )
            ],
            value="on"
        )
    ],
    style={
        "position": "relative",
        "textAlign": "center"
    }
)



select_input = html.Div( id='tag', children =
    [
        dcc.Store(id="store_tag"),
        dmc.Select(
            label="Select tag",
            placeholder="ej. diagnostic, ...",
            id="select_tag_clu",
            value="",
            data=[],
            style={"width": 200, "marginBottom": 10},
        ), 
        html.Div(id = 'output_delete_tag')
    ]
)

MultiSelect_to_featuring = html.Div( id = 'SuperDiv_MultiSelect',children =
    [
        dmc.MultiSelect(
            label="Caracteristicas para el algoritmo",
            placeholder="No atributos de alta correlación",
            id="input_multiselect",
            value=[],
            data=[],
            style={"width": 400, "marginBottom": 10},
        ),
        dmc.Text(id='read_multiselect', style = {'display': 'none'}),
        dmc.Button("Generar Matrix", id = 'generate_matrix_ok'),
    ]
)

clustering = html.Div([
    dmc.Tabs(
        [
            dmc.TabsList(
                position="center",
                grow=True,
                children=[
                    dmc.Tab("Jerarquico", value="j"),
                    dmc.Tab("Particional", value="p")
                ]
            )
        ],
        id='tap_logic_clustering',
        value='',
        color="blue",
        variant='pills',
        orientation="horizontal"
    ),
    html.Div(
        id='output_tabs_logic_Clu',children=[
        ],
        style={
            "paddingTop": 10,
            "display": "flex",
            "justifyContent": "center",
            "alignItems": "center"
        }
    )
])
