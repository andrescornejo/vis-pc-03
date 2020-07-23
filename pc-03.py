# pc-03

import pandas as pd
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

df = pd.read_csv("cpi-data.csv")
df = df.groupby(['CPI 2016 Rank','Country', 'Country Code'])[['CPI 2016 Score']].mean()
df.reset_index(inplace=True)
print(df[:10])

# App layout
app.layout = html.Div([

    html.H1("Placeholder header", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_year",
                options=[
                    {"label": "2016", "value": 'CPI 2016 Score'},
                    {"label": "2015", "value": 'CPI 2015 Score'},
                    {"label": "2014", "value": 'CPI 2014 Score'},
                    {"label": "2013", "value": 'CPI 2013 Score'},
                    {"label": "2012", "value": 'CPI 2012 Score'}],
                multi=False,
                value='CPI 2016 Score',
                style={'width': "40%"}
                ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='cpi_map', figure={})

])

# Connect Plotly with Dash
@app.callback(
    [Output(component_id='output_container', component_property='children'),
    Output(component_id='cpi_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)

def update_graph(option_selected):
    print(option_selected)
    print(type(option_selected))

    container = "The year chosen by user was: {}".format(option_selected)

    dff = df.copy()
    fig = px.choropleth(dff, locations="Country Code",
                    color="CPI 2016 Score", # lifeExp is a column of gapminder
                    hover_name="Country", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.Plasma)
    return container, fig
  #  dff = dff[dff["CPI 2016 Score"] == option_selected]
  #  dff = dff[dff[""]]
# Main function

if __name__ == '__main__':
    app.run_server(debug=True)
# http://127.0.0.1:8050/