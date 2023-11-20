#import dash 
from dash import html, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
#import pandas as pd
from flask import Flask, url_for
from .mydash import * #access DataStore, MyDash
from .dashboard_turnover import * # <- new dashboard tab
from .dashboard_organization import * # <- new dashboard tab
from flask_login import login_required

#Create a Plotly Dash dashboard within a running Flask app.
# param Flask app: Top-level Flask application.
def add_dashboard (app : Flask):
    #initialized in MyDash
    dash_module = MyDash(
        name = __name__,
        server = app,
        url_base_pathname='/dashboard/',
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        meta_tags=[{'name': 'Dashboard', 'content': 'width=device-width, initial-scale=1.0'}]
    )

    # tab layout
    dash_module.layout = html.Div([
        dbc.Tabs([
            dbc.Tab(tab_id='tab-orgstructure', label="OrgStructure"),
            dbc.Tab(tab_id='tab-turnover', label="Turnover"),
        ], id = 'tabs', active_tab='tab-orgstructure'),
        html.Div(id="content")
    ])
    
    add_callback_tab(dash_module)
    #<-- todo: add new tab call backs below
    add_callback_turnover(dash_module) 
    add_callback_orgstructure(dash_module) 
    
    return dash_module.server

# add call back to Dash

def add_callback_tab(dash_module: MyDash):

    #change tab
    @dash_module.callback(Output('content', 'children'), [Input("tabs", "active_tab")])
    def change_tab(tab):
        if tab == 'tab-turnover':
            return render_turnover(dash_module)
        if tab == 'tab-orgstructure':
            return render_orgstructure(dash_module)
        else:
            return ''
