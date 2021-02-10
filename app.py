import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go
import numpy as np

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

df = pd.read_csv("C:\\Users\\LENOVO\\WebScrapping\\covidreport.csv")
df=df.dropna()
df_continent=df['Continents'].value_counts().keys()
df_continent
#df1 = df.groupby(['Continents']).count()[['Deaths','Confirmed']]
#df1.reset_index(inplace=True)
#print(df1[:5])
df1= pd.read_csv("https://s3.amazonaws.com/rawstore.datahub.io/f6f2ac7be65b7d271b8a3b74df3ad724.csv")
df_Ind = df1[df1['Country']=='India']
print(df_Ind[:5])
df2_rest = pd.read_csv("https://s3.amazonaws.com/rawstore.datahub.io/9dc095afacc22888e66192aa23e71314.csv")

fig2 = px.sunburst(df, path=['Continents', 'Country'], values='Confirmed',
                  color='Deaths', hover_data=['Country'],
                  color_continuous_scale='RdBu',
                  color_continuous_midpoint=np.average(df['Deaths'], weights=df['Confirmed']))

fig3 = px.scatter_geo(df, locationmode='country names', locations='Country', color='Continents',
                     hover_name='Country', size='Confirmed',
                     projection='natural earth')

fig4 = px.area(df1, x="Date", y="Recovered", color="Country",line_group="Country")
fig4.update_xaxes(rangeslider_visible=True)
#fig4 = px.area(df1, facet_col=['Confirmed','Recovered','Deaths'], facet_col_wrap=3)
# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([
    
    html.Div([

    html.H1("Web Application Dashboards with Dash", style={'text-align': 'center'}),

    #dcc.Dropdown(id="slct_continent",
     #            options=[
     #                {'label': 'Asia', 'value': 'Asia'},
     #                {'label': 'Africa', 'value': 'Africa'},
     #                {'label': 'Europe', 'value': 'Europe'},
     #                {'label': 'South America', 'value': 'South America'},
     #                {'label': 'North America', 'value': 'North America'},
     #                {'label': 'Australia/Oceania', 'value': 'Australia/Oceania'},
     #               ],
     #            multi=False,
     #            value='Asia',
     #            style={'width': "40%"}
     #            ),
        dcc.Dropdown(
        id="option_slctd",
        options=[{"label": x1, "value": x1} 
                 for x1 in df_continent],
        value=df_continent[1],
        clearable=False,
        style={'width': "40%"}
    ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='covid_map', figure={})

]),

    html.Div([
            html.H1(children='Confirmed-Death cases'),

            dcc.Graph(
                id='graph2',
                figure=fig2
            ),  
        ]),
    
    html.Div([
            html.H1(children='Covid19 spread on Earth'),

            dcc.Graph(
                id='graph3',
                figure=fig3
            ),  
        ]),
    
    html.Div([
        
        html.H1("Daily update of Covid in India", style={'text-align': 'center'}),
        dcc.Dropdown(
        id="ticker",
        options=[{"label": x, "value": x} 
                 for x in df_Ind.columns[2:]],
        value=df_Ind.columns[3],
        clearable=False,
        style={'width': "40%"}    
    ),
    dcc.Graph(id="time-series-chart"),
        ]),
    
     html.Div([
            html.H1(children='Covid recovery on Earth'),

            dcc.Graph(
                id='graph4',
                figure=fig4
            ),  
        ])
])
# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='covid_map', component_property='figure'),
     Output("time-series-chart", "figure")],
    [Input(component_id='option_slctd', component_property='value'),
     Input("ticker", "value")]
)
def update_graph(option_slctd,ticker):
    
    container = "The Continent chosen by user was: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["Continents"] == option_slctd]
   
    # Plotly Express
    fig = px.choropleth(
        data_frame=dff,
        locationmode='country names',
        locations='Country',
        scope="world",
        color='Deaths',
        hover_data=['Country', 'Deaths','Confirmed'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Deaths': 'No. of Deaths'},
        template='plotly_dark'
    )
    
    fig5 = px.line(df_Ind, x='Date', y=ticker, title='Date tracking with Rangeslider')
    fig5.update_xaxes(rangeslider_visible=True)
    # Plotly Graph Objects (GO)
    # fig = go.Figure(
    #     data=[go.Choropleth(
    #         locationmode='USA-states',
    #         locations=dff['state_code'],
    #         z=dff["Pct of Colonies Impacted"].astype(float),
    #         colorscale='Reds',
    #     )]
    # )
    #
    # fig.update_layout(
    #     title_text="Bees Affected by Mites in the USA",
    #     title_xanchor="center",
    #     title_font=dict(size=24),
    #     title_x=0.5,
    #     geo=dict(scope='usa'),
    # )

    return container, fig, fig5


    
    

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)