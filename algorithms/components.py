from dash import dcc, html,dash_table

""" Generate update component (just html) """
upload_component = html.Div([
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
              'padding-bottom: 10%'
       },
       # Permitir cargar múltiples archivos
       multiple=False
       ),
       html.Div(id='output-data-upload'),
])

""" Create and return dash_table """
def create_data_table(df, indexFlag):
       if indexFlag:
              df_with_index = df.reset_index()
              columns = [{"name": "Index", "id": "index"}] + [{"name": i, "id": i} for i in df.columns]
              data = df_with_index.to_dict("records")
       else:
              columns = [{"name": i, "id": i} for i in df.columns]
              data = df.to_dict("records")

       table = dash_table.DataTable(
              id="database-table",
              columns=columns,
              data=data,
              sort_action="native",
              sort_mode="native",
              page_size=10,
              style_table={'overflowX': 'scroll', 'overflowY': 'scroll', 'color': '#3c3c3c'}
       )
       return table


