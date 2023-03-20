from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from dash import dash_table
from dash.dependencies import Input, Output
import plotly.graph_objects as go

app = Dash(__name__)

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
            title=go.layout.Title(text='Pokemons stats comparison'),
            polar={'radialaxis': {'visible': False}},
            showlegend=True
        )
    )
    return fig

top = 9
# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

df = pd.read_csv('Pokemon.csv')

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

fig = px.histogram(df_top, x='Type 1', y = 0, color = df_top['Type 1'], color_discrete_sequence = colors_type(df_top))
fig_2 = px.histogram(df_down, x='Type 1', y = 0, color = df_down['Type 1'], color_discrete_sequence = colors_type(df_down))
pokemon = df['Name'][0]
categories=['HP','Attack','Defense','Sp. Atk','Sp. Def','Speed']
values = df[categories].loc[df['Name']==pokemon].values.flatten().tolist()
fig_3= go.Figure(
        data=[
            go.Scatterpolar(r=values, theta=categories, fill='toself', name=pokemon),
        ],
        layout=go.Layout(
            title=go.layout.Title(text= pokemon +'s Stats'),
            polar={'radialaxis': {'visible': False}},
            showlegend=True
        )
    )
fig_3.update_layout(
    autosize=False,
    width=500,
    height=500)

app.layout = html.Div(children=[
    html.H1(children='Pokemon, Attrapez les tous',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }),

    html.Div([
    html.H2('Top 5 Pokemons by total'),
    dcc.Dropdown(
        id='generation-dropdown',
        options=[{'label': i, 'value': i} for i in df['Generation'].unique()],
        value=1,
        style = {'width': '200px'}
    ),
    dcc.Input(id='n-input', value=10, type='number'),
    html.Br(),
    html.Div(id='output-table',style={'width': '40%','display': 'inline-block'}),
    ]),

    html.Div(children =[
        html.H1(children = 'Stats de Pok'),
        dcc.Dropdown(
        id="pokemon-dropdown",
        options=[{'label': i, 'value': i} for i in df['Name'].unique()],
        value= pokemon,
        style = {'width': '1000px'},
        multi=True
    ),
    html.Div(id='pokemon-div',style={'width': '40%','display': 'inline-block'}),
    dcc.Graph(id='pokemon-graph', figure=update_figure(pokemon),style={'margin-left': '50px'}),
    ]),

    html.H3('Les top et les flop des types de Pokemon'),
    html.Div(children=[
        dcc.Graph(id="graph1", figure=fig, style={'display': 'inline-block'}),
        dcc.Graph(id="graph2", figure= fig_2 ,style={'display': 'inline-block'})

    ])
])

@app.callback(
    Output(component_id='pokemon-graph', component_property='figure'),
    [Input(component_id='pokemon-dropdown', component_property='value')]
)

def update_pokemon_graph(pokemon):
    return update_figure(pokemon)

if __name__ == '__main__':
    app.run_server(debug=True)
