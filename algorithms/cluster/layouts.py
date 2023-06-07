from dash import html,ctx
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

matrix_cluster = html.Div(
    id='div_matrix_clu',
    children=[
        html.H4("CORRELATION MATRIX"),
        html.Div(
            id='output_matrix_clu',
            style={
                'display': 'flex',
                'justify-content': 'center',
                'align-items': 'center'
            }
        )
    ]
)

select_input = html.Div( id='tag', children =
    [
        dmc.Select(
            label="Select tag",
            placeholder="ej. diagnostic, ...",
            id="select_tag_clu",
            value="",
            data=[],
            style={"width": 200, "marginBottom": 10},
        )
    ]
)


