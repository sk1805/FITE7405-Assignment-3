import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import numpy as np
from models.black_scholes import black_scholes
from models.implied_volatility import implied_volatility
from models.geometric_asian import geometric_asian
from models.arithmetic_asian_mc import arithmetic_asian_mc
from models.geometric_basket import geometric_basket
from models.arithmetic_basket_mc import arithmetic_basket_mc
from models.american_binomial import american_binomial
from models.kiko_quasi_mc import kiko_quasi_mc

# Custom CSS styles
external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap'
]

# Initialize the Dash app with custom styling
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Custom theme colors
theme_colors = {
    'primary': '#3498db',
    'secondary': '#2ecc71',
    'background': '#f8f9fa',
    'text': '#2c3e50',
    'border': '#e9ecef'
}

# Common styles for components
input_style = {
    'borderRadius': '8px',
    'border': f'1px solid {theme_colors["border"]}',
    'padding': '10px',
    'marginBottom': '15px'
}

label_style = {
    'fontWeight': '500',
    'marginBottom': '5px',
    'color': theme_colors['text']
}

button_style = {
    'borderRadius': '8px',
    'padding': '10px 20px',
    'fontWeight': '600',
    'textTransform': 'none'
}

# About Us content
about_us_content = html.Div([
    html.H2("About Us", className="mb-4", style={'color': theme_colors['text'], 'fontWeight': '700'}),
    html.Div([
        html.H3("Group 30", className="mb-3", style={'color': theme_colors['primary']}),
        html.Div([
            html.H4("Abhimanyu Bhati", className="mb-2", style={'color': theme_colors['text']}),
            html.P("SID: 3036383745",
                  className="mb-4", style={'color': theme_colors['text']}),
            html.H4("Sameer Kabani", className="mb-2", style={'color': theme_colors['text']}),
            html.P("SID: 3036384012",
                  className="mb-4", style={'color': theme_colors['text']}),
        ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
    ], style={'maxWidth': '800px', 'margin': '0 auto'})
], style={'padding': '40px', 'backgroundColor': theme_colors['background']})

# Model-specific tabs
tabs = [
    # Black-Scholes (European) tab
    dbc.Tab([
        html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Spot Price (S(0))", style=label_style),
                    dbc.Input(id="bs-S", type="number", value=100, step=1, style=input_style),
                ], width=6),
                dbc.Col([
                    dbc.Label("Strike Price (K)", style=label_style),
                    dbc.Input(id="bs-K", type="number", value=100, step=1, style=input_style),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Risk-free Rate (r)", style=label_style),
                    dbc.Input(id="bs-r", type="number", value=0.05, step=0.05, style=input_style),
                ], width=6),
                dbc.Col([
                    dbc.Label("Repo Rate (q)", style=label_style),
                    dbc.Input(id="bs-q", type="number", value=0.02, step=0.05, style=input_style),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Time to Maturity (T)", style=label_style),
                    dbc.Input(id="bs-T", type="number", value=1.0, step=1, style=input_style),
                ], width=6),
                dbc.Col([
                    dbc.Label("Volatility (σ)", style=label_style),
                    dbc.Input(id="bs-sigma", type="number", value=0.2, step=0.01, style=input_style),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Option Type", style=label_style),
                    dbc.Select(
                        id="bs-option-type",
                        options=[
                            {"label": "Call", "value": "call"},
                            {"label": "Put", "value": "put"}
                        ],
                        value="call",
                        style=input_style
                    ),
                ], width=6),
            ]),
            dbc.Button("Calculate", id="bs-calculate", color="primary", className="mt-3", style=button_style),
            html.Div(id="bs-result", className="mt-3", style={'padding': '15px', 'backgroundColor': 'white', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
        ], style={'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
    ], label="European Option", tab_style={'fontWeight': '500'}),
    
    # Implied Volatility tab
    dbc.Tab([
        html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Spot Price (S(0))", style=label_style),
                    dbc.Input(id="iv-S", type="number", value=100, step=1, style=input_style),
                ], width=6),
                dbc.Col([
                    dbc.Label("Strike Price (K)", style=label_style),
                    dbc.Input(id="iv-K", type="number", value=100, step=1, style=input_style),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Risk-free Rate (r)", style=label_style),
                    dbc.Input(id="iv-r", type="number", value=0.05, step=0.05, style=input_style),
                ], width=6),
                dbc.Col([
                    dbc.Label("Repo Rate (q)", style=label_style),
                    dbc.Input(id="iv-q", type="number", value=0.02, step=0.05, style=input_style),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Time to Maturity (T)", style=label_style),
                    dbc.Input(id="iv-T", type="number", value=1.0, step=1, style=input_style),
                ], width=6),
                dbc.Col([
                    dbc.Label("Option Premium", style=label_style),
                    dbc.Input(id="iv-market-price", type="number", value=10, step=1, style=input_style),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Option Type", style=label_style),
                    dbc.Select(
                        id="iv-option-type",
                        options=[
                            {"label": "Call", "value": "call"},
                            {"label": "Put", "value": "put"}
                        ],
                        value="call",
                        style=input_style
                    ),
                ], width=6),
            ]),
            dbc.Button("Calculate", id="iv-calculate", color="primary", className="mt-3", style=button_style),
            html.Div(id="iv-result", className="mt-3", style={'padding': '15px', 'backgroundColor': 'white', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
        ], style={'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
    ], label="Implied Volatility", tab_style={'fontWeight': '500'}),
    
    # Geometric Asian tab
    dbc.Tab([
        html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Spot Price (S(0))", style=label_style),
                    dbc.Input(id="ga-S", type="number", value=100, step=1, style=input_style),
                ], width=6),
                dbc.Col([
                    dbc.Label("Volatility (σ)", style=label_style),
                    dbc.Input(id="ga-sigma", type="number", value=0.3, step=0.01, style=input_style),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Risk-free Rate (r)", style=label_style),
                    dbc.Input(id="ga-r", type="number", value=0.05, step=0.05, style=input_style),
                ], width=6),
                dbc.Col([
                    dbc.Label("Time to Maturity (T)", style=label_style),
                    dbc.Input(id="ga-T", type="number", value=3.0, step=1, style=input_style),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Strike Price (K)", style=label_style),
                    dbc.Input(id="ga-K", type="number", value=100, step=1, style=input_style),
                ], width=6),
                dbc.Col([
                    dbc.Label("Number of Observations (n)", style=label_style),
                    dbc.Input(id="ga-n", type="number", value=50, step=1, style=input_style),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Option Type", style=label_style),
                    dbc.Select(
                        id="ga-option-type",
                        options=[
                            {"label": "Call", "value": "call"},
                            {"label": "Put", "value": "put"}
                        ],
                        value="call",
                        style=input_style
                    ),
                ], width=6),
            ]),
            dbc.Button("Calculate", id="ga-calculate", color="primary", className="mt-3", style=button_style),
            html.Div(id="ga-result", className="mt-3", style={'padding': '15px', 'backgroundColor': 'white', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
        ], style={'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
    ], label="Geometric Asian", tab_style={'fontWeight': '500'}),
    
    # Arithmetic Asian tab
    dbc.Tab([
        html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Spot Price (S(0))", style=label_style),
                    dbc.Input(id="aa-S", type="number", value=100, step=1, style=input_style),
                ], width=6),
                dbc.Col([
                    dbc.Label("Volatility (σ)", style=label_style),
                    dbc.Input(id="aa-sigma", type="number", value=0.3, step=0.01, style=input_style),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Risk-free Rate (r)", style=label_style),
                    dbc.Input(id="aa-r", type="number", value=0.05, step=0.05, style=input_style),
                ], width=6),
                dbc.Col([
                    dbc.Label("Time to Maturity (T)", style=label_style),
                    dbc.Input(id="aa-T", type="number", value=3.0, step=1, style=input_style),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Strike Price (K)", style=label_style),
                    dbc.Input(id="aa-K", type="number", value=100, step=1, style=input_style),
                ], width=6),
                dbc.Col([
                    dbc.Label("Number of Observations (n)", style=label_style),
                    dbc.Input(id="aa-n", type="number", value=50, step=1, style=input_style),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Option Type", style=label_style),
                    dbc.Select(
                        id="aa-option-type",
                        options=[
                            {"label": "Call", "value": "call"},
                            {"label": "Put", "value": "put"}
                        ],
                        value="call",
                        style=input_style
                    ),
                ], width=6),
                dbc.Col([
                    dbc.Label("Number of Simulations (m)", style=label_style),
                    dbc.Input(id="aa-num-simulations", type="number", value=100000, step=1000, style=input_style),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Control Variate Method", style=label_style),
                    dbc.Select(
                        id="aa-control-variate",
                        options=[
                            {"label": "No Control Variate", "value": "none"},
                            {"label": "Geometric Asian", "value": "geometric"}
                        ],
                        value="none",
                        style=input_style
                    ),
                ], width=6),
            ]),
            dbc.Button("Calculate", id="aa-calculate", color="primary", className="mt-3", style=button_style),
            html.Div(id="aa-result", className="mt-3", style={'padding': '15px', 'backgroundColor': 'white', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
        ], style={'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
    ], label="Arithmetic Asian", tab_style={'fontWeight': '500'}),
    
    # Geometric Basket tab
    dbc.Tab([
        html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Spot Price 1 (S1(0))", style=label_style),
                    dbc.Input(id="gb-S1", type="number", value=100, step=1, style=input_style),
                ], width=6),
                dbc.Col([
                    dbc.Label("Spot Price 2 (S2(0))", style=label_style),
                    dbc.Input(id="gb-S2", type="number", value=100, step=1, style=input_style),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Volatility 1 (σ1)", style=label_style),
                    dbc.Input(id="gb-sigma1", type="number", value=0.3, step=0.01, style=input_style),
                ], width=6),
                dbc.Col([
                    dbc.Label("Volatility 2 (σ2)", style=label_style),
                    dbc.Input(id="gb-sigma2", type="number", value=0.3, step=0.01, style=input_style),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Risk-free Rate (r)", style=label_style),
                    dbc.Input(id="gb-r", type="number", value=0.05, step=0.05, style=input_style),
                ], width=6),
                dbc.Col([
                    dbc.Label("Time to Maturity (T)", style=label_style),
                    dbc.Input(id="gb-T", type="number", value=3.0, step=1, style=input_style),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Strike Price (K)", style=label_style),
                    dbc.Input(id="gb-K", type="number", value=100, step=1, style=input_style),
                ], width=6),
                dbc.Col([
                    dbc.Label("Correlation (ρ)", style=label_style),
                    dbc.Input(id="gb-rho", type="number", value=0.5, step=0.01, style=input_style),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Option Type", style=label_style),
                    dbc.Select(
                        id="gb-option-type",
                        options=[
                            {"label": "Call", "value": "call"},
                            {"label": "Put", "value": "put"}
                        ],
                        value="call",
                        style=input_style
                    ),
                ], width=6),
            ]),
            dbc.Button("Calculate", id="gb-calculate", color="primary", className="mt-3", style=button_style),
            html.Div(id="gb-result", className="mt-3", style={'padding': '15px', 'backgroundColor': 'white', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
        ], style={'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
    ], label="Geometric Basket", tab_style={'fontWeight': '500'}),
    
    # Arithmetic Basket tab
    dbc.Tab([
        html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Spot Price 1 (S1(0))", style=label_style),
                    dbc.Input(id="ab-S1", type="number", value=100, step=1, style=input_style),
                ], width=6),
                dbc.Col([
                    dbc.Label("Spot Price 2 (S2(0))", style=label_style),
                    dbc.Input(id="ab-S2", type="number", value=100, step=1, style=input_style),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Volatility 1 (σ1)", style=label_style),
                    dbc.Input(id="ab-sigma1", type="number", value=0.3, step=0.01, style=input_style),
                ], width=6),
                dbc.Col([
                    dbc.Label("Volatility 2 (σ2)", style=label_style),
                    dbc.Input(id="ab-sigma2", type="number", value=0.3, step=0.01, style=input_style),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Risk-free Rate (r)", style=label_style),
                    dbc.Input(id="ab-r", type="number", value=0.05, step=0.05, style=input_style),
                ], width=6),
                dbc.Col([
                    dbc.Label("Time to Maturity (T)", style=label_style),
                    dbc.Input(id="ab-T", type="number", value=3.0, step=1, style=input_style),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Strike Price (K)", style=label_style),
                    dbc.Input(id="ab-K", type="number", value=100, step=1, style=input_style),
                ], width=6),
                dbc.Col([
                    dbc.Label("Correlation (ρ)", style=label_style),
                    dbc.Input(id="ab-rho", type="number", value=0.5, step=0.01, style=input_style),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Option Type", style=label_style),
                    dbc.Select(
                        id="ab-option-type",
                        options=[
                            {"label": "Call", "value": "call"},
                            {"label": "Put", "value": "put"}
                        ],
                        value="call",
                        style=input_style
                    ),
                ], width=6),
                dbc.Col([
                    dbc.Label("Number of Simulations (m)", style=label_style),
                    dbc.Input(id="ab-num-simulations", type="number", value=100000, step=1000, style=input_style),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Control Variate Method", style=label_style),
                    dbc.Select(
                        id="ab-control-variate",
                        options=[
                            {"label": "No Control Variate", "value": "none"},
                            {"label": "Geometric Basket", "value": "geometric"}
                        ],
                        value="none",
                        style=input_style
                    ),
                ], width=6),
            ]),
            dbc.Button("Calculate", id="ab-calculate", color="primary", className="mt-3", style=button_style),
            html.Div(id="ab-result", className="mt-3", style={'padding': '15px', 'backgroundColor': 'white', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
        ], style={'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
    ], label="Arithmetic Basket", tab_style={'fontWeight': '500'}),
    
    # American Option tab
    dbc.Tab([
        html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Option Type", style=label_style),
                    dbc.Select(
                        id='american-option-type',
                        options=[
                            {'label': 'Put', 'value': 'put'},
                            {'label': 'Call', 'value': 'call'}
                        ],
                        value='put',
                        style=input_style
                    )
                ], width=12)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Spot Price (S(0))", style=label_style),
                    dbc.Input(id="american-S", type="number", value=50, step=1, style=input_style),
                ], width=6),
                dbc.Col([
                    dbc.Label("Strike Price (K)", style=label_style),
                    dbc.Input(id="american-K", type="number", value=40, step=1, style=input_style),
                ], width=6)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Risk-free Rate (r)", style=label_style),
                    dbc.Input(id="american-r", type="number", value=0.1, step=0.05, style=input_style),
                ], width=6),
                dbc.Col([
                    dbc.Label("Time to Maturity (T)", style=label_style),
                    dbc.Input(id="american-T", type="number", value=2.0, step=1, style=input_style),
                ], width=6)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Volatility (σ)", style=label_style),
                    dbc.Input(id="american-sigma", type="number", value=0.4, step=0.05, style=input_style),
                ], width=6),
                dbc.Col([
                    dbc.Label("Number of Steps (N)", style=label_style),
                    dbc.Input(id="american-N", type="number", value=200, style=input_style)
                ], width=6)
            ]),
            dbc.Button("Calculate", id="american-calculate", color="primary", className="mt-3", style=button_style),
            html.Div(id="american-output", className="mt-3", style={'padding': '15px', 'backgroundColor': 'white', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
        ], style={'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
    ], label="American Option", tab_style={'fontWeight': '500'}),
    
    # KIKO Put Option tab
    dbc.Tab([
        html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Spot Price (S(0))", style=label_style),
                    dbc.Input(id="kiko-S", type="number", value=100, step=1, style=input_style),
                ], width=6),
                dbc.Col([
                    dbc.Label("Strike Price (K)", style=label_style),
                    dbc.Input(id="kiko-K", type="number", value=100, step=1, style=input_style),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Risk-free Rate (r)", style=label_style),
                    dbc.Input(id="kiko-r", type="number", value=0.05, step=0.05, style=input_style),
                ], width=6),
                dbc.Col([
                    dbc.Label("Time to Maturity (T)", style=label_style),
                    dbc.Input(id="kiko-T", type="number", value=2.0, step=1, style=input_style),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Volatility (σ)", style=label_style),
                    dbc.Input(id="kiko-sigma", type="number", value=0.2, step=0.01, style=input_style),
                ], width=6),
                dbc.Col([
                    dbc.Label("Lower Barrier (L)", style=label_style),
                    dbc.Input(id="kiko-L", type="number", value=80, step=1, style=input_style),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Upper Barrier (U)", style=label_style),
                    dbc.Input(id="kiko-U", type="number", value=125, step=1, style=input_style),
                ], width=6),
                dbc.Col([
                    dbc.Label("Rebate (R)", style=label_style),
                    dbc.Input(id="kiko-R", type="number", value=1.5, step=1, style=input_style),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Number of Observation Times (n)", style=label_style),
                    dbc.Input(id="kiko-n", type="number", value=24, step=1, style=input_style),
                ], width=6),
                dbc.Col([
                    dbc.Label("Calculate Delta", style=label_style),
                    dbc.Select(
                        id="kiko-calculate-delta",
                        options=[
                            {"label": "Yes", "value": "yes"},
                            {"label": "No", "value": "no"}
                        ],
                        value="yes",
                        style=input_style
                    ),
                ], width=6),
            ]),
            dbc.Button("Calculate", id="kiko-calculate", color="primary", className="mt-3", style=button_style),
            html.Div(id="kiko-result", className="mt-3", style={'padding': '15px', 'backgroundColor': 'white', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
        ], style={'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
    ], label="KIKO Put Option", tab_style={'fontWeight': '500'}),
]

# Update the app layout with About Us at the end
app.layout = html.Div([
    html.H1("Option Pricing Calculator", 
            className="text-center mb-4",
            style={'color': theme_colors['text'], 
                   'fontWeight': '700',
                   'padding': '20px 0'}),
    
    dbc.Container([
        dbc.Tabs([
            *[tab for tab in tabs if tab.label != "About Us"],
            dbc.Tab(about_us_content, label="About Us", tab_style={'fontWeight': '500'})
        ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
    ], fluid=True)
], style={'backgroundColor': theme_colors['background'], 'minHeight': '100vh', 'padding': '20px'})

def format_result(value, title, additional_info=None):
    result_div = [
        html.H4(title, style={'color': theme_colors['primary'], 'marginBottom': '10px', 'fontWeight': '600'}),
        html.H3(f"{value:.6f}", style={'color': theme_colors['text'], 'fontWeight': '700'})
    ]
    
    if additional_info:
        for info_title, info_value in additional_info.items():
            if isinstance(info_value, (tuple, list)):
                result_div.append(html.H5(
                    f"{info_title}: [{info_value[0]:.6f}, {info_value[1]:.6f}]",
                    style={'color': theme_colors['text'], 'marginTop': '10px', 'fontWeight': '500'}
                ))
            else:
                result_div.append(html.H5(
                    f"{info_title}: {info_value:.6f}",
                    style={'color': theme_colors['text'], 'marginTop': '10px', 'fontWeight': '500'}
                ))
    
    return html.Div(result_div, style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})

@app.callback(
    Output("bs-result", "children"),
    [Input("bs-calculate", "n_clicks")],
    [
        State("bs-S", "value"),
        State("bs-K", "value"),
        State("bs-r", "value"),
        State("bs-q", "value"),
        State("bs-T", "value"),
        State("bs-sigma", "value"),
        State("bs-option-type", "value"),
    ],
)
def calculate_black_scholes(n_clicks, S, K, r, q, T, sigma, option_type):
    if n_clicks is None:
        return ""
    try:
        price = black_scholes(S, K, r, q, T, sigma, option_type)
        return format_result(price, "Option Price")
    except Exception as e:
        return html.Div([
            html.H4("Error", style={'color': '#e74c3c', 'marginBottom': '10px', 'fontWeight': '600'}),
            html.P(str(e), style={'color': theme_colors['text']})
        ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})

@app.callback(
    Output("iv-result", "children"),
    [Input("iv-calculate", "n_clicks")],
    [
        State("iv-S", "value"),
        State("iv-K", "value"),
        State("iv-r", "value"),
        State("iv-q", "value"),
        State("iv-T", "value"),
        State("iv-market-price", "value"),
        State("iv-option-type", "value"),
    ],
)
def calculate_implied_volatility(n_clicks, S, K, r, q, T, market_price, option_type):
    if n_clicks is None:
        return ""
    try:
        iv = implied_volatility(S, K, r, q, T, market_price, option_type)
        return format_result(iv, "Implied Volatility")
    except Exception as e:
        return html.Div([
            html.H4("Error", style={'color': '#e74c3c', 'marginBottom': '10px', 'fontWeight': '600'}),
            html.P(str(e), style={'color': theme_colors['text']})
        ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})

@app.callback(
    Output("ga-result", "children"),
    [Input("ga-calculate", "n_clicks")],
    [
        State("ga-S", "value"),
        State("ga-sigma", "value"),
        State("ga-r", "value"),
        State("ga-T", "value"),
        State("ga-K", "value"),
        State("ga-n", "value"),
        State("ga-option-type", "value"),
    ],
)
def calculate_geometric_asian(n_clicks, S, sigma, r, T, K, n, option_type):
    if n_clicks is None:
        return ""
    
    # Validate risk-free rate
    if r is None or r < 0 or r > 1:
        return html.Div("Error: Risk-free rate (r) must be between 0 and 1", style={"color": "red"})
    
    try:
        price = geometric_asian(S, sigma, r, T, K, n, option_type)
        return format_result(price, "Option Price")
    except Exception as e:
        return html.Div([
            html.H4("Error", style={'color': '#e74c3c', 'marginBottom': '10px', 'fontWeight': '600'}),
            html.P(str(e), style={'color': theme_colors['text']})
        ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})

@app.callback(
    Output("aa-result", "children"),
    [Input("aa-calculate", "n_clicks")],
    [
        State("aa-S", "value"),
        State("aa-sigma", "value"),
        State("aa-r", "value"),
        State("aa-T", "value"),
        State("aa-K", "value"),
        State("aa-n", "value"),
        State("aa-option-type", "value"),
        State("aa-num-simulations", "value"),
        State("aa-control-variate", "value"),
    ],
)
def calculate_arithmetic_asian(n_clicks, S, sigma, r, T, K, n, option_type, num_simulations, control_variate):
    if n_clicks is None:
        return ""
    try:
        price, stderr = arithmetic_asian_mc(S, sigma, r, T, K, n, option_type, num_simulations, control_variate)
        conf_interval = [price - 1.96 * stderr, price + 1.96 * stderr]
        additional_info = {
            "Standard Error": stderr,
            "95% Confidence Interval": conf_interval
        }
        return format_result(price, "Option Price", additional_info)
    except Exception as e:
        return html.Div([
            html.H4("Error", style={'color': '#e74c3c', 'marginBottom': '10px', 'fontWeight': '600'}),
            html.P(str(e), style={'color': theme_colors['text']})
        ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})

@app.callback(
    Output("gb-result", "children"),
    [Input("gb-calculate", "n_clicks")],
    [
        State("gb-S1", "value"),
        State("gb-S2", "value"),
        State("gb-sigma1", "value"),
        State("gb-sigma2", "value"),
        State("gb-r", "value"),
        State("gb-T", "value"),
        State("gb-K", "value"),
        State("gb-rho", "value"),
        State("gb-option-type", "value"),
    ],
)
def calculate_geometric_basket(n_clicks, S1, S2, sigma1, sigma2, r, T, K, rho, option_type):
    if n_clicks is None:
        return ""
    
    # Validate risk-free rate
    if r is None or r < 0 or r > 1:
        return html.Div("Error: Risk-free rate (r) must be between 0 and 1", style={"color": "red"})
    
    try:
        price = geometric_basket(S1, S2, sigma1, sigma2, r, T, K, rho, option_type)
        return format_result(price, "Option Price")
    except Exception as e:
        return html.Div([
            html.H4("Error", style={'color': '#e74c3c', 'marginBottom': '10px', 'fontWeight': '600'}),
            html.P(str(e), style={'color': theme_colors['text']})
        ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})

@app.callback(
    Output("ab-result", "children"),
    [Input("ab-calculate", "n_clicks")],
    [
        State("ab-S1", "value"),
        State("ab-S2", "value"),
        State("ab-sigma1", "value"),
        State("ab-sigma2", "value"),
        State("ab-r", "value"),
        State("ab-T", "value"),
        State("ab-K", "value"),
        State("ab-rho", "value"),
        State("ab-option-type", "value"),
        State("ab-num-simulations", "value"),
        State("ab-control-variate", "value"),
    ],
)
def calculate_arithmetic_basket(n_clicks, S1, S2, sigma1, sigma2, r, T, K, rho, option_type, num_simulations, control_variate):
    if n_clicks is None:
        return ""
    try:
        price, stderr, conf_interval = arithmetic_basket_mc(S1, S2, sigma1, sigma2, r, T, K, rho, option_type, num_simulations, control_variate)
        if isinstance(conf_interval, (tuple, list)) and len(conf_interval) == 2:
            additional_info = {
                "Standard Error": stderr,
                "95% Confidence Interval": (conf_interval[0], conf_interval[1])
            }
        else:
            additional_info = {
                "Standard Error": stderr
            }
        return format_result(price, "Option Price", additional_info)
    except Exception as e:
        return html.Div([
            html.H4("Error", style={'color': '#e74c3c', 'marginBottom': '10px', 'fontWeight': '600'}),
            html.P(str(e), style={'color': theme_colors['text']})
        ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})

@app.callback(
    Output("american-output", "children"),
    [Input("american-calculate", "n_clicks")],
    [
        State("american-S", "value"),
        State("american-K", "value"),
        State("american-r", "value"),
        State("american-T", "value"),
        State("american-sigma", "value"),
        State("american-N", "value"),
        State("american-option-type", "value")
    ],
)
def calculate_american(n_clicks, S, K, r, T, sigma, N, option_type):
    if n_clicks is None:
        return ""
    try:
        american_price = american_binomial(S, K, r, T, sigma, N, option_type)
        european_price = black_scholes(S, K, r, 0, T, sigma, option_type)
        early_exercise_premium = american_price - european_price
        
        return format_result(american_price, "Option Price", {
            "Early Exercise Premium": early_exercise_premium,
            "European Price": european_price
        })
    except Exception as e:
        return html.Div([
            html.H4("Error", style={'color': '#e74c3c', 'marginBottom': '10px', 'fontWeight': '600'}),
            html.P(str(e), style={'color': theme_colors['text']})
        ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})

@app.callback(
    Output("kiko-result", "children"),
    [Input("kiko-calculate", "n_clicks")],
    [
        State("kiko-S", "value"),
        State("kiko-K", "value"),
        State("kiko-r", "value"),
        State("kiko-T", "value"),
        State("kiko-sigma", "value"),
        State("kiko-L", "value"),
        State("kiko-U", "value"),
        State("kiko-R", "value"),
        State("kiko-n", "value"),
        State("kiko-calculate-delta", "value"),
    ],
)
def calculate_kiko(n_clicks, S, K, r, T, sigma, L, U, R, n, calculate_delta):
    if n_clicks is None:
        return ""
    
    # Validate all input parameters are not None
    if any(v is None for v in [S, K, r, T, sigma, L, U, R, n]):
        return html.Div("Error: All fields must be filled", style={"color": "red"})
    
    # Validate risk-free rate
    if r < 0 or r > 1:
        return html.Div("Error: Risk-free rate (r) must be between 0 and 1", style={"color": "red"})
    
    # Validate barriers
    if L >= U:
        return html.Div("Error: Lower barrier (L) must be less than upper barrier (U)", style={"color": "red"})
    
    # Validate positive values
    if any(v <= 0 for v in [S, K, T, sigma, n]):
        return html.Div("Error: Spot price, strike price, time to maturity, volatility, and number of observations must be positive", style={"color": "red"})
    
    # Validate rebate
    if R < 0:
        return html.Div("Error: Rebate must be non-negative", style={"color": "red"})
    
    try:
        calculate_delta = calculate_delta == "yes"
        result = kiko_quasi_mc(S, K, r, T, sigma, L, U, R, n, calculate_delta)
        
        if calculate_delta:
            price, stderr, conf_interval, delta = result
            if isinstance(conf_interval, (tuple, list)) and len(conf_interval) == 2:
                additional_info = {
                    "Standard Error": stderr,
                    "95% Confidence Interval": (conf_interval[0], conf_interval[1]),
                    "Delta": delta
                }
            else:
                additional_info = {
                    "Standard Error": stderr,
                    "Delta": delta
                }
        else:
            price, stderr, conf_interval = result
            if isinstance(conf_interval, (tuple, list)) and len(conf_interval) == 2:
                additional_info = {
                    "Standard Error": stderr,
                    "95% Confidence Interval": (conf_interval[0], conf_interval[1])
                }
            else:
                additional_info = {
                    "Standard Error": stderr
                }
        return format_result(price, "Option Price", additional_info)
    except Exception as e:
        return html.Div([
            html.H4("Error", style={'color': '#e74c3c', 'marginBottom': '10px', 'fontWeight': '600'}),
            html.P(str(e), style={'color': theme_colors['text']})
        ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})

if __name__ == "__main__":
    app.run_server(debug=True) 