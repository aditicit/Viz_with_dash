import pandas as pd
import plotly.express as px  

import dash 
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = pd.read_csv("E:\Data Science\Bank_Dataset\Train.csv")

df['Item_Weight']=df['Item_Weight'].fillna(df['Item_Weight'].mean())
df['Outlet_Size']=df['Outlet_Size'].fillna(df['Outlet_Size'].mode()[0])
df['Item_Fat_Content']=df['Item_Fat_Content'].replace({'low fat':'Low Fat','LF':'Low Fat','reg':'Regular'})
fig1 = px.bar(data_frame=df, x="Item_Type",color="Outlet_Type",barmode="stack")
fig2 = px.bar(data_frame=df, x="Item_Type",color="Item_Fat_Content",barmode="stack")

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div(children=[

    html.Div([

    html.H1("Dashboard of Big Mart Dataset with Dash", style={'text-align': 'center'}),
        
    ## create a dash core component-drop down with different outlet options
    dcc.Dropdown(id="outlet_type",
                 options=[
                     {"label": "Supermarket Type1", "value": 'Supermarket Type1'},
                     {"label": "Supermarket Type2", "value": 'Supermarket Type2'},
                     {"label": "Grocery Store", "value": 'Grocery Store'},
                     {"label": "Supermarket Type3", "value": 'Supermarket Type3'}],
                 multi=False,
                 value='Grocery Store',
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='big_mart_map', figure={})

]),
    ## Bar chart representation of Item Vs Outlet
    html.Div([
            html.H1(children='Item Vs Outlet'),

            html.Div(children='''
                Count of Item present in different Outlet
            '''),

            dcc.Graph(
                id='graph2',
                figure=fig1
            ),  
        ], className='six columns'),
    
    ## Stacked bar chart showing Fat present in each item
    html.Div([
            html.H1(children='Fat content in each item'),

            dcc.Graph(
                id='graph3',
                figure=fig2
            ),  
        ], className='row')
])
    
# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='big_mart_map', component_property='figure')],
    [Input(component_id='outlet_type', component_property='value')]
)
## this function will return a countplot of the selected outlet option
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The outlet selected by user was: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["Outlet_Type"] == option_slctd]
    print(dff)
    df_group = dff.groupby(by=["Outlet_Type","Outlet_Location_Type"]).size().reset_index(name="counts")
    print(df_group)
    fig = px.bar(data_frame=df_group, x="Outlet_Type", y="counts", color="Outlet_Location_Type", barmode="group")
    return container, fig



# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)