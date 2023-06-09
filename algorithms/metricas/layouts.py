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
        dcc.Store(id="store_metric"),
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
    dcc.Store(id="store_lambda"),
    dmc.TextInput(id='lambda',placeholder="Lambda", style={"width": 200}, disabled=False),
    dmc.Button("ok", id='button-leer-valor',variant="gradient"),
    html.Div(id='output-valor')
    ]
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

compare= dmc.Stack(children=
[
    dmc.Center(children=
    [
        dmc.SimpleGrid(cols=2,children = 
        [
            dmc.TextInput(
                    id = 'element1',
                    label = 'Elemento a)',
                    required = True,
                    placeholder="10",
                    size='md',radius='xl'
            ),
            dmc.TextInput(
                    id = 'elemento2',
                    label = 'Elemento b)',
                    required = True,
                    placeholder="7",
                    size='md',radius='xl'
            ),
            dmc.Button("comparar",id="comparar_send",size='md',radius='xl')
        ])
    ]),
    html.Div(id='output_comparation')
],align="center",justify="center",spacing='sm')