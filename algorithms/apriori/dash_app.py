import dash
from dash import dcc, html
from .. import components,callbacks
import os

from django_plotly_dash import DjangoDash

app = DjangoDash('section_apriori')
path_file = os.path.join(os.path.dirname(__file__), '../data/', 'file.csv')
print(path_file)

app.layout = html.Div(children=[
    components.upload_component
])    