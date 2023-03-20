#Package import
import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output



#initialising app
app = dash.Dash(
    external_stylesheets = [dbc.themes.DARKLY])


#colours
colors = {
    'black' : '#1A1B25',
    'red' : '#F8C271E',
    'white' : '#EFE9E7',
    'background' : '#333333',
    'text' : '#FFFFFF'
}

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
    brand="FPL dashboard",
    brand_href="#",
    color="dark",
    dark=True,
)


app.layout = html.Div(className = 'document', children=[
    navbar,
    html.H1(children = "Pokemon Attrapez les tous", className = "text-center p-3", style = {'color': '#EFE9E7'}),
    html.H3(children = "Le meilleur site sur les Pokemon.", className = "text-center p-2 text-light ")

    ])




if __name__ == '__main__':
    app.run_server(debug=True)
