from dash import dcc, html

""" Generate update component (just html) """
upLoad_component = html.Div([
       dcc.Upload(
       id='upload-data',
       children=html.Div([
              'Carga de archivo ',
              html.A('Select CSV File')
       ]),
       style={
              'margin'
              'height': '60px',
              'lineHeight': '60px',
              'borderWidth': '2px',
              'borderStyle': 'dashed',
              'borderRadius': '5px',
              'textAlign': 'center',
              'margin': '50px 10px'
       },
       # Permitir cargar múltiples archivos
       multiple=False
       ),
       html.Div(id='output-data-upload'),
])