from dash import html,ctx
standarizar = html.Div(id='button-container-est',children=[
    html.Button('Normalizar', id='btn-nclicks-nor', n_clicks=0),
    html.Button('Escalar', id='btn-nclicks-esc', n_clicks=0),
    html.Button('View', id='btn-nclicks-view', n_clicks=0),
    html.Div(id='container-button-timestamp')
])

