from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import seaborn as sns
from dash import dash_table
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate


df = pd.read_csv('Pokemon.csv')

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])



colors = {
    'background': '#e4d3f5',
    'text': '#0a3cd1',
    'fig': '#f0f7f7'
}


@app.callback(
    Output(component_id='output-table', component_property='children'),
    [Input(component_id='generation-dropdown', component_property='value'),
     Input(component_id='n-input', component_property='value')]
)


# @app.callback(
#     Output(component_id='div-2', component_property='figure'),
#     [Input(component_id='pokemons', component_property='value')]
# )

def update_table(generation, n):
    df_gen = df[['Name','Total']].loc[df['Generation']==generation]
    df_gen = df_gen.sort_values('Total', ascending=False).head(n)
    return dash_table.DataTable(
        id='table',
        columns=[{"name": 'Name', "id": 'Name'}, {"name": 'Total', "id": 'Total'}],
        data=df_gen.to_dict("rows"),
        style_table = {'width': '400px', 'height': '500px','display': 'inline-block'}
    )

def update_figure(pokemons):
    data=[]
    for i in range (len(pokemons)) :
        pokemon = pokemons[i]
        categories=['HP','Attack','Defense','Sp. Atk','Sp. Def','Speed']
        values = df[categories].loc[df['Name']==pokemon].values.flatten().tolist()
        data.append(go.Scatterpolar(r=values, theta=categories, fill='toself', name=pokemon))

    fig = go.Figure(
        data=data,
        layout=go.Layout(
            title=go.layout.Title(text='Comparaison de stats'),
            polar={'radialaxis': {'visible': False}},
            showlegend=True))

    return fig


top = 9
# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options



colors1 = {'Water': 'darkblue',
          'Normal': 'gray',
          'Grass': 'darkgreen',
         'Bug': 'olive',
          'Psychic': 'crimson',
          'Fire': 'orangered',
         'Electric': 'gold',
          'Rock': 'darkkhaki',
          'Dragon': 'rebeccapurple',
         'Ground': 'darkgoldenrod',
          'Ghost': 'midnightblue',
          'Poison': 'purple',
         'Steel': 'slategray',
          'Fighting': 'saddlebrown',
          'Ice': 'lightblue',
         'Fairy': 'pink',
          'Flying': 'lightseagreen',
         'Dark': 'black'}


df_top = df.groupby(df['Type 1']).size().to_frame().sort_values([0], ascending = False).head(top).reset_index()
df_down = df.groupby(df['Type 1']).size().to_frame().sort_values([0], ascending = True).head(top).reset_index()


def colors_type(df):
    colors2=[]
    for x in range(len(df)):
        colors2.append(colors1[df['Type 1'][x]])
    return colors2

def update_bar_chart(clickData):
    if clickData is not None:
        selected_generation = clickData["points"][0]["label"]
        filtered_df = df[df["Generation"] == selected_generation]
        df_gb = filtered_df.groupby(by="Generation")["Total"].mean().reset_index()
        fig_gen = px.bar(df_gb, x="Generation", y="Total", color="Generation", color_discrete_sequence=px.colors.sequential.Viridis)
        fig_gen.update_layout(title="Moyenne de total-stats par Generation", xaxis_title="Generation", yaxis_title="Mean Total")
        return fig_gen
    else:
        raise PreventUpdate

# pokemon['type1'].value_counts(normalize=True).nlargest(4).plot(kind="pie",
#         colors=[colors2[x] for x in pokemon['type1'].value_counts()[:top].index])
fig = px.histogram(df_top, x='Type 1', y = 0, color = df_top['Type 1'], color_discrete_sequence = colors_type(df_top))
fig_2 = px.histogram(df_down, x='Type 1', y = 0, color = df_down['Type 1'], color_discrete_sequence = colors_type(df_down))

# generation_bar = px.histogram(df, x= "Generation")

top_4 = df["Type 1"].value_counts().head(4).index.tolist()
df_filtered = df[df["Type 1"].isin(top_4)]

pie_type = px.pie(df_filtered, names="Type 1", title="Top 4 des types de pokemon", color_discrete_sequence=px.colors.sequential.Viridis)

df_gb = df.groupby(by = "Generation")["Total"].mean().reset_index()
fig_gen = px.bar(df_gb, x="Generation", y="Total", color="Generation", color_discrete_sequence=px.colors.sequential.Viridis)
fig_gen.update_layout(title="Moyenne de total-stats par Generation", xaxis_title="Generation", yaxis_title="Mean Total")

pokemon = df['Name'][0]
categories=['HP','Attack','Defense','Sp. Atk','Sp. Def','Speed']
values = df[categories].loc[df['Name']==pokemon].values.flatten().tolist()

# Define the callback function to update the bar chart based on the data point clicked in the pie chart
@app.callback(
    Output("graph2", "figure"),
    [Input("graph1", "clickData")]
)
def update_bar_chart(clickData):
    # If no data is clicked, show the average total by generation
    if not clickData:
        df_gb = df.groupby(by="Generation")["Total"].mean().reset_index()
        fig_gen = px.bar(df_gb, x="Generation", y="Total", color="Generation", color_discrete_sequence=px.colors.sequential.Viridis)
        fig_gen.update_layout(title="Moyenne de total-stats par Generation", xaxis_title="Generation", yaxis_title="Mean Total")
        return fig_gen

    # Extract the selected data point from the clickData
    type_name = clickData["points"][0]["label"]

    # Create a filtered dataframe based on the selected data point
    df_filtered = df[df["Type 1"] == type_name]

    # Group the filtered dataframe by generation and calculate the mean total
    df_gb = df_filtered.groupby(by="Generation")["Total"].mean().reset_index()

    # Create the bar chart figure
    fig_gen = px.bar(df_gb, x="Generation", y="Total", color="Generation", color_discrete_sequence=px.colors.sequential.Viridis)
    fig_gen.update_layout(title=f"Moyenne de total-stats par Generation pour les Pokemons de type {type_name}", xaxis_title="Generation", yaxis_title="Mean Total")

    return fig_gen


app.layout = html.Div(style={'text-align': 'center'}, children=[
    html.H1(children='Pokemon, Attrapez les tous',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }),

    html.Div([
    html.H2('Top 5 des pokemons par total de stats'),
    dcc.Dropdown(
        id='generation-dropdown',
        options=[{'label': i, 'value': i} for i in df['Generation'].unique()],
        value=1,
        style = {'width': '200px', 'margin-left': '382px'}
    ),
    dcc.Input(id='n-input', value=10, type='number'),
    html.Br(),
    html.Div(id='output-table',style={'width': '40%','display': 'inline-block'}),
    ]),

    html.Div(style={'text-align': 'center'}, children =[
        html.H3(children = 'Statistiques'),
        dcc.Dropdown(
        id="pokemon-dropdown",
        options=[{'label': i, 'value': i} for i in df['Name'].unique()],
        value= pokemon,
        style = {'width': '700px', 'margin-left': '270px'},
        multi=True
    ),
    html.Div(id='pokemon-div',style={'width': '40%','display': 'inline-block'}),
    dcc.Graph(id='pokemon-graph', figure=update_figure(pokemon),style={'margin-left': '50px', 'margin-bottom': '100px'}),
    ]),

    html.H3('Types et Générations', style={'text-align': 'center'}),
    html.Div(style={'text-align': 'center'},
        children=[
        dcc.Graph(id="graph1", figure=pie_type, style={'display': 'inline-block'}),
        dcc.Graph(id="graph2", figure= fig_gen ,style={'display': 'inline-block'})
    ]),

    # html.Div(children =[
    #     dcc.Graph(id= 'bar-generation', figure = go.Figure(data=data_gen,layout=layout_gen), style={'display': 'inline-block'})
    # ])
])

@app.callback(
    Output(component_id='pokemon-graph', component_property='figure'),
    [Input(component_id='pokemon-dropdown', component_property='value')]
)
# Define the callback function to update the bar chart based on the data point clicked in the pie chart
# @app.callback(
#     Output(component_id="graph2", component_property="figure"),
#     [Input(component_id="graph1", component_property="clickData")]
# )


def update_pokemon_graph(pokemon):
    return update_figure(pokemon)


if __name__ == '__main__':
    app.run_server(debug=True)
