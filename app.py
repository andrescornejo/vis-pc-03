# pc-03

import pandas as pd
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ])

df = pd.read_csv("cpi-data.csv")
df = df.groupby(['CPI 2016 Rank','Country', 'Country Code'])[['CPI 2016 Score','CPI 2015 Score','CPI 2014 Score','CPI 2013 Score','CPI 2012 Score']].mean()
df.reset_index(inplace=True)
print(df[:10])

mapbox_style = "mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz"

# App layout
app.layout = html.Div(
    id="root",
    children=[
    html.Div(
        id="header",
        children=[
            html.H4(children="Índice de corrupción percibida mundialmente"),
            html.P(
                id="description",
                children="""El índice de percepción de corrupción, según transparency.org, es un ranking de territorios y países. 
                El ranking está basado en qué tan corrupto es percibido el sector público por expertos y ejecutivos del mundo empresarial. """,
            ),
        ]
    ),
    html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="graph-container",
                    children=[
                        html.P(id="chart-selector", children="Seleccione un año:"),
                        dcc.Dropdown(
                            options=[
                                {"label": "Corrupción percibida en el 2016", "value": 'CPI 2016 Score'},
                                {"label": "Corrupción percibida en el 2015", "value": 'CPI 2015 Score'},
                                {"label": "Corrupción percibida en el 2014", "value": 'CPI 2014 Score'},
                                {"label": "Corrupción percibida en el 2013", "value": 'CPI 2013 Score'},
                                {"label": "Corrupción percibida en el 2012", "value": 'CPI 2012 Score'}],
                            multi=False,
                            value='CPI 2016 Score',
                            id="chart-dropdown",
                        ),
                        dcc.Graph(id='cpi_map', figure={}
                        )
                    ],
                ),
            ],
        ),
    ],
)

    # dcc.Dropdown(id="slct_year",
                # options=[
                    # {"label": "2016", "value": 'CPI 2016 Score'},
                    # {"label": "2015", "value": 'CPI 2015 Score'},
                    # {"label": "2014", "value": 'CPI 2014 Score'},
                    # {"label": "2013", "value": 'CPI 2013 Score'},
                    # {"label": "2012", "value": 'CPI 2012 Score'}],
                # multi=False,
                # value='CPI 2016 Score',
                # style={'width': "40%"}
                # ),
# 
    # html.Div(id='output_container', children=[]),
    # html.Br(),
# 
    # dcc.Graph(id='cpi_map', figure={})
 


# Connect Plotly with Dash
@app.callback(
    # [Output(component_id='heatmap-container', component_property='children'),
    Output(component_id='cpi_map', component_property='figure'),
    [Input(component_id='chart-dropdown', component_property='value')]
)

def update_graph(option_selected):
    print(option_selected)
    print(type(option_selected))



    dff = df.copy()
    fig = px.choropleth(dff, locations="Country Code",
                    color=option_selected, 
                    hover_name="Country", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.Inferno,
                    template='plotly_dark',
    )
    return fig

# Main function

if __name__ == '__main__':
    app.run_server(debug=True)
# http://127.0.0.1:8050/