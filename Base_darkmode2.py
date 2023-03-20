#Package import
import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from dash import dash_table
#initialising app
app = dash.Dash(
    external_stylesheets = [dbc.themes.DARKLY])

df = pd.read_csv('Pokemon.csv')
#colours
colors = {
    'black' : '#1A1B25',
    'red' : '#F8C271E',
    'white' : '#EFE9E7',
    'background' : '#333333',
    'text' : '#FFFFFF'
}

@app.callback(
    Output(component_id='output-table', component_property='children'),
    [Input(component_id='generation-dropdown', component_property='value'),
     Input(component_id='n-input', component_property='value')]
)


def update_table(generation, n):
    df_gen = df[['Name','Total']].loc[df['Generation']==generation]
    df_gen = df_gen.sort_values('Total', ascending=False).head(n)
    return dash_table.DataTable(
        id='table',
        columns=[{"name": 'Name', "id": 'Name'}, {"name": 'Total', "id": 'Total'}],
        data=df_gen.to_dict("rows"),style_data={
        'color': 'black',
        'backgroundColor': 'white'
    },
        style_table = {'color': 'black',
        'backgroundColor': 'white','display': 'inline-block'})

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

#COMPONENTS

#navbar
navbar = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("How it works", href="#"),
                dbc.DropdownMenuItem("The statistics", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="Explore",
        ),
    ],
    brand="Sudoku team",
    brand_href="#",
    color="dark",
    dark=True,
)

# figure

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

app.layout = html.Div(className = 'document', children=[
    navbar,
    html.H1(children = "Pokemon Attrapez les tous", className = "text-center p-3", style = {'color': '#EFE9E7'}),
    html.Img(src=app.get_asset_url('graffiti-pokemon-toulouse.jpg'),style={"text-align":"center"}),
    html.H3(children = "Le meilleur site sur les Pokemons !", className = "text-center p-2 text-light "),

    html.Div(children =[ html.H4(children = 'Statistique des Pokémon'),
        dcc.Dropdown(
        id="pokemon-dropdown",
        options=[{'label': i, 'value': i} for i in df['Name'].unique()],
        value= pokemon,
        style = {'width': '1000px','color': 'black',
        'backgroundColor': 'white'},
        multi=True
    ),
    html.Div(id='pokemon-div',style={'width': '40%'}),
    dcc.Graph(id='pokemon-graph', figure=update_figure(pokemon),style={'display': 'inline-block'}),
    html.Img(id = 'html_img' , src=app.get_asset_url('png-clipart-pokeball-pokeball-thumbnail.png'),style={'width': '10%','display': 'inline-block'})
    ]),
    html.Div([
    html.H2('Top 5 Pokemons by total'),
    dcc.Dropdown(
        id='generation-dropdown',
        options=[{'label': i, 'value': i} for i in df['Generation'].unique()],
        value=1,
        style = {'width': '200px','color': 'black',
        'backgroundColor': 'white'}
    ),
    dcc.Input(id='n-input', value=10, type='number'),
    html.Br(),
    html.Div(id='output-table',style={'width': '40%','display': 'inline-block'}),
    ]),
     html.H3('Les top et les flop des types de Pokemon'),
    html.Div(children=[
        dcc.Graph(id="graph1", figure=fig, style={'display': 'inline-block'}),
        dcc.Graph(id="graph2", figure= fig_2 ,style={'display': 'inline-block'})

    ]),
    ])

@app.callback(
    Output(component_id='pokemon-graph', component_property='figure'),
    [Input(component_id='pokemon-dropdown', component_property='value')]
)
# putain de callback

def update_pokemon_graph(pokemon):
    return update_figure(pokemon)



if __name__ == '__main__':
    app.run_server(debug=True)
